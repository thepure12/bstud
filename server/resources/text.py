from bottle_suite import Resource
from bottle import static_file
import requests
from pyhtml2pdf import converter
import os
from string import Template
import re
import toml

config = toml.load("config.toml")
ESV_URL = config["esv_url"]
API_TOKEN = config["api_token"]
HEADERS = {"Authorization": f"Token {API_TOKEN}"}
PRINT_OPTIONS = {
    "landscape": True,
    "marginTop": 0.25,
    "marginBottom": 0.25,
    "marginLeft": 0.25,
    "marginRight": 0.25,
}


class PassageText(Resource):
    def _formatText(self, passages: list) -> str:
        text = "\n".join(passages)
        text = re.sub(r"\n +", "\n", text)
        text = re.sub(r" {2,}", " ", text)
        text = re.sub(r"\n{2,}", "\n", text)
        return text

    def get(self):
        res = requests.get(ESV_URL, headers=HEADERS, params=self.params)
        if "download" in self.params:
            html_path = os.path.abspath("worksheet.html")
            css_path = os.path.abspath("worksheet.css")
            with open(html_path) as tpl_file:
                tpl = Template(tpl_file.read())
            with open(css_path) as css_file:
                css = css_file.read()
            text = self._formatText(res.json()["passages"])
            worksheet_text = tpl.substitute(
                text=text, style=css, font_size=self.params.get("font-size") or 10
            )
            print("Converting")
            converter.convert(
                f"data:text/html;charset=utf-8,{worksheet_text}",
                "out.pdf",
                print_options=PRINT_OPTIONS,
            )
            print("Converted")
            filename = (
                f"{self.params.q}.pdf" if self.params.q else "bible_study_worksheet.pdf"
            )
            return static_file("out.pdf", "./", download=filename)
        return res.json()
