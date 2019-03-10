import os
from unidecode import unidecode
from flask import Flask
from flask_restful import Api, Resource, reqparse
from tatoeba import scraper

class Sentence(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("word")
        parser.add_argument("source_language")
        parser.add_argument("target_language")
        arguments = parser.parse_args()

        tatoeba = scraper.TatoebaScraper(unidecode(arguments["word"]), arguments["source_language"], arguments["target_language"])
        return tatoeba.get_sentences(), 200

app = Flask(__name__)
api = Api(app)
api.add_resource(Sentence, "/sentence")
#app.run(port=os.environ['PORT'])
