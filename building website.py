# project: p4
# submitter: kenigsztein
# partner: none
# hours: 20
# data source: https://www.kaggle.com/spscientist/students-performance-in-exams


import pandas as pd
from flask import Flask, request, jsonify, Response
import re
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
import time
import requests
from IPython.core.display import Image
from multiprocessing import Process
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


app = Flask(__name__)
counts_dict = {"A": 0, "B":0}
home_visits = 0
@app.route('/')

def home():
    global home_visits
    with open("index.html") as f:
        html = f.read()
    if home_visits>=10:
        if counts_dict["A"] > counts_dict["B"]:
            new_html = html.replace("donate should be here", '</p><a href="donate.html?from=A">donate</a></p>')
        elif counts_dict["A"] < counts_dict["B"]:
            new_html = html.replace("donate should be here", '</p><a href="donate.html?from=B">DONATE</a></p>')
    else:         
        home_visits += 1
        if home_visits%2 == 0:           
            new_html = html.replace("donate should be here", '</p><a href="donate.html?from=A">donate</a></p>')
        else:          
            new_html = html.replace("donate should be here", '</p><a href="donate.html?from=B">DONATE</a></p>')
    return new_html
   
    
@app.route('/browse.html')
def browse_handler():
    df = pd.read_csv("main.csv")
    return "<html><body><h1>Browse</h1><p>{}</p></body></html>".format(df.to_html())

n = 0
@app.route('/email', methods=["POST"])
def email():
    global n
    email = str(request.data, "utf-8")
    if re.match(r"[^@]+@[^@]+\.[^@]+", email): # 1 regex adapted from: https://stackoverflow.com/questions/8022530/how-to-check-for-valid-email-address
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email + "\n") # 2
        n = n+1
        return jsonify(f"thanks, you're subscriber number {n}!")
    return jsonify("email is invalid") # 3


@app.route('/donate.html')
def donate():
    
    version = request.args.get("from")
    if version in counts_dict:
        counts_dict[version]+=1
    return "<html><body><h1>DONATE</h1><p>Hello, please donate to help the students achieve their dreams and get into good schools, they need good grades to do so!</p></body></html>"

@app.route("/robots.txt")
def robots ():
    no_browse="hungrycaterpillar"
    yes_browse ="busyspider"


    html=f"""
    user-agent: {no_browse}
    not: /browse.html
    
    user-agent: {yes_browse}
    not: /
    """
    return Response(html, headers={"Content-Type": "text/plain"}, status = 200)
    

@app.route('/math.svg')
def math():
    dfs = pd.read_csv("main.csv")
    dfs = dfs.astype({'math score':int})
    
    try:
        test = request.args['gender']
    except Exception as ex:
        test = "All"
    if test == "All":
        dfs["bigger_70"] = np.where(dfs["math score"] >= 70,1,0)
        value = dfs["bigger_70"].value_counts()
    else:
        dfs = dfs[dfs["gender"] == test]
        dfs["bigger_70"] = np.where(dfs["math score"] >= 70,1,0)
        value = dfs["bigger_70"].value_counts()
    fig, ax = plt.subplots()
    value.plot.bar(ax=ax)
    
    ax.set_xticklabels(["70 or Greater Scores", "Less Than 70 Scores"])
    ax.set_xlabel("Math Scores")
    ax.set_ylabel(f"Grade Range Frequency")
    fake= BytesIO()
    ax.get_figure().savefig(fake, format='svg', bbox_inches = 'tight')
    return Response(fake.getvalue(), headers = {"Content-Type": "image/svg+xml"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.
