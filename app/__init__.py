from __future__ import print_function
from flask import Flask, jsonify, render_template
from flask import url_for, escape
import json


app = Flask(__name__, instance_relative_config=True)
dataPath='test/song.json'
with open(dataPath) as f:
    test_data = json.load(f)

@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    """load home template"""
    return render_template('home.html')


@app.route('/allData')
def allData():
    '''
    arg: None
    return: the entire json data we loaded
    '''
    return jsonify(test_data)

@app.route('/renderAllData',methods = ['POST','GET'])
def renderAllData():
    '''
    arg: None
    return: a rendered html using the entire json data
    '''
    ### problem right now: the html page is not being rendered while no error is incurred ###
    dataPath='test/song.json'
    with open(dataPath) as f:
        test_data = json.load(f)
    return render_template('visualizeData.html',data=test_data)

@app.route('/user/<name>')
def user_page(name):
    return "User: %s" % escape(name)

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name="Haosong"))
    print(url_for('user_page', name="Zishi"))
    print(url_for("test_url_for"))
    print(url_for('test_url_for',num=2))
    return "Test page"


# will move to utils later
# def parse_song_data(data):
#     for artist in data:
#         print(artist,file=sys.stderr)


if __name__ == '__main__':
    app.run(debug=True)
    
