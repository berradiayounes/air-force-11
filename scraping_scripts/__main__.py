# Here we will create 2 files : 1 simple file that contains only the reviews. The second file will contain
# the additional pieces of information each member of the group managed to scrap.

import pandas as pd
import numpy as np
from datetime import datetime
import langdetect
from langdetect import detect
import string
from tqdm import tqdm
import warnings

warnings.filterwarnings("ignore")

tqdm.pandas()


def format_date(date):
    date = datetime.strptime(
        date.strip(),
        "%B %d, %Y",
    ).strftime("%Y-%m-%d")

    return date


def keep_only_english_non_empty(sentence):
    if pd.isna(sentence):
        return sentence

    sentence_wo_punctuation = "".join(
        [c.lower() for c in sentence if c not in string.punctuation]
    ).strip()

    if sentence_wo_punctuation == "":
        return np.nan
    try:
        review_language = detect(sentence)
    except langdetect.lang_detect_exception.LangDetectException:
        return np.nan

    if review_language != "en":
        return np.nan

    return sentence


def merge_reviews():
    # Flight_report_df part
    flight_report_df = pd.read_csv("data/flight_report.csv")
    flight_report_df = flight_report_df.rename(
        columns={"review": "Review Body"}
    )
    flight_report_df_simple = flight_report_df["Review Body"]

    # airline_ratings_df PART
    airline_ratings_df = pd.read_csv(
        "data/airlineratings.csv", sep="\t", encoding="utf-8-sig"
    )

    # standardizing the scores /10
    percentage_columns = [
        "Overall Value for Money",
        "Seat and Cabin Space",
        "Customer Service",
        "In Flight Entertainment",
        "Baggage Handling",
        "Check-in Process",
        "Meals and Beverages",
    ]
    for col in percentage_columns:
        airline_ratings_df[col] = airline_ratings_df[col].replace(
            {
                "100%": float(10),
                "90%": float(9),
                "80%": float(8),
                "70%": float(7),
                "60%": float(6),
                "50%": float(5),
                "40%": float(4),
                "30%": float(3),
                "20%": float(2),
                "10%": float(1),
                "0%": float(0),
            }
        )

    airline_ratings_df["Rating"] = airline_ratings_df["Rating"].replace(
        {
            "10/10": float(10),
            "9/10": float(9),
            "8/10": float(8),
            "7/10": float(7),
            "6/10": float(6),
            "5/10": float(5),
            "4/10": float(4),
            "3/10": float(3),
            "2/10": float(2),
            "1/10": float(1),
            "0/10": float(0),
        }
    )
    airline_ratings_df["Review Title"] = np.nan
    airline_ratings_df["Route"] = np.nan
    airline_ratings_df["Date"] = airline_ratings_df["Date"].apply(format_date)

    # rearranging the different columns to to append the different files after
    airline_ratings_df_rearranged = airline_ratings_df[
        [
            "Airline",
            "Review Title",
            "Review",
            "Recommend Airline",
            "Rating",
            "Class",
            "Country",
            "Route",
            "Overall Value for Money",
            "Seat and Cabin Space",
            "Customer Service",
            "In Flight Entertainment",
            "Meals and Beverages",
            "Date",
        ]
    ]

    # renaming the columns to append the different files after
    airline_ratings_df_rearranged = airline_ratings_df_rearranged.rename(
        columns={
            "Review": "Review Body",
            "Recommend Airline": "Recommended",
            "Rating": "Score",
            "Overall Value for Money": "Score Value for Money",
            "Seat and Cabin Space": "Score Seat Comfort",
            "Customer Service": "Cabin Staff & Customer Service",
            "Meals and Beverages": "Food and Beverages",
            "In Flight Entertainment": "Inflight Entertainment",
        }
    )

    airline_ratings_df_simple = airline_ratings_df_rearranged["Review Body"]
    simple_master_file = flight_report_df_simple.append(
        airline_ratings_df_simple
    )

    # trip_advisor_df PART
    trip_advisor_df = pd.read_csv("data/trip_advisor_reviews.csv")
    trip_advisor_df = trip_advisor_df.rename(
        columns={"reviews": "Review Body"}
    )
    trip_advisor_df["scores"] = (
        trip_advisor_df["scores"] * 2
    )  # standardizing the scores /10

    trip_advisor_df_simple = trip_advisor_df["Review Body"]
    simple_master_file = simple_master_file.append(trip_advisor_df_simple)

    # skytrax_df PART
    skytrax_df = pd.read_csv("data/skytrax.csv", sep="\t")
    skytrax_df["Review_Body"] = (
        skytrax_df["Review_Body"]
        .str.replace("✅ Trip Verified |", "")
        .replace("❌", "")
        .replace("Not Verified |", "")
    )

    # rearranging the different columns to to append the different files after
    skytrax_df_rearranged = skytrax_df[
        [
            "Airline",
            "Review title",
            "Review_Body",
            "Recommended",
            "Rating out of 10",
            "Seat_Type",
            "Route",
            "Value For Money",
            "Seat comfort",
            "Cabin Staff Service",
            "Inflight Entertainment",
            "Food and Beverages",
            "Date Published",
        ]
    ]

    # renaming the columns to append the different files after
    skytrax_df_rearranged = skytrax_df_rearranged.rename(
        columns={
            "Review title": "Review Title",
            "Review_Body": "Review Body",
            "Rating out of 10": "Score",
            "Seat_Type": "Class",
            "Value For Money": "Score Value for Money",
            "Seat comfort": "Score Seat Comfort",
            "Cabin Staff Service": "Cabin Staff & Customer Service",
            "Date Published": "Date",
        }
    )

    skytrax_df_simple = skytrax_df_rearranged["Review Body"]
    simple_master_file = simple_master_file.append(skytrax_df_simple)
    simple_master_file = (
        simple_master_file.dropna()
        .progress_apply(keep_only_english_non_empty)
        .dropna()
    )

    # Creating a simple master file with only the reviews
    simple_master_file.to_csv("data/main.csv", index=False)

    # Creating a big masterfile that tries to not loose date
    master_file = pd.DataFrame(
        columns=[
            "Airline",
            "Review Title",
            "Review Body",
            "Recommended",
            "Score",
            "Class",
            "Country",
            "Route",
            "Score Value for Money",
            "Score Seat Comfort",
            "Cabin Staff & Customer Service",
            "Inflight Entertainment",
            "Food and Beverages",
            "Date",
        ]
    )
    master_file = master_file.append(airline_ratings_df_rearranged)
    master_file = master_file.append(skytrax_df_rearranged)
    master_file["Review Body"] = master_file["Review Body"].progress_apply(
        keep_only_english_non_empty
    )
    master_file = master_file.dropna(subset=["Review Body"])
    master_file.to_csv("data/main_with_ratings.csv", index=False)

    master_file["Class"].replace(
        {
            "Flew Economy Class": "Economy Class",
            "Flew Business Class": "Business Class",
            "Flew Economy": "Economy Class",
            "Flew First": "First Class",
            "Flew Premium Economy": "Premium Economy Class",
            "Flew Business": "Business Class",
            "Flew Premium Economy Class": "Premium Economy Class",
            "Flew First Class": "First Class",
            "Premium Economy": "Premium Economy Class",
        },
        inplace=True,
    )
    master_file["Airline_Merge"] = (
        master_file["Airline"]
        .str.replace("-", "")
        .str.replace(" ", "")
        .str.lower()
    )

    df3 = pd.read_csv("data/airlineratings_categories_and_ratings.csv")
    df3["Airline_Merge"] = (
        df3["Airline"].str.replace(" ", "").str.replace("-", "").str.lower()
    )

    main_file = pd.merge(
        master_file, df3, left_on="Airline_Merge", right_on="Airline_Merge"
    )

    main_file = main_file.rename(
        columns={"Rating": "Rating Airline from other file"}
    )
    main_file[["YEAR", "MONTH", "DAY"]] = main_file["Date"].str.split(
        "-", expand=True
    )
    main_file[["YEAR", "MONTH", "DAY"]] = main_file[
        ["YEAR", "MONTH", "DAY"]
    ].astype(int)
    main_file["Recommended"] = main_file["Recommended"].str.lower()
    del main_file["Date"]

    # This filter will give you the data that includes only the starting year and above.
    def filter_by_year(df, year):
        output = df[df.YEAR >= year]
        print(output.shape)
        return output

    # This filter will give you the data that includes only the type of category you choose.
    # You may choose between 3 categories : "Full Service Carrier", "Low Cost Carrier" and "Regional Carrier"
    def filter_by_category(df, category):
        output = df[df.Category == category]
        print(output.shape)
        return output

    # This filter will give you only the recommended ("yes") or not recommended ('no') data
    def filter_by_recommended(df, answer):
        output = df[df.Recommended == answer]
        print(output.shape)
        return output

    # This will filter the dataset by seat type/class type.
    # Economy Class
    # Business Class
    # Premium Economy Class
    # First Class
    def filter_by_class(df, CLASSE):
        output = df[df.Class == CLASSE]
        print(output.shape)
        return output

    # main_file = filter_by_year(main_file,2015)
    # main_file = filter_by_category(main_file,"Full Service Carrier")
    # main_file = filter_by_recommended(main_file, 'no')
    # main_file = filter_by_class(main_file, 'First Class')

    final_master_file = main_file

    _ = final_master_file.to_csv("data/main_with_ratings_category.csv")

    return True


if __name__ == "__main__":
    _ = merge_reviews()
