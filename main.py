from flask import Flask, request
import requests
import json
from bs4 import BeautifulSoup
import sys
import io

app = Flask(__name__)

def getNews(page):
    try:
        res = requests.get(f'https://www.ifsudestemg.edu.br/noticias/barbacena/?b_start:int={int(page)*20}')
        soup = BeautifulSoup(res.text, 'html.parser')
        # print(soup.prettify())

        titles = soup.find_all("a", {"class": "summary url"})
        descriptions = soup.find_all("span", {"class": "description"})



        json = {
            "noticias": []
        }

        for noticia in range(len(titles)):
            json["noticias"].append({
                "titulo": titles[noticia].contents[0],
                "descricao" : descriptions[noticia].contents[0]
            })
        
        return json
    except:
        return False

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api():
    if request.method == 'GET':
        return json.dumps(
            {
                "payload": "API rodando com sucesso!",
                "status": 200
            }
        )

@app.route('/noticias/<pagina>', methods=['GET'])
def noticias(pagina):
    if request.method == 'GET':
        response = getNews(pagina)
        if response == False:
            return json.dumps({
                "status": 400,
                "mensagem": "Página inválida"
            })
        else:
            return json.dumps(
                {
                    "payload": getNews(pagina),
                    "status": 200
                }
            )

if __name__ == '__main__':
    app.run(debug=True)