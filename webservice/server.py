# import flask
#
#
# app = flask.Flask(__name__)
# # app.config["DEBUG"] = True
#
#
# # @app.route('/', methods=['GET'])
# # def home():
# #     return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
#
# @app.route("/")
# def main():
#     return "Welcome!"
#
# if __name__ == "__main__":
#     # app.run(host='18.188.28.205', port=80)
#     app.run(host='0.0.0.0', port=80)
#     # app.run()

from time import sleep
from time import time

t = time()

print('{} karel'.format(time() - t))
# sleep(0.01)