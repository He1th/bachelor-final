import calendar
import os
import time
import uuid
from datetime import datetime

import jsonpickle
from flask import Flask, jsonify, Response, request
from Code.Article import Article
from Code.ArticleProfiler import ArticleProfiler
from Code.SqlHandler import SqlHandler
from Code.MatchingAlgorithm import MatchingAlgorithm
from Code.User import User
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

app.config['Access-Control-Allow-Origin'] = '*'

profiler = ArticleProfiler()
matcher = MatchingAlgorithm()


@app.route('/')
def welcome():
    # return a json
    return jsonify({'status': 'api working'})


@app.route('/recommended/<user_id>')
def getRecommended(user_id=1):
    sh = SqlHandler()

    user = sh.retrieveUser(user_id)
    user.recommendedArticles = {}
    params = sh.retrieveParameters()
    latestArticles = sh.retrieveLatestArticles(params[9])

    recommended = []

    if len(user.readArticles) > 2:
        for a in latestArticles:
            matcher.calculateRelevanceScore(a, user)

        user.sortRecommendedArticles()


        for i in range(0, 10):
            article_id = list(user.recommendedArticles)[i]
            recommended.append(sh.retrieveArticle(article_id))
        recommendedArticles = recommended
    else:
        recommendedArticles = latestArticles[:10]

    sh.insertUser(user)

    sqlResponse = jsonpickle.encode(recommendedArticles)
    backendResponse = Response(response=sqlResponse,
                               status=200,
                               mimetype="application/json")
    backendResponse.headers["Content-Type"] = "application/json; charset=utf-8"
    backendResponse.headers["Access-Control-Allow-Origin"] = "*"

    return backendResponse

@app.route('/article/<article_id>')
def getSingleArticle(article_id):
    sh = SqlHandler()
    article = sh.retrieveArticle(str(article_id))
    sqlResponse = jsonpickle.encode(article)
    backendResponse = Response(response=sqlResponse,
                               status=200,
                               mimetype="application/json")
    backendResponse.headers["Content-Type"] = "application/json; charset=utf-8"
    backendResponse.headers["Access-Control-Allow-Origin"] = "*"
    return backendResponse

@app.route('/latest')
def getLatest():
    sh = SqlHandler()
    params = sh.retrieveParameters()
    rv = sh.retrieveLatestArticles(params[8])

    sqlResponse = jsonpickle.encode(rv)
    backendResponse = Response(response=sqlResponse,
                               status=200,
                               mimetype="application/json")
    backendResponse.headers["Content-Type"] = "application/json; charset=utf-8"
    backendResponse.headers["Access-Control-Allow-Origin"] = "*"

    return backendResponse


@app.route('/article/<article_id>/<user_id>')
def getArticle(article_id, user_id):
    sh = SqlHandler()
    user = sh.retrieveUser(user_id)
    article = sh.retrieveArticle(article_id)

    user.addReadArticle(article, sh)
    sh.insertUser(user)

    sqlResponse = jsonpickle.encode(article)
    backendResponse = Response(response=sqlResponse,
                               status=200,
                               mimetype="application/json")
    backendResponse.headers["Content-Type"] = "application/json; charset=utf-8"
    backendResponse.headers["Access-Control-Allow-Origin"] = "*"

    return backendResponse


@app.route('/randomArticle')
def randomArticle():
    sh = SqlHandler()
    rv = sh.retrieveRandomArticles()

    sqlResponse = jsonpickle.encode(rv)
    backendResponse = Response(response=sqlResponse,
                               status=200,
                               mimetype="application/json")
    backendResponse.headers["Content-Type"] = "application/json; charset=utf-8"
    backendResponse.headers["Access-Control-Allow-Origin"] = "*"

    return backendResponse


@app.route('/search/<searchTerm>')
def search(searchTerm = "test"):
    sh = SqlHandler()
    rv = sh.searchForArticles(searchTerm)

    sqlResponse = jsonpickle.encode(rv)
    backendResponse = Response(response=sqlResponse,
                               status=200,
                               mimetype="application/json")
    backendResponse.headers["Content-Type"] = "application/json; charset=utf-8"
    backendResponse.headers["Access-Control-Allow-Origin"] = "*"

    return backendResponse


@app.route('/prepare')
def profileArticle():
    sh = SqlHandler()
    articleList = sh.retrieveAllArticles()
    print("Filtering Nouns")
    for a in articleList:
        profiler.filterNouns(a)

    print("Ranking Nouns")
    for a in articleList:
        profiler.rankNouns(a, articleList)

    sh.establishConnection()
    for a in articleList:
        sh.insertArticle(a)

    articleList.clear()
    return jsonify({"Database": "Prepared"})


@app.route('/createUser')
def createTestUser():
    sh = SqlHandler()

    user = User(1)
    sh.insertUser(user)

    return jsonify({"Test user 2": "Created"})

@app.route('/admin/createUser/<username>')
def createTestUserByUsername(username):
    sh = SqlHandler()

    user = User(username)
    sh.insertUser(user)

    return jsonify({"Test user " + username: "Created"})


@app.route('/connect')
def connect():
    sh = SqlHandler()
    sh.establishConnection()
    return jsonify({"Reestablished": "Connection"})


@app.route('/read/<user_id>')
def getReadArticles(user_id):
    sh = SqlHandler()
    user = sh.retrieveUser(user_id)

    readArticles = []
    for aid in user.readArticles:
        readArticles.append(sh.retrieveArticle(aid).headline)

    print(user.nounScore)

    sqlResponse = jsonpickle.encode(readArticles)
    backendResponse = Response(response=sqlResponse,
                               status=200,
                               mimetype="application/json")
    backendResponse.headers["Content-Type"] = "application/json; charset=utf-8"
    backendResponse.headers["Access-Control-Allow-Origin"] = "*"

    return backendResponse


@app.route('/createRandomUser')
def createRandomUser():
    user = User(2)

    sh = SqlHandler()
    alist = sh.retrieveRandomArticles(5)

    for a in alist:
        user.addReadArticle(a, sh)

    sh.insertUser(user)

    return jsonify({"Test user": "Created"})

@app.route('/repopulate')
def repopulateDatabase():
    sh = SqlHandler()
    sh.populateDatabase()

    return jsonify({"Database": "repopulated"})

@app.route('/admin/create-article', methods = ['POST'])
@cross_origin(supports_credentials=True)
def createArticle():
    sh = SqlHandler()

    headline = request.form['headline']
    excerpt = request.form['excerpt']
    author = request.form['author']
    text = request.form['text']

    article = Article(str(uuid.uuid1()), str(calendar.timegm(time.gmtime())), author, headline, excerpt, text)

    profiler.filterNouns(article)
    articleList = sh.retrieveAllArticles()
    profiler.rankNouns(article, articleList)

    sh.insertArticle(article)

    response = jsonify(message="Simple server is running")

    # Enable Access-Control-Allow-Origin
    return response

@app.route('/admin/setParameters', methods=['POST'])
@cross_origin(supports_credentials=True)
def setParameter():
    sh = SqlHandler()

    hl = request.form['headline']
    ex = request.form['excerpt']
    tx = request.form['text']
    noun = request.form['noun']
    name = request.form['name']
    loc = request.form['location']
    org = request.form['organisation']
    latest = request.form['articles']
    latestRec = request.form['recommendedArticles']

    profiler.updateParameters(hl, ex, tx, noun, name, loc, org)
    sh.insertParameters(hl, ex, tx, noun, name, loc, org, latest, latestRec)

    params = (hl, ex, tx, noun, name, loc, org, latest, latestRec)

    return jsonify({"parameters updated": params})

@app.route('/admin/parameters')
def getParameters():
    sh = SqlHandler()

    params = sh.retrieveParameters()

    return jsonify(params)

@app.route('/admin/getUsers')
def getUserList():
    sh = SqlHandler()

    data = sh.retrieveAllUsers()

    return jsonify({"data": data})

@app.route('/admin/resetUser/<user_id>')
def resetUser(user_id):
    sh = SqlHandler()

    user = User(user_id)
    sh.insertUser(user)

    return jsonify({"user reset": user_id})




if __name__ == '__main__':
    #define the localhost ip and the port that is going to be used
    # in some future article, we are going to use an env variable instead a hardcoded port
    app.run(host='0.0.0.0', port=os.getenv('PORT'))
