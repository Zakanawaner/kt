from airium import Airium
import json

d = Airium()


class CardGenerator:
    def __init__(self, doc):
        doc('<!DOCTYPE html>')
        with doc.html(id='html', lang='en'):
            with doc.head():
                doc.link(type="text/css",
                         rel="stylesheet",
                         href="{{ url_for('static', filename='stylesheets/cardGenerator.css') }}")
                doc.meta(charset="UTF-8")
                doc.title(_t="Your Kill Team Cards")
        self.generatorData = json.load(open("../hard/data.json"))['cardGenerator']
        self.doc = doc

    def addCard(self, faction, title=None, ab1=None, ab2=None, titlePic=None,
                stats=None, weapons=None, ab=None, abOp=None, backImg=None):
        class Fact:
            shortName = 'void-dancertroupe'
        faction = Fact()
        border = self.generatorData[faction.shortName]['card-border']
        background = self.generatorData[faction.shortName]['card-background']
        titleBackground = self.generatorData[faction.shortName]['title-background']
        with self.doc.html(id='html', lang='en'):
            with self.doc.body():
                with self.doc.div(klass="card", style="border-image: ?; background: ?;".format(border, background)):
                    with self.doc.div(klass="header"):
                        with self.doc.div(klass="title", style="background: ?;".format(titleBackground)):
                            with self.doc.div(klass="name-ability"):
                                self.doc.p(klass="stat-name", _t=title if title else "")
                            with self.doc.div(klass="type-ability"):
                                self.doc.p(klass="type-name", _t=ab1 if ab1 else "")
                            with self.doc.div(klass="type-ability"):
                                self.doc.p(klass="type-name", _t=ab2 if ab2 else "")
                        if titlePic:
                            self.doc.div(klass="picture", style="background-image: url(?);".format(titlePic))


cardGenerator = CardGenerator(d)
cardGenerator.addCard("ff", "hola")
f = cardGenerator.doc.html
f = 0
