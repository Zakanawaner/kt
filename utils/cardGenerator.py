from domonic import html, head, link, meta, title, body, div, p
import json


class CardGenerator:
    def __init__(self):
        self.pages = 0
        self.cards = 0
        self.html = html(_lang='en')
        self.html.appendChild(head())
        self.html.head.appendChild(meta(_charset="UTF-8"))
        self.html.head.appendChild(title("Your Kill Team Cards"))
        self.html.head.appendChild(link(_type="text/css",
                                        _rel="stylesheet",
                                        _href="static/stylesheets/cardGenerator.css"))
        self.html.appendChild(body())
        self.addPage()
        self.generatorData = json.load(open("hard/data.json"))['cardGenerator']

    def addPage(self):
        self.html.body.appendChild(div(_class="page"))
        self.pages += 1
        self.cards = 0

    def addBackPage(self, faction):
        border = self.generatorData[faction.shortName]['card-back-border']
        background = self.generatorData[faction.shortName]['card-back-background']
        newPage = div(_class="page")
        for i in range(0, 8):
            newCard = div(_class="card-back", _style="border-image: {}; background: {};".format(border, background))
            newCard.appendChild(div(_class="back-image"))
            newPage.appendChild(newCard)
        self.html.body.appendChild(newPage)
        self.pages += 1
        self.cards = 0

    def addCard(self, faction, tit=None, ab1=None, ab2=None, titlePic=None,
                stats=None, weapons=None, ab=None, abOp=None, backImg=None):


        class Fact:
            shortName = 'void-dancertroupe'
        faction = Fact()



        border = self.generatorData[faction.shortName]['card-border']
        background = self.generatorData[faction.shortName]['card-background']
        titleBackground = self.generatorData[faction.shortName]['title-background']

        cardTitle = div(_class="title", _style="background: {};".format(titleBackground))
        cardTitle.appendChild(div(_class="name-ability").appendChild(p(tit if tit else "", _class="stat-name")))
        cardTitle.appendChild(div(_class="type-ability").appendChild(p(ab1 if ab1 else "", _class="type-name")))
        cardTitle.appendChild(div(_class="type-ability").appendChild(p(ab2 if ab2 else "", _class="type-name")))

        cardHeader = div(_class="header")
        cardHeader.appendChild(cardTitle)
        if titlePic:
            cardHeader.appendChild(div(_class="picture", _style="background-image: url({});".format(titlePic)))

        newCard = div(_class="card-front", _style="border-image: {}; background: {};".format(border, background))
        newCard.appendChild(cardHeader)
        if self.cards == 8:
            self.addBackPage(faction)
            self.addPage()
        self.html.body.lastChild.appendChild(newCard)
        self.cards += 1
