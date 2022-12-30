from flask import Flask
import requests
from flask_cors import CORS
from tweets import getTwetsOffAllNotices

app = Flask('__name__')
app.config['JSON_AS_ASCII'] = False

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

cache = {}

def getTweetsOfNews(news):
  return getTwetsOffAllNotices(news)


@app.route('/api/noticias/<categoria>')
def noticias(categoria):
  try:
    if categoria in cache:
      return cache[categoria]
    else:
      response = requests.get(f'http://api.mediastack.com/v1/news?access_key=5b420db782079931d5d5f1c69c24d24a&categories={categoria}&languages=pt')
      data = response.json()
      news = getTweetsOfNews(data['data'])
      cache[categoria] = news
      return news
  except requests.exceptions.RequestException as e: 
    return e


app.config['DEBUG'] = True
app.run()