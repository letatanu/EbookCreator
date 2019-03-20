from bs4 import BeautifulSoup as BS
import urllib.request as reader

class HTMLParser():
    def __init__(self, link, chapter):
        self.link = link
        self.chapter = chapter
        self.endOfBook = False
        try:
            response = reader.urlopen(self.link+str(self.chapter))
            content = response.read().decode("utf8")
            data = BS(content, "html.parser").find_all(name="div", attrs={"class": "chapter-c"})
            self.metaData = ""
            self.chapterTitle = "No Title"
            if len(data) > 0:
                self.metaData = str(data[0])
                data1 = BS(content, "html.parser").find_all(name="a", attrs={"class": "chapter-title"})
                if len(data1) > 0:
                    self.chapterTitle = "Chương " + str(data1[0].contents[-1])
                # print(self.metaData)
            eOB = BS(content, "html.parser").find_all(name="a", attrs={"class":"btn btn-success disabled",
                                                                       "id": "next_chap"})
            if len(eOB) > 0:
                self.endOfBook = True
            else:
                self.endOfBook = False
        except:
            self.endOfBook = True
            print("Cannot read content from URL")





