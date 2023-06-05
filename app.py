from flask import Flask,render_template,request,redirect,url_for,Response,jsonify
import json
from pyecharts import options as opts
from pyecharts.charts import Tree
app = Flask(__name__)

#pyecharts渲染网站初始化
init_opts=opts.InitOpts(width="2500px",height="1000px",page_title="合成路线全展示")

@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")
@app.route('/statistics')
def get_statistics():
    return render_template("statistics.html")
@app.route('/search')
def search_math():
    return render_template("search.html")

@app.route('/contact')
def get_contact():
    return render_template("contact.html")
@app.route('/allocation')
def get_allocation():
    return render_template("map.html")

@app.route('/find1', methods=['GET', 'POST'])
def find1():
    with open('nihao.txt', 'w') as file:
        file.write(str(request.args['message']))
    if request.args['message'] is None:
        return "none"
    else:
        global mathname
        smiles = None
        mathname = request.args['message']
        with open('nihao.txt','w') as file:
            file.write(str(request.args['message']))
        return redirect(url_for('findmathematician'))



@app.route('/findmathematician')
def findmathematician():
    if mathname =='':
        return render_template("kong.html")


    else:
        result = None
        colors = ['#FFAE57', '#FF7853', '#EA5151', '#CC3F57', '#9A2555']
        with open('static/relation.json', 'r', encoding='utf-8') as f:
            content = json.loads(f.read())
            for math in content:
                if re.search(mathname, math['name']) is not None:
                    result = math
                    break
        if result is None:
            return render_template("notfind.html")
        else:
            return render_template("charts.html")

import random
import re
@app.route('/getroute')
def getroute():
    result=None
    colors=['#FFAE57', '#FF7853', '#EA5151', '#CC3F57', '#9A2555']
    with open('static/relation.json','r',encoding='utf-8') as f:
        content=json.loads(f.read())
        for math in content:
            if re.search(mathname,math['name']) is not None:
               result=math
               break
    result["itemStyle"]={
      "color":random.sample(colors,1)[0]
    }
    result=[result]
    return jsonify(result)


if __name__ == '__main__':
    app.run(port=5004)
