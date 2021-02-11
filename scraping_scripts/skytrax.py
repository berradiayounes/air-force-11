import pandas as pd
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import numpy as np


def scrape_skytrax():
    url = "https://www.airlinequality.com/review-pages/a-z-airline-reviews/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text)
    soup2 = soup.find_all("div", {"class": "a_z_col_group"})

    list_airlines = []
    for i in soup2:
        p = i.find_all("a")
        for k in p:
            k.get("href")
            list_airlines.append(k.get("href"))

    main_df = pd.DataFrame(
        columns=[
            "Airline",
            "Review title",
            "Review_Body",
            "Rating out of 10",
            "Verified?",
            "Date Published",
            "Aircraft",
            "Type_Of_Traveller",
            "Seat_Type",
            "Route",
            "Date_Flown",
            "Recommended",
            "Seat comfort",
            "Cabin Staff Service",
            "Food and Beverages",
            "Inflight Entertainment",
            "Ground Service",
            "Wifi and Connectivity",
            "Value For Money",
        ]
    )

    url = "https://www.airlinequality.com/review-pages/a-z-airline-reviews/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text)
    soup2 = soup.find_all("div", {"class": "a_z_col_group"})

    list_airlines = []
    for i in soup2:
        p = i.find_all("a")
        for k in p:
            k.get("href")
            list_airlines.append(k.get("href"))

    for i in tqdm(list_airlines):
        url = "https://www.airlinequality.com{}/page/1/?sortby=post_date%3ADesc&pagesize=10000".format(
            i
        )
        page = requests.get(url)
        soup = BeautifulSoup(page.text)
        print("starting with:", i)
        Airline = i[17:]
        list_reviews = soup.findAll("article", {"itemprop": "review"})

        nb_of_review = 0
        # itirating through the reviews:
        for review in tqdm(list_reviews):

            nb_of_review = nb_of_review + 1

            date_published = review.find(
                "meta", {"itemprop": "datePublished"}
            ).get("content")

            if review.find("span", {"itemprop": "ratingValue"}) == None:
                rating_out_of_10 = "NA"
            else:
                rating_out_of_10 = int(
                    review.find("span", {"itemprop": "ratingValue"}).text
                )

            author = review.find("span", {"itemprop": "name"}).text

            review_title = (
                review.find("div", {"class": "body"})
                .find("h2", {"class": "text_header"})
                .text[1:-1]
            )

            if review.find("div", {"class": "text_content"}) == None:
                is_verified = "no"
            elif (
                review.find("div", {"class": "text_content"}).find("strong")
                == None
            ):
                is_verified = "no"
            elif (
                review.find("div", {"class": "text_content"})
                .find("strong")
                .find("em")
                == None
            ):
                is_verified = "no"
            else:
                is_verified = (
                    review.find("div", {"class": "text_content"})
                    .find("strong")
                    .find("em")
                    .text
                )

            review_body = review.find("div", {"class": "text_content"}).text

            Big_stats = review.find("div", {"class": "review-stats"})
            list_stats = Big_stats.find_all("tr")

            Aircraft = ""
            Type_Of_Traveller = ""
            Seat_Type = ""
            Route = ""
            Date_Flown = ""
            Recommended = ""
            Seat_Comfort = np.nan
            Cabin_Staff_Service = np.nan
            Food_and_Beverages = np.nan
            Inflight_Entertainment = np.nan
            Ground_Service = np.nan
            Wifi_and_Connectivity = np.nan
            Value_For_Money = np.nan

            for stat in list_stats:
                if stat.find_all("td")[0].text == "Aircraft":
                    Aircraft = stat.find_all("td")[1].text

                elif stat.find_all("td")[0].text == "Type Of Traveller":
                    Type_Of_Traveller = stat.find_all("td")[1].text

                elif stat.find_all("td")[0].text == "Seat Type":
                    Seat_Type = stat.find_all("td")[1].text

                elif stat.find_all("td")[0].text == "Route":
                    Route = stat.find_all("td")[1].text

                elif stat.find_all("td")[0].text == "Date Flown":
                    Date_Flown = stat.find_all("td")[1].text

                elif stat.find_all("td")[0].text == "Recommended":
                    Recommended = stat.find_all("td")[1].text

                elif stat.find_all("td")[0].text == "Seat Comfort":
                    if (
                        len(
                            stat.find_all("td")[1].find_all(
                                "span", {"class": "star fill"}
                            )
                        )
                        == 0
                    ):
                        Seat_Comfort = np.nan
                    else:
                        Seat_Comfort = int(
                            stat.find_all("td")[1]
                            .find_all("span", {"class": "star fill"})[-1]
                            .text
                        )

                elif stat.find_all("td")[0].text == "Cabin Staff Service":
                    if (
                        len(
                            stat.find_all("td")[1].find_all(
                                "span", {"class": "star fill"}
                            )
                        )
                        == 0
                    ):
                        Cabin_Staff_Service = np.nan
                    else:
                        Cabin_Staff_Service = int(
                            stat.find_all("td")[1]
                            .find_all("span", {"class": "star fill"})[-1]
                            .text
                        )

                elif stat.find_all("td")[0].text == "Food & Beverages":
                    if (
                        len(
                            stat.find_all("td")[1].find_all(
                                "span", {"class": "star fill"}
                            )
                        )
                        == 0
                    ):
                        Food_and_Beverages = np.nan
                    else:
                        Food_and_Beverages = int(
                            stat.find_all("td")[1]
                            .find_all("span", {"class": "star fill"})[-1]
                            .text
                        )

                elif stat.find_all("td")[0].text == "Inflight Entertainment":
                    if (
                        len(
                            stat.find_all("td")[1].find_all(
                                "span", {"class": "star fill"}
                            )
                        )
                        == 0
                    ):
                        Inflight_Entertainment = np.nan
                    else:
                        Inflight_Entertainment = int(
                            stat.find_all("td")[1]
                            .find_all("span", {"class": "star fill"})[-1]
                            .text
                        )

                elif stat.find_all("td")[0].text == "Ground Service":
                    if (
                        len(
                            stat.find_all("td")[1].find_all(
                                "span", {"class": "star fill"}
                            )
                        )
                        == 0
                    ):
                        Ground_Service = np.nan
                    else:
                        Ground_Service = int(
                            stat.find_all("td")[1]
                            .find_all("span", {"class": "star fill"})[-1]
                            .text
                        )

                elif stat.find_all("td")[0].text == "Wifi & Connectivity":
                    if (
                        len(
                            stat.find_all("td")[1].find_all(
                                "span", {"class": "star fill"}
                            )
                        )
                        == 0
                    ):
                        Wifi_and_Connectivity = np.nan
                    else:
                        Wifi_and_Connectivity = int(
                            stat.find_all("td")[1]
                            .find_all("span", {"class": "star fill"})[-1]
                            .text
                        )

                elif stat.find_all("td")[0].text == "Value For Money":
                    if (
                        len(
                            stat.find_all("td")[1].find_all(
                                "span", {"class": "star fill"}
                            )
                        )
                        == 0
                    ):
                        Value_For_Money = np.nan
                    else:
                        Value_For_Money = int(
                            stat.find_all("td")[1]
                            .find_all("span", {"class": "star fill"})[-1]
                            .text
                        )

            data = [
                [
                    Airline,
                    review_title,
                    review_body,
                    rating_out_of_10,
                    is_verified,
                    date_published,
                    Aircraft,
                    Type_Of_Traveller,
                    Seat_Type,
                    Route,
                    Date_Flown,
                    Recommended,
                    Seat_Comfort,
                    Cabin_Staff_Service,
                    Food_and_Beverages,
                    Inflight_Entertainment,
                    Ground_Service,
                    Wifi_and_Connectivity,
                    Value_For_Money,
                ]
            ]

            df1 = pd.DataFrame(
                data,
                columns=[
                    "Airline",
                    "Review title",
                    "Review_Body",
                    "Rating out of 10",
                    "Verified?",
                    "Date Published",
                    "Aircraft",
                    "Type_Of_Traveller",
                    "Seat_Type",
                    "Route",
                    "Date_Flown",
                    "Recommended",
                    "Seat comfort",
                    "Cabin Staff Service",
                    "Food and Beverages",
                    "Inflight Entertainment",
                    "Ground Service",
                    "Wifi and Connectivity",
                    "Value For Money",
                ],
            )
            main_df = main_df.append(df1)

    _ = main_df.to_csv(
        "data/skytrax.csv", sep="\t", index=False, encoding="utf-8-sig"
    )

    return True


if __name__ == "__main__":
    _ = scrape_skytrax()
