import pandas as pd 
import numpy as np
import os
import sys
from argparse import ArgumentParser

from model.preprocess import Preprocessor
from model.topic_modeling_gensim import topic_modeling
from model.embedding_nmf import get_embeddings_nmf, get_topics
from model.sentiment_analysis import get_sentiments

DATA_PATH = "data/main_with_ratings_category.csv"
PREPROCESSED_DATA_PATH = DATA_PATH.replace(".csv", "_preprocessed.csv")
REVIEW_COLUMN = "Review Body"
METHOD_TOPIC_MODELING = "gensim"

def preprocess(df):
    preprocessor = Preprocessor(stem=False)
    df_preprocessed = preprocessor.preprocess(df, REVIEW_COLUMN)
    df_preprocessed.to_csv(PREPROCESSED_DATA_PATH, index=False)

    return df_preprocessed


def main(method=METHOD_TOPIC_MODELING, from_scratch=False):
    df = pd.read_csv(DATA_PATH)
    if from_scratch:
        print("PREP")
        df_preprocessed = preprocess(df)
    else:
        df_preprocessed = pd.read_csv(PREPROCESSED_DATA_PATH,  converters={f"{REVIEW_COLUMN}_preprocessed": eval})

    if not os.path.exists("results"):
        os.makedirs("results")
        
    if method == "gensim":
        topic_dict = topic_modeling(df_preprocessed[f"{REVIEW_COLUMN}_preprocessed"], start=2, limit=8, step=1, num_words_per_topic=5)
        topic_df = pd.DataFrame(topic_dict)
        _ = topic_df.to_csv(f"topics_{method}.csv")

    elif method == "nmf":
        embeddings, feature_names = get_embeddings_nmf(
            df_preprocessed, review_column=f"{REVIEW_COLUMN}_preprocessed", verbose=True
        )   
        topic_dict = get_topics(
            embeddings,
            feature_names,
            n_top_words=5,
            verbose=True,
        )
        topic_df = pd.DataFrame(topic_dict)
        _ = topic_df.to_csv(f"topics_{method}.csv")

    aspects_list = []
    for new_aspects in topic_dict.values():
        aspects_list = [*aspects_list, *new_aspects]
    sentiment_df = get_sentiments(df[[REVIEW_COLUMN]], aspects_list, REVIEW_COLUMN)
    _ = sentiment_df.to_csv(f"sentiment_{method}.csv")

    return 0

if __name__ == "__main__":
    parser = ArgumentParser()
    _ = parser.add_argument("--from_scratch", "-fs", type=bool, default=False)
    _ = parser.add_argument("--method", "-m", type=str, default=METHOD_TOPIC_MODELING)
    args = parser.parse_args()
    sys.exit(
        main(
            method=args.method,
            from_scratch=args.from_scratch,
        )
    )