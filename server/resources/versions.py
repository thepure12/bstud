from bottle_suite import Resource

VERSIONS = {
    "versions": [
        "ESV",
        "NIV",
        "CSB",
        "KVJ",
        "NKJV"
    ]
}

class Version(Resource):

    def options(self):
        pass

    def get(self):
        return VERSIONS
    