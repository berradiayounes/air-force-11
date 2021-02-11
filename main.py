import pandas as pd 
import numpy as np
import os

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
    df_preprocessed.to_csv(PREPROCESSED_DATA_PATH)

    return df_preprocessed


def main(method=METHOD_TOPIC_MODELING):
    df = pd.read_csv(DATA_PATH)
    df_preprocessed = preprocess(df)

    if not os.path.exists("results"):
        os.makedirs("results")
        
    if method == "gensim":
        topic_dict = topic_modeling(df_preprocessed[f"{REVIEW_COLUMN}_preprocessed"], start=2, limit=8, step=1, num_words_per_topic=5)
        topic_df = pd.DataFrame(topic_dict)
        _ = topic_df.to_csv(f"topics_{method}.csv")

    elif method == "nmf":
        embeddings, feature_names = get_embeddings_nmf(
            PREPROCESSED_DATA_PATH, review_column=f"{REVIEW_COLUMN}_preprocessed", verbose=True
        )   
        topic_dict = get_topics(
            embeddings,
            feature_names,
            n_top_words=5,
            verbose=True,
        )
        _ = topic_df.to_csv(f"topics_{method}.csv")

    sentiment_df = get_sentiments(df[[REVIEW_COLUMN]], topic_df)
    _ = sentiment_df.to_csv(f"sentiment_{method}.csv")

    return 0

if __name__ == "__main__":
    _ = main()
