from flask import Flask, render_template, jsonify
import json


app = Flask(
    __name__,
    template_folder="../client",  # Set template folder to 'client'
    static_folder="../client"  # Set static folder to 'client'
)

# Load network data
with open('network_data.json') as f:
    network_data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify(network_data)

if __name__ == "__main__":
    app.run(debug=True)
