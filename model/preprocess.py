import string
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from langdetect import detect
from tqdm import tqdm
import warnings
import transformers
from transformers import BertTokenizer


warnings.filterwarnings("ignore")

tqdm.pandas()


class Preprocessor:
    def __init__(self, stem=True, omit={}):
        self.stem = stem
        self.stemmer = PorterStemmer()
        self.omit = {"cancel", "covid", "cancelled"}
        self.omit.update(omit)
        name = "absa/classifier-rest-0.2"  # rest for restaurant
        self.tokenizer = BertTokenizer.from_pretrained(
            name
        ).basic_tokenizer.tokenize

    def preprocess_sentence(self, sentence):
        # Remove punctuation
        sentence = "".join(
            [c.lower() for c in sentence if c not in string.punctuation]
        ).strip()

        # Tokenize words
        sentence = [
            w
            for w in self.tokenizer(sentence)
            if not w in stopwords.words("english")
        ]

        # Empty review if it contains words in the omit set
        if self.omit.intersection(sentence):
            sentence = np.nan

        # Stem words
        if self.stem:
            stemmer = self.stemmer
            sentence = [stemmer.stem(w) for w in sentence]

        return sentence

    def preprocess(self, df, review_col):
        df = df.dropna(subset=[review_col])
        df[f"{review_col}_preprocessed"] = df[review_col].progress_apply(
            self.preprocess_sentence
        )
        df = df.dropna(subset=[f"{review_col}_preprocessed"])
        return df
