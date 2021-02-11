import pandas as pd 
import numpy as np

from model.preprocess import Preprocessor



def main():
    df = pd.read_csv("data/main.csv")
    preprocessor = Preprocessor()
    df_preprocessed = preprocessor.preprocess(df, "Review Body")
    df_preprocessed.to_csv("data/main_preprocessed.csv")

    return 0

if __name__ == "__main__":
    _ = main()
