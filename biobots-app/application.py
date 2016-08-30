import flask
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from predictor import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/predictor")
def predictor():
    return render_template('predictor.html')

@app.route("/explorer")
def explorer():
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    conn = sqlite3.connect('biodata.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute('select * from session_meta')
    results = cursor.fetchall()
    return render_template('explorer.html', rows = results)

@app.route("/predictor/get_prediction", methods=["GET"])
def get_prediction():
    cl_intensity = int(request.args.get('cl_intensity', '0'))
    cl_duration = int(request.args.get('cl_duration', '0'))
    extruder1 = float(request.args.get('extruder1', '0.0'))
    extruder2 = float(request.args.get('extruder2', '0.0'))
    layer_height = float(request.args.get('layer_height', '0.0'))
    layer_num = float(request.args.get('layer_num', '0.0'))
    wellplate = int(request.args.get('wellplate', '0'))
    cl_enabled = 'true'
    result = makePrediction(cl_duration, cl_enabled, cl_intensity, extruder1, extruder2, layer_height, layer_num, wellplate)
    return render_template('prediction.html',  result = result)

if __name__ == "__main__":
    app.run()



