from flask import Flask, render_template, jsonify
import json


app = Flask(
    __name__,
    template_folder="../client",  # Set template folder to 'client'
    static_folder="../client"  # Set static folder to 'client'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    with open('../assets/network_data.json') as f:
        network_data = json.load(f)
    return jsonify(network_data)

@app.route('/stat')
def stat():
    with open('../assets/statistics.json') as f:
        statistics = json.load(f)
    return jsonify(statistics)

if __name__ == "__main__":
    app.run(debug=True)
