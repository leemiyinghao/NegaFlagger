import jieba
import fasttext
import numpy
import fnv
from math import log

DF_DOC_COUNT = 2438173


def _hash(word):
    return fnv.hash(str.encode(word)) % 10000000


class Sentence2Vec(object):
    def __init__(self, embedding_path, dict_path, df_path, stopword_path):
        super().__init__()

        # loading fasttext model
        self.embedding = fasttext.load_model(embedding_path)

        # init jieba pos-tagger
        jieba.load_userdict(dict_path)

        # loading stopwords
        stopwords = ["\n"]
        with open(stopword_path, "r") as file:
            for word in file.readlines():
                stopwords.append(word[:-1])
        self.stopwords = set(stopwords)

        # loading df table
        self.df_table = numpy.load(df_path)

    def get(self, sentence):
        # pos-tagging
        words = jieba.lcut(sentence, cut_all=False, HMM=True)

        # remove stop words
        words = [word for word in words if word not in self.stopwords]
        if len(words) == 0:
            raise Exception("stopwords only sentence")

        # word2vec
        words_with_vectors = [(word, self.embedding[word]) for word in words]

        # apply tf-idf
        words_with_vectors = [(word, vector * log(DF_DOC_COUNT/(1+self.df_table[_hash(word)])))
                              for word, vector in words_with_vectors]

        return numpy.mean([vector for word, vector in words_with_vectors], axis=0)


if __name__ == '__main__':
    sentence2Vec = Sentence2Vec(
        './fasttext_model_ptt_wiki_2.bin', 'dict.txt.big', 'df.npy', 'stopwords.txt')
    print(sentence2Vec.get("我也覺得國泰很難辦"))
