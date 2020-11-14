from lxml import etree
import requests
import os


class Answer(object):
    def __init__(self):
        self.id = ""
        self.url = ""
        self.response = None
        self.author = ""
        self.picURLList = []


class User(object):
    def __init__(self, cookie):
        self.Cookie = cookie
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        self.headers = {
            "cookie": self.Cookie,
            "user-agent": self.user_agent
        }
        self.session = requests.session()
        self.session.headers = self.headers
        self.currentBrowseAnswer = Answer()

    def getZhiHuAnswerWeb(self):
        response = self.session.get(url=self.currentBrowseAnswer.url)
        return response

    def getAnswerAuthor(self):
        content = self.currentBrowseAnswer.response.text
        HTML = etree.HTML(content)
        author = HTML.xpath(
            '//div[@class="Card AnswerCard"]//div[@class="AuthorInfo-content"]/div[@class="AuthorInfo-head"]//a[@class="UserLink-link"]/text()')[
            0]
        return author

    def extractPicURL(self):
        content = self.currentBrowseAnswer.response.text
        HTML = etree.HTML(content)
        picURLList = HTML.xpath(
            '//div[@class="Card AnswerCard"]//div[@class="RichContent-inner"]/span/figure/img/@data-original')
        return picURLList

    def downloadPicList(self):
        for url in self.currentBrowseAnswer.picURLList:
            self.downloadPic(url)

    def downloadPic(self, url):
        pic = self.session.get(url).content
        filename = os.path.basename(url)
        filename = filename[::-1][filename[::-1].index("?") + 1:][::-1]
        with open(self.currentBrowseAnswer.author + "/" + self.currentBrowseAnswer.id + "@" + filename, "wb") as f:
            f.write(pic)


if __name__ == '__main__':
    cookie = open("COOKIE", "r", encoding="utf-8")
    user = User(cookie.read())
    while True:
        inputArg = input("请输入知乎回答编号或链接: ")
        if inputArg.isdigit():
            user.currentBrowseAnswer.id = inputArg
            answerURL = "https://www.zhihu.com/answer/" + inputArg
        elif inputArg[:4] == "http":
            user.currentBrowseAnswer.id = inputArg[::-1][:inputArg[::-1].index("/")][::-1]
            answerURL = inputArg
        else:
            continue
        user.currentBrowseAnswer.url = answerURL
        user.currentBrowseAnswer.response = user.getZhiHuAnswerWeb()
        user.currentBrowseAnswer.author = user.getAnswerAuthor()
        # 没有答主的目录则创建
        if not os.path.exists(user.currentBrowseAnswer.author):
            os.mkdir(user.currentBrowseAnswer.author)
        user.currentBrowseAnswer.picURLList = user.extractPicURL()
        user.downloadPicList()
