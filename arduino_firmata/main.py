from pyfirmata import Arduino
from time import sleep

# creating python server
from flask import Flask, render_template

# creating flask object
app = Flask(__name__)


# homepage route
@app.route('/')
def home():
    render_template('index.html')


board = Arduino('COM3')

pin13 = board.get_pin('d:13:o')

while True:
    pin13.write(1)
    sleep(1)
    pin13.write(0)
    sleep(1)
