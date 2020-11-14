from lxml import etree
import requests
import os


def getZhiHuAnswerWeb(AID):
    answerURL = "https://www.zhihu.com/answer/" + AID
    response = session.get(url=answerURL)
    return response


def extractPicURL(response):
    content = response.text
    HTML = etree.HTML(content)
    picURLList = HTML.xpath(
        '//div[@class="Card AnswerCard"]//div[@class="RichContent-inner"]/span/figure/img/@data-original')
    return picURLList


def downloadPicList(urlList):
    for url in urlList:
        downloadPic(url)


def downloadPic(url):
    pic = session.get(url).content
    filename = os.path.basename(url)
    filename = filename[::-1][filename[::-1].index("?") + 1:][::-1]
    with open(answerID + "/" + filename, "wb") as f:
        f.write(pic)


if __name__ == '__main__':
    session = requests.session()
    cookie = open("COOKIE", "r", encoding="utf-8")
    session.headers = {
        "cookie": cookie.read(),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }

    while True:
        answerID = input("请输入知乎回答编号: ")
        if not os.path.exists(answerID):
            os.mkdir(answerID)
        response = getZhiHuAnswerWeb(answerID)
        picURLList = extractPicURL(response)
        downloadPicList(picURLList)
