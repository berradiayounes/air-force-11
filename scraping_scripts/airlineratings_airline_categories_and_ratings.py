from bs4 import BeautifulSoup
import requests
import pandas as pd


def airlineratings_scraping():
    df_airlines = pd.DataFrame(columns=["Airline", "Category", "Rating"])

    url = "https://www.airlineratings.com/airline-passenger-reviews/"
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

        # Reviews pages for each airline with the same beginning letter
        for number_of_airlines in range(len(airlines_first_letter_href)):

            # Scrape infos on first page of one particular airline
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

            # Get airline category
            airline_header = soup_airline.findAll(
                "header", {"class": "td-post-title td-post-title-logo"}
            )
            airline_category = airline_header[0].find("p").text

            # Get airline average rating
            airline_rating_box = soup_airline.findAll(
                "div", {"class": "average_passenger_rating"}
            )
            if len(airline_rating_box) > 0:
                airline_rating = airline_rating_box[0].find("h4").text[:-4]

            # Put infos in df
            df_airlines = df_airlines.append(
                {
                    "Airline": airline_name,
                    "Category": airline_category,
                    "Rating": airline_rating,
                },
                ignore_index=True,
            )

    df_airlines.to_csv(
        "data/airlineratings_categories_and_ratings.csv", sep=",", index=False
    )

    return True


if __name__ == "__main__":
    _ = airlineratings_scraping()
