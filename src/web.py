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

        scrape = scraper.TatoebaScraper()
        scrape.set_languages(arguments["source_language"], arguments["target_language"])
        scrape.set_word(arguments["word"])
        return scrape.get_sentences(), 200

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

app = Flask(__name__)
api = Api(app)
api.add_resource(Sentence, "/sentence")
app.run()
