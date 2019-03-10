"""
Cultivate - scraper.py
Apache License (c) 2015
https://github.com/codenameyau/cultivate
"""
import requests
import bs4

class TatoebaScraper:

    def __init__(self):
        # Define language settings
        self.language_original = 'deu'
        self.language_translated = 'eng'
        self.supported_languages = (
                'cmn',  # Chinese
                'deu',  # German
                'eng',  # English
                'fin',  # Finnish
                'fra',  # French
                'ita',  # Italian
                'jpn',  # Japanese
                'kor',  # Korean
                'pol',  # Polish
                'por',  # Portuguese
                'rus',  # Russian
                'spa',  # Spanish
                )

        # Define site path to scrape random sentence
        self.site_base = 'https://tatoeba.org/eng/sentences/search?query={word}&from={original}&to={translated}&orphans=no&unapproved=no&user=&tags=&list=&has_audio=&trans_filter=limit&trans_to=eng&trans_link=&trans_user=&trans_orphan=&trans_unapproved=no&trans_has_audio=&sort=words'
        self.sentences = []

    ##################
    # Public Methods #
    ##################
    def set_languages(self, original, translated):
        if translated in self.supported_languages and original in self.supported_languages:
            self.language_translated = translated
            self.language_original = original

    def set_word(self, word_to_learn):
        self.word_to_learn = word_to_learn

    def get_sentences(self):
        return self.scrape_sentences(requests.get(self.site_url()))

    ####################
    # Internal Methods #
    ####################
    def site_url(self):
        return self.site_base.format(word=self.word_to_learn, original=self.language_original, translated=self.language_translated)

    def scrape_sentences(self, res):
        sentences = []
        if res.status_code == 200:
            soup = bs4.BeautifulSoup(res.content)
            divs = soup.find_all('div', class_='sentence-and-translations')
            for div in divs:
                sentece = {}
                self._find_original_sentence(div, sentece)
                self._find_translations(div, sentece)
                sentences.append(sentece)
        return sentences

    def _find_original_sentence(self, sentence_div, data):
        div = sentence_div.find('div', class_='sentence').find('div', class_='text')

        sentence_text = ''
        for part in div:
            sentence_text += part.string
        sentence_text = sentence_text.strip()

        data['original'] = {}
        data['original']['sentence'] = sentence_text 


    def _find_translations(self, sentence_div, data):
        data['translations'] = {}

        translations = sentence_div.find_all('div', class_='translation')
        for translation in translations:
            flag = translation.find('img')
            data['translations'][flag.attrs['alt']] = {
                    'sentence': translation.find('div', class_='text').string.strip(),
                    'language': flag.attrs['title']
                    }
