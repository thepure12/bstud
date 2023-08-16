try:
    from gevent import monkey
except:
    pass
monkey.patch_all()
from bottle_suite import BottleSuite
from bottle import static_file
import os

prod = os.environ.get("BSTUD_PROD")

app = BottleSuite()


@app.get(["/", "/<page>"])
def index(page=None):
    return static_file("index.html", root="../client/dist")


@app.get(["/_nuxt/<filename>"])
def nuxt(filename):
    return static_file(filename, f"../client/dist/_nuxt")

if prod:
    application = app
else:
    app.run(port=8000, server="gevent")
