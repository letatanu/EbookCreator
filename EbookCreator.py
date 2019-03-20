from HTMLParser import *
import ebooklib as ebl
from ebooklib import epub
import numpy as np
import xml.etree.ElementTree as ET


class Ebook():
    def __init__(self, title="Phàm Nhân Tu Tiên 2", link="https://truyenfull.vn/pham-nhan-tu-tien-chi-tien-gioi-thien-pham-nhan-tu-tien-2/chuong-", ebookName=""):
        self.title = title
        self.link = link
        self.ebookName = ebookName

    def addMoreChapters(self, toChapter=0):
        if toChapter==0:
            toChapter = np.inf
        try:
            book = epub.read_epub("%s.epub"%self.ebookName)
            chapter = len(book.spine)
            toc = book.get_item_with_id("ncx")
            nav = book.get_item_with_id("nav")

            html = HTMLParser(link=self.link, chapter=chapter)
            if toChapter == 0:
                toChapter = np.inf
            # create chapters
            c = epub.EpubHtml(title=html.chapterTitle, file_name='chap_%d.xhtml' % chapter)
            c.set_content(u'<html><body><h1>%s</h1>%s</body></html>' % (html.chapterTitle, html.metaData))
            c.id = "chapter_%d"%(chapter-1)
            # adding chapter to the book
            book.toc.append(c)
            # modify toc and nav content
            newChapterTOC = "<navPoint id=\"chapter_%d\"><navLabel><text>%s​</text></navLabel><content src=\"chap_%d.xhtml\"/></navPoint></navMap>"% (chapter, html.chapterTitle, chapter)
            toc.content =  str(toc.content).replace("</navMap>", newChapterTOC)

            print("Chapter %d" % chapter)
            book.add_item(c)
            # basic spine
            book.spine.append(c)
            newNav = "<li><a href=\"chap_%d.xhtml\">%s​</a></li></ol>"%(chapter, html.chapterTitle)
            nav.content = str(nav.content).replace("</ol>", newNav)
            chapter = chapter + 1

            while (not html.endOfBook) and (chapter <= toChapter):
                html = HTMLParser(link=self.link, chapter=chapter)
                # create chapters
                c = epub.EpubHtml(title=html.chapterTitle, file_name='chap_%d.xhtml' % chapter)
                c.set_content(u'<html><body><h1>%s</h1>%s</body></html>' % (html.chapterTitle, html.metaData))
                c.id = "chapter_%d"%(chapter-1)

                # adding chapter to the book
                book.toc.append(c)
                newChapterTOC = "<navPoint id=\"chapter_%d\"><navLabel><text>%s​</text></navLabel><content src=\"chap_%d.xhtml\"/></navPoint></navMap>" % (
                chapter-1, html.chapterTitle, chapter)
                toc.content = str(toc.content).replace("</navMap>", newChapterTOC)

                print("Chapter %d" % chapter)
                book.add_item(c)
                # basic spine
                book.spine.append(c)
                newNav = "<li><a href=\"chap_%d.xhtml\">%s​</a></li></ol>" % (chapter, html.chapterTitle)
                nav.content = str(nav.content).replace("</ol>", newNav)

                chapter = chapter + 1

            epub.write_epub("%s_%d.epub" % (self.ebookName, toChapter), book)

        except:
            print("Cannot read Ebook")


    def createEbook(self, toChapter=0, fromChapter=1):
        book = epub.EpubBook()
        book.set_title(self.title)
        chapter = fromChapter
        book.spine = ['nav']
        # define CSS style
        style = 'BODY {color: white;}'
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

        # add CSS file
        book.add_item(nav_css)

        html = HTMLParser(link=self.link, chapter=chapter)
        if toChapter == 0:
            toChapter = np.inf
        # create chapters
        c = epub.EpubHtml(title=html.chapterTitle, file_name='chap_%d.xhtml' % chapter)
        c.set_content(u'<html><body><h1>%s</h1>%s</body></html>' % (html.chapterTitle, html.metaData))
        # adding chapter to the book
        book.toc.append(c)

        print("Chapter %d" % chapter)
        book.add_item(c)
        # basic spine
        book.spine.append(c)
        chapter = chapter + 1

        while(not html.endOfBook) and (chapter <= toChapter):
            html = HTMLParser(link=self.link, chapter=chapter)
            # create chapters
            c = epub.EpubHtml(title=html.chapterTitle, file_name='chap_%d.xhtml'%chapter)
            c.set_content(u'<html><body><h1>%s</h1>%s</body></html>' % (html.chapterTitle,html.metaData))
            #adding chapter to the book
            book.toc.append(c)

            print("Chapter %d"%chapter)
            book.add_item(c)
            # basic spine
            book.spine.append(c)
            chapter = chapter + 1

        # add default NCX and Nav file
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        epub.write_epub("%s_%d.epub" % (self.ebookName, toChapter), book)


def main():
    fromChapter = 1
    toChapter = 757
    ebookName = "PhamNhanTuTien2_1_0"
    title = "Phàm Nhân Tu Tiên 2"
    link = "https://truyenfull.vn/pham-nhan-tu-tien-chi-tien-gioi-thien-pham-nhan-tu-tien-2/chuong-"
    book = Ebook(title=title, link=link, ebookName=ebookName)
    # book.createEbook(toChapter=toChapter, fromChapter=fromChapter)
    book.addMoreChapters(toChapter=toChapter)

if __name__ == '__main__':
    main()



