import matplotlib.pyplot as pyplot
import re
import numpy
import hickle
import os
from sklearn.cluster import AgglomerativeClustering
from tqdm import tqdm
import json

re_url_and_emo = re.compile(r'(?:\[[a-zA-Z0-9]+\])|(?:https?:[^\s\n]+)')


def _kmeans(vectors):
    pass


def remove_url(sentence):
    pass


if __name__ == '__main__':
    IDS_SENTENCES_VECS_JSON_PATH = 'sentences_with_vecs.json'
    if not os.path.exists(IDS_SENTENCES_VECS_JSON_PATH):
        from sentence2vec import Sentence2Vec
        from grabber.models import Plurk
        # sentence2vec
        sentence2vec = Sentence2Vec(
            './fasttext_model_ptt_wiki_2.bin',
            'dict.txt.big',
            'df.npy',
            'stopwords.txt')
        ids_sentences_vecs = []
        for plurk in tqdm(Plurk.select()):
            try:
                sentence = re_url_and_emo.sub('', plurk.content_raw)
                vector = sentence2vec.get(sentence)
                ids_sentences_vecs.append((plurk.id, sentence, vector.tolist()))
            except Exception as e:
                continue
        json.dump(ids_sentences_vecs, open(
            IDS_SENTENCES_VECS_JSON_PATH, "w"), ensure_ascii=False)
    # clustering
    ids_sentences_vecs = json.load(open(IDS_SENTENCES_VECS_JSON_PATH, "r"))
    ids, sentences, vectors = zip(*ids_sentences_vecs)
    clustering = AgglomerativeClustering(
        n_clusters=1000,
        affinity='cosine',
        linkage='complete').fit(vectors)
    ids_sentences_with_labels = list(zip(ids, sentences, clustering.labels_))
    ids_sentences_with_labels.sort(key=lambda x: x[2])
    with open("classed.txt", "w") as output:
        for _id, sentence, label in ids_sentences_with_labels:
            output.write("[{}] {} {}\n".format(
                label, _id, sentence.replace("\n", " ").replace("\r", "")))
