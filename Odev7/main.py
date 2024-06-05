from flask import Flask, render_template, jsonify, url_for
from plots import generate_plot

app = Flask(__name__)

@app.route('/')
def index():
    generate_plot()
    return render_template('index.html')

@app.route('/generate_plot', methods=['GET'])
def plot():
    generate_plot()
    return jsonify(new_image_url=url_for('static', filename='images/plot.jpg'))

if __name__ == '__main__':
    app.run(debug=True)
