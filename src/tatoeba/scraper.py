"""
Cultivate - scraper.py
Apache License (c) 2015
https://github.com/codenameyau/cultivate
"""
import requests
import bs4

class TatoebaScraper:

    def __init__(self):
        """
        Constructor: (String) -> TatoebaScraper
        Sets up the class data structures
        """
        # Define language settings
        self.language_original = 'jpn'
        self.language_translated = 'eng'
        self.supported_languages = (
            'eng',
            'jpn',
        )

        # Define site path to scrape
        self.site_url = 'http://tatoeba.org/eng/sentences/show/' + self.language_original
        self.sentences = []
        self.soup = None


    ##################
    # Public Methods #
    ##################
    def set_languages(self, language_translated, language_original):
        """
        Public: (String, String) -> None
        Sets the languages for the scraper
        """
        if language_translated in self.supported_languages \
            and language_original in self.supported_languages:
            self.language_translated = language_translated
            self.language_original = language_original

    def set_url(self, specified_url):
        """
        Public: (String) -> None
        Sets the site_url to specified url
        """
        self.site_url = specified_url

    def get_random_sentences(self, count):
        """
        Public: None -> String
        Scrapes the site and finds target article
        """
        self.sentences = []
        for i in range(0, count):
            res = requests.get(self.site_url)
            if res.status_code == 200:
                data = {}
                self.soup = bs4.BeautifulSoup(res.content)
                self._find_sentence_id(data)
                self._find_original_sentence(data)
                self._find_translations(data)
                self.sentences.append(data)
        return self.sentences

    ####################
    # Internal Methods #
    ####################
    def _find_sentence_id(self, data):
        """
        Internal: None -> None
        Stores the sentence id into data
        """
        data['sentence_id'] = self.soup.find(id='SentenceSentenceId').attrs['value']

    def _find_original_sentence(self, data):
        """
        Internal: None -> None
        Stores the main sentence into data
        """
        div = self.soup.find('div', class_='mainSentence')
        data['original'] = {
            'sentence': div.find('div', class_='text').string,
            'romanization': div.find('div', class_='romanization').attrs['title']
        }

    def _find_translations(self, data):
        """
        Internal: None -> None
        Finds all additional translations and store in data
        """
        # [TODO]: Add romanization in data
        data['translations'] = {}

        # Scrape alt flag name and translation text
        div = self.soup.find('div', class_='translations')
        translations = div.find_all('a', class_='text')
        flags = div.find_all('img', class_='languageFlag')
        for i in range(0, len(translations)):
            lang_short = flags[i].attrs['alt']
            data['translations'][lang_short] = {
                'sentence': translations[i].string,
                'language': flags[i].attrs['title'],
            }