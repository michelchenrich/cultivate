import requests
import bs4

class TatoebaScraper:
    def __init__(self, word_to_learn, original_language, translated_language):
        self.word_to_learn = word_to_learn
        self.language_translated = translated_language
        self.language_original = original_language
        self.site_base = 'https://tatoeba.org/eng/sentences/search?query={word}&from={original}&to={translated}&orphans=no&unapproved=no&user=&tags=&list=&has_audio=&trans_filter=limit&trans_to=eng&trans_link=&trans_user=&trans_orphan=&trans_unapproved=no&trans_has_audio=&sort=words'

    def get_sentences(self):
        return self.scrape_sentences(requests.get(self.site_url()))

    def site_url(self):
        return self.site_base.format(word=self.word_to_learn, original=self.language_original, translated=self.language_translated)

    def scrape_sentences(self, response):
        sentences = []
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content)
            divs = soup.find_all('div', class_='sentence-and-translations')
            for div in divs:
                sentences.append({
                        'text': self.get_original_sentence(div),
                        'translation': self.get_translation(div)
                        })
        return sentences

    def get_original_sentence(self, sentence_div):
        div = sentence_div.find('div', class_='sentence').find('div', class_='text')

        sentence_text = ''
        for part in div:
            sentence_text += part.string
        sentence_text = sentence_text.strip()

        return sentence_text 

    def get_translation(self, sentence_div):
        translations = sentence_div.find_all('div', class_='translation')
        for translation in translations:
            flag = translation.find('img')
            if flag.attrs['alt'] == self.language_translated:
                return translation.find('div', class_='text').string.strip()
