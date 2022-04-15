from flask import Flask, request, jsonify, render_template
import json
import sys
import interpreter as fbi #FunzoBunzo Interpreter
import logging


app = Flask(__name__, static_folder='static', static_url_path='')


@app.route("/")
def index():
    return render_template("index.html")

logging.basicConfig(level=logging.DEBUG)

@app.route("/api/compute", methods=['POST'])
def compute():
    try:
        output = fbi.execute(request.json, request.args)
        return jsonify({"result" : output})
    except Exception as err:
        return jsonify({"error" : err.__str__()})