import argparse

from flask import Flask, request

app = Flask(__name__)


@app.route("/test", methods=['POST'])
def test():
    data = request.get_json()
    print("Received {}".format(data))
    return ""


if __name__ == "__main__":
    app.run()
