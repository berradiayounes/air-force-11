import string
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *
from tqdm import tqdm

tqdm.pandas()


class Preprocessor:
    def preprocess_sentence(self, sentence):
        sentence = "".join(
            [c.lower() for c in sentence if c not in string.punctuation]
        ).strip()

        sentence = " ".join(
            [
                w
                for w in word_tokenize(sentence)
                if not w in stopwords.words("english")
            ]
        )

        stemmer = PorterStemmer()
        sentence = " ".join([stemmer.stem(w) for w in word_tokenize(sentence)])

        return sentence

    def preprocess(self, df, review_col):
        df = df.dropna(subset=[review_col])
        df[f"{review_col}_preprocessed"] = df[review_col].progress_apply(
            self.preprocess_sentence
        )
        return df
