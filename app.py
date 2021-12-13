import configparser
import json
import webbrowser

import flask

from DatabaseReader import DatabaseReader


config = None
dbreader = None


app = flask.Flask(__name__, static_url_path="/static")

@app.route("/api/get_scholars")
def getScholars():
    global dbreader
    return flask.jsonify(dbreader.getScholars())

@app.route("/api/update_scholars", methods=["POST"])
def updateScholars():
    global dbreader
    updateVal = [flask.request.get_json()]
    dbreader.updateScholars(updateVal)
    return flask.jsonify(dbreader.getScholars())

@app.route("/api/shutdown_server")
def shutdownServer():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "Server Shutdown!"
        

if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read("config.ini")
    dbreader = DatabaseReader(config["DEFAULT"]["DATABASE_FILE"])
    dbreader.createDatabaseTables()
    webbrowser.open("http://127.0.0.1:8888/static/index.html")
    app.run("127.0.0.1", 8888, debug=True)