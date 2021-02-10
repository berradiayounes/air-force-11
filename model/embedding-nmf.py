from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import NMF
import pandas as pd


def get_topics(D, feature_names, n_top_words, verbose):
    p, r = D.shape
    topic_dict = {}
    for topic_idx in range(r):
        topic = D[:, topic_idx]
        message = "Topic #%d: " % topic_idx
        message += " ".join(
            [
                feature_names[i]
                for i in topic.argsort()[: -n_top_words - 1 : -1]
            ]
        )
        if verbose:
            print(message)

        topic_dict[topic_idx] = [
            feature_names[i] for i in topic.argsort()[: -n_top_words - 1 : -1]
        ]
    return topic_dict


def get_nmf_topics(
    path,
    review_column="review",
    n_features=50,
    n_components=20,
    n_top_words=5,
    verbose=False,
):
    dataset = pd.read_csv(path, na_values="")[review_column].dropna().values

    tfidf_vectorizer = TfidfVectorizer(
        max_df=0.5,  # max doc freq (as a fraction) of any word to include in the vocabulary
        min_df=2,  # min doc freq (as doc counts) of any word to include in the vocabulary
        max_features=n_features,  # max number of words in the vocabulary
        stop_words="english",  # remove English stopwords
        use_idf=True,
    )  # use IDF scores
    tfidf = tfidf_vectorizer.fit_transform(dataset)

    # Fit the NMF model
    nmf = NMF(n_components=n_components).fit(tfidf)

    topic_dict = get_topics(
        nmf.components_.T,
        tfidf_vectorizer.get_feature_names(),
        n_top_words,
        verbose,
    )

    return topic_dict


if __name__ == "__main__":
    topic_dict = get_nmf_topics("data/flight_report.csv", verbose=True)
