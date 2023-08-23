import requests
import bs4
import re
import toml
import os

try:
    config = toml.load("config.toml")
    URL = config["gateway_url"]
except:
    URL = os.environ.get("GATEWAT_URL")


class PassageSoup(bs4.BeautifulSoup):
    def __init__(self, markup, **kwargs) -> None:
        super().__init__(markup, **kwargs)
        self.query = "; ".join(
            [e.text for e in self.find_all("div", {"class": "bcv"})]
        ).strip()
        self.copyright = self.find("div", {"class": "copyright-table"}).text.strip()
        self.chapter_nums = self.find_all("span", {"class": "chapternum"})
        self.full_chapter_link = self.find("a", {"class": "full-chap-link"})

        # Mogrify
        self.replaceChapterNums()
        self.removeFullChapterLink()
        self.removeDropDowns()
        self.removeTranslation()

    def replaceChapterNums(self):
        for chapter_num in self.chapter_nums:
            chapter_num.replace_with("1 ")

    def removeFullChapterLink(self):
        if self.full_chapter_link:
            self.full_chapter_link.decompose()

    def removeDropDowns(self):
        for dropdowns in self.find_all("div", {"class": "dropdowns"}):
            dropdowns.decompose()

    def removeTranslation(self):
        for translations in self.find_all("div", {"class": "translation"}):
            translations.decompose()

    def removeChapterRefs(self):
        for chapter_ref in self.find_all("div", {"class": "bcv"}):
            chapter_ref.decompose()

    def removeHeadings(self):
        for heading in self.find_all("h3"):
            heading.decompose()

    def removeFootnotes(self):
        footnotes = self.find("div", {"class": "footnotes"})
        if footnotes:
            footnotes.decompose()
        for footnote in self.find_all("sup", {"class": "footnote"}):
            if footnote:
                footnote.decompose()

    def removeCrossRefs(self):
        cross_refs = self.find("div", {"class": "crossrefs"})
        if cross_refs:
            cross_refs.decompose()
        for cross_reff in self.find_all("sup", {"class": "crossreference"}):
            if cross_reff:
                cross_reff.decompose()

    @property
    def text(self):
        passage_html = self.find_all("div", {"class": "passage-col"})
        passage_text = "\n".join([e.text for e in passage_html]).strip()
        text = f"{passage_text}\n\n{self.copyright}"
        text = re.sub(r"\n{4,}", "\n", text)
        return text.replace("Footnotes", "Footnotes\n").replace(
            "Cross references", "Cross references\n"
        )

    def serialize(self):
        return {"query": self.query, "passages": [self.text]}


def getText(
    search,
    version,
    headings=False,
    footnotes=False,
    chapter_refs=True,
    cross_refs=False,
):
    res = requests.get(URL.format(search=search, version=version))
    soup = PassageSoup(res.content, features="html.parser")
    if not headings:
        soup.removeHeadings()
    if not footnotes:
        soup.removeFootnotes()
    if not chapter_refs:
        soup.removeChapterRefs()
    if not cross_refs:
        soup.removeCrossRefs()
    return soup.serialize()


if __name__ == "__main__":
    text = getText("Romans 12-13", "NKJV")
    print(text)
