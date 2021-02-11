import numpy as np
import pandas as pd
import aspect_based_sentiment_analysis as absa
from transformers import BertTokenizer
from tqdm import tqdm


def create_absa_pipeline(default_model=True, model_name="absa/classifier-rest-0.2"):
    """
    Initialize the pipeline according to the desired model.

    Input:
      default_model: boolean, True if we want to use default absa model
      model_name: str, 'absa/classifier-rest-0.2' or 'absa/classifier-lapt-0.2',
                  rest for restaurants or lapt for laptops
    """

    if default_model:
        return absa.load()

    model = absa.BertABSClassifier.from_pretrained(model_name)
    tokenizer = BertTokenizer.from_pretrained(model_name)
    professor = absa.Professor(
        pattern_recognizer=absa.aux_models.BasicPatternRecognizer()
    )  # Independent component that supervises and explains a model prediction.
    text_splitter = absa.sentencizer()  # The English CNN model from SpaCy.

    return absa.Pipeline(model, tokenizer, professor, text_splitter)


def get_aspects_for_review(review, all_aspects):
    """
    Select aspects that appear in the given review.

    review: str, review in english
    all_aspects: [str], list of all aspects of interest
    """

    aspects = []
    for aspect in all_aspects:
        if aspect in review.lower():
            aspects.append(aspect)

    return aspects


def get_sentiments(
    reviews,
    all_aspects,
    review_column,
    default_model=True,
    model_name="absa/classifier-rest-0.2",
    verbose=True,
):
    """
    Get sentiments on the given reviews regarding the given aspects.

    default_model: boolean, True if we want to use default absa model
    reviews: Pandas Dataframe, Dataframe with one "review" column indexed by integers
    all_aspects: [str], list of all aspects of interest
    model_name: str, 'absa/classifier-rest-0.2' or 'absa/classifier-lapt-0.2'
    """

    nlp = create_absa_pipeline(default_model, model_name)

    if verbose:
        print("Model created...")

    NaN = np.nan
    for aspect in all_aspects:
        reviews[aspect] = NaN

    if verbose:
        print("Starting to analyze sentiments...")

    reviews = reviews.head(20)

    for i in tqdm(reviews.index):
        review = reviews.at[i, review_column]
        aspects = get_aspects_for_review(review, all_aspects)

        if aspects != []:
            for task in nlp(review, aspects=aspects):
                if task.sentiment == absa.Sentiment.negative:
                    reviews.at[i, task.aspect] = -1
                if task.sentiment == absa.Sentiment.neutral:
                    reviews.at[i, task.aspect] = 0
                if task.sentiment == absa.Sentiment.positive:
                    reviews.at[i, task.aspect] = 1

    if verbose:
        print("Done!")

    return reviews
