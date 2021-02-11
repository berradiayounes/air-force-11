from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

url = "https://www.airlineratings.com/airline-passenger-reviews/"


def collect_reviews_and_infos_on_one_page(comments_airline, reviews_df):
    for feedback in comments_airline:
        # get review
        review = feedback.find_all("div", {"class": "passenger_review_body"})[
            0
        ].find_all("p")
        if len(review) > 0:
            review = (
                feedback.find_all("div", {"class": "passenger_review_body"})[0]
                .find_all("p")[0]
                .text
            )
        else:
            review = np.nan

        # get rating
        rating = (
            feedback.find_all("div", {"class": "passenger_rating_overall"})[0]
            .find_all("h4")[0]
            .text
        )

        # get country
        country = (
            feedback.find_all("div", {"class": "passenger_review_header"})[0]
            .find_all("p")[0]
            .text
        )
        country = country[
            country.find("from ") + len("from ") : country.rfind(" -")
        ]

        # get date
        date = (
            feedback.find_all("div", {"class": "passenger_review_header"})[0]
            .find_all("p")[0]
            .text
        )
        date = date[date.find("- ") + len("- ") : date.rfind("")]

        # get class
        cabin_flown = feedback.find_all("p", {"class": "cabin_flown"})[0].text

        # get ratings by category
        ratings = {}
        li = feedback.find_all("div", {"class": "passenger_ratings"})[
            0
        ].find_all("li")
        for el in li:
            rating_cat = el.find_all("h4")[0].text
            if len(el.find_all("div", {"class": "rating"})) > 0:
                rating_value = el.find_all("div", {"class": "rating"})[0].get(
                    "style"
                )[7:]
            ratings[rating_cat] = rating_value

        # get rating for 'Overall Value for Money'
        if "Overall Value for Money" in ratings.keys():
            rating_ovm = ratings["Overall Value for Money"]
        else:
            rating_ovm = np.nan

        # get rating for 'Seat and Cabin Space'
        if "Seat and Cabin Space" in ratings.keys():
            rating_scs = ratings["Seat and Cabin Space"]
        else:
            rating_scs = np.nan

        # get rating for 'Customer Service'
        if "Customer Service" in ratings.keys():
            rating_cs = ratings["Customer Service"]
        else:
            rating_cs = np.nan

        # get rating for 'In Flight Entertainment'
        if "In Flight Entertainment" in ratings.keys():
            rating_ife = ratings["In Flight Entertainment"]
        else:
            rating_ife = np.nan

        # get rating for 'Baggage Handling'
        if "Baggage Handling" in ratings.keys():
            rating_bh = ratings["Baggage Handling"]
        else:
            rating_bh = np.nan

        # get rating for 'Check-in Process'
        if "Check-in Process" in ratings.keys():
            rating_cip = ratings["Check-in Process"]
        else:
            rating_cip = np.nan

        # get rating for 'Check-in Process'
        if "Meals and Beverages" in ratings.keys():
            rating_mb = ratings["Meals and Beverages"]
        else:
            rating_mb = np.nan

        # get recommandation info
        recommandation = feedback.find_all(
            "div", {"class": "passenger_ratings"}
        )[0].find_all("li")[-1]
        if recommandation.find_all("h4")[0].text == "Recommend Airline":
            recommend = recommandation.find_all("span")[0].text
        else:
            recommend = np.nan

        # put infos in df
        reviews_df = reviews_df.append(
            {
                "Airline": airline_name,
                "Review": review,
                "Rating": rating,
                "Country": country,
                "Date": date,
                "Class": cabin_flown,
                "Overall Value for Money": rating_ovm,
                "Seat and Cabin Space": rating_scs,
                "Customer Service": rating_cs,
                "In Flight Entertainment": rating_ife,
                "Baggage Handling": rating_bh,
                "Check-in Process": rating_cip,
                "Meals and Beverages": rating_mb,
                "Recommend Airline": recommend,
            },
            ignore_index=True,
        )
    return reviews_df


def airlineratings_scraping(url):
    reviews_df = pd.DataFrame(
        columns=[
            "Airline",
            "Review",
            "Rating",
            "Country",
            "Date",
            "Class",
            "Overall Value for Money",
            "Seat and Cabin Space",
            "Customer Service",
            "In Flight Entertainment",
            "Baggage Handling",
            "Check-in Process",
            "Meals and Beverages",
            "Recommend Airline",
        ]
    )

    page = requests.get(url)
    soup = BeautifulSoup(page.text)
    li = soup.findAll("div", {"class": "td-page-content"})[0].find_all("li")

    airlines_A_Z_href = []
    for el in li:
        airlines_A_Z_href.append(el.find("a").get("href"))

    for first_letter in range(len(airlines_A_Z_href)):
        url_first_letter = (
            "https://www.airlineratings.com" + airlines_A_Z_href[first_letter]
        )
        page_first_letter = requests.get(url_first_letter)
        soup_first_letter = BeautifulSoup(page_first_letter.text)
        li_first_letter = soup_first_letter.findAll(
            "div", {"class": "td-page-content"}
        )[0].find_all("li")

        airlines_first_letter_href = []
        for el in li_first_letter:
            airlines_first_letter_href.append(el.find("a").get("href"))
        airlines_first_letter_href = airlines_first_letter_href[26:]

        # Reviews for each airline with the same first letter
        for number_of_airlines in range(len(airlines_first_letter_href)):

            # Reviews from first page of one particular airline
            url_airline = airlines_first_letter_href[number_of_airlines]
            page_airline = requests.get(url_airline)
            soup_airline = BeautifulSoup(page_airline.text)
            airline_name = (
                soup_airline.findAll(
                    "header", {"class": "td-post-title td-post-title-logo"}
                )[0]
                .find_all("h1")[0]
                .text
            )
            comments_airline = soup_airline.findAll(
                "div", {"class": "passenger_review"}
            )

            reviews_df = collect_reviews_and_infos_on_one_page(
                comments_airline, reviews_df
            )

            # Reviews from pages 2 to end of this particular airline
            for page_number in range(2, 10000):
                url_airline = (
                    airlines_first_letter_href[number_of_airlines]
                    + "page/"
                    + str(page_number)
                    + "/"
                )
                page_airline = requests.get(url_airline)
                soup_airline = BeautifulSoup(page_airline.text)
                airline_name = (
                    soup_airline.findAll(
                        "header", {"class": "td-post-title td-post-title-logo"}
                    )[0]
                    .find_all("h1")[0]
                    .text
                )
                comments_airline = soup_airline.findAll(
                    "div", {"class": "passenger_review"}
                )

                if len(comments_airline) == 0:
                    break

                reviews_df = collect_reviews_and_infos_on_one_page(
                    comments_airline, reviews_df
                )

    reviews_df.to_csv(
        "data/airlineratings.csv", sep="\t", index=False, encoding="utf-8-sig"
    )

    return True


if __name__ == "__main__":
    _ = airlineratings_scraping()
