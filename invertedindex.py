from appearance import Appearance
import re
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')

class InvertedIndex:
    def __init__(self, db):
        self.index = dict()
        self.db = db
    def __repr__(self):
        return str(self.index)
        
    def index_document(self, document):
        clean_text = re.sub(r'[^\w\s]','', document['text'])
        terms = word_tokenize(clean_text)
        tokens_without_sw = [
            word for word in terms if not word in stopwords.words()]

        #tokens_without_sw = clean_text.split(' ')
        appearances_dict = dict()

        for term in tokens_without_sw:
            term = term.lower()
            term_frequency = appearances_dict[term].frequency if term in appearances_dict else 0
            appearances_dict[term] = Appearance(document['id'], term_frequency + 1)
            
        update_dict = { key: [appearance]
                       if key not in self.index
                       else self.index[key] + [appearance]
                       for (key, appearance) in appearances_dict.items() }
        self.index.update(update_dict)
        self.db.add(document)
        return document
    
    def lookup_query(self, query):
        return { term: self.index[term] for term in query.split(' ') if term in self.index }

    def get_data_frame(self):
        data_list = dict()
        for index, term in self.index.items():
            if not index or not term:
                continue

            data_list[index] = term[0].frequency
        data_list = dict(sorted(data_list.items(), key=lambda item: item[1]))
        return data_list
