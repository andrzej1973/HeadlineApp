# get apiKey from https://newsapi.org/bbc-news-api
# install requests library with following command executed in terminal window: pip3 install requests
# use postman to first test rest calls and return info structures
# install Flask web framework with following command executed in the terminal window: pip3 install Flask

#if you can run this code from PyCharm but not from cli then check the following:
# ~/.bash_profile has to have following line:
#       export PATH="/usr/local/opt/python/libexec/bin:$PATH
#force use of correct python version in this file as well by typing !/usr/bin/python3.6 instead of !/usr/bin/python
#

#!/usr/bin/python3.6
import sys
import os
import requests
import time
from flask import Flask,jsonify,request,render_template

def runEnvDebug():
    json_output_directory=jsonify(str({
                                   'Status':'OK',
                                   'Python_Interpreter_Path':str(sys.executable),
                                   'Python_Current_Working_Directory':str(os.getcwd()),
                                   'Python_Modules_Search_Paths':str(sys.path),

                                   }))
    return json_output_directory

headline_source_url = \
    "https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=c1d31a5c72db4917aae853111bdb0bf5"

app=Flask(__name__)

#@ signifies a decorator - way to wrap a function and modifying its behaviour
@app.route('/',methods=['GET'])
@app.route('/index.html',methods=['GET'])
@app.route('/index.htm',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/bbc_headlines_html',methods=['GET'])
def bbc_headlines_html():
    headlines_html=str(getLatestBBCHealines_html(headline_source_url))
    return render_template("headlines.html",headlines=headlines_html)

@app.route('/bbc_headlines_json',methods=['GET'])
def bbc_headlines_json():
    return getLatestBBCHealines_json(headline_source_url)


@app.route('/user/<user_name>',methods=['GET'])
def env_debugging(user_name):
        print("env_debugging started")
        if (user_name == 'admin'):
            return runEnvDebug()
        else:
            return jsonify(str({'Status','NOK'}))

def getLatestBBCHealines_html(url):

    currenttime = time.strftime("%Y-%m-%d @ %H:%M:%S", time.gmtime())
    file=open("LatestNewsFromBBC","w")

    response=requests.get(url)
    response_json=response.json()

    parent=response_json["articles"]

    headline_summary = ""
    header='\n' + "BBC Top stories from: " + currenttime + '\n'
    headline_summary = '<h2>'+ header + '</h2>' + '\n'

    file.write(header)

    headline_summary=headline_summary + '<p>' + '\n'
    for item in parent:
        headline=item["title"] + item["url"]
        headline_summary=headline_summary + '<a href="' + item["url"] + '">' + item["title"] + '<br></a>\n'
        file.write(headline + '\n')
    headline_summary = headline_summary + '</p>'

    file.close()
    print (headline_summary)
    return headline_summary


def getLatestBBCHealines_json(url):
    response = requests.get(url)
    response_json=response.json()
    response_json["source"]='CallBBCRestAPI'
    return str(response_json)

if __name__=="__main__":
    app.run(debug=True,port=8080)

main()


