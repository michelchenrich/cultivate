"""
Cultivate - cultivate.py
Apache License (c) 2015
https://github.com/codenameyau/cultivate
"""
from tatoeba import scraper
import argparse

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Select languages and sentences')
    parser.add_argument('-l', default='deu', help='language to learn')
    parser.add_argument('-t', default='eng', help='translated language')
    parser.add_argument('-w', default='arbeit', help='word to learn')
    args = parser.parse_args()

    # Setup scraper for tatoeba
    scrape = scraper.TatoebaScraper()
    scrape.set_languages(args.l, args.t)
    scrape.set_word(args.w)
    results = []

    # Retrieve sentences for word
    results += scrape.get_sentences()

    for data in results:
        # Print sentence id
        lines = '-'*30

        # Print original sentence
        print lines
        print data['original']['sentence']
        print lines

        # Print translation
        if args.t in data['translations']:
            print "\n%s" % data['translations'][args.t]['sentence']
        else:
            print "\nTranslation for '%s' is not available." % args.t
        print ""

if __name__ == '__main__':
    main()
