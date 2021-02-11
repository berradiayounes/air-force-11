# Imports
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import requests
from tqdm import tqdm


def scrape_tripadvisor():
    # Driver
    driver = webdriver.Chrome("./chromedriver")

    # Load airline urls (the csv file is written after running trip_advisor_airlines.py)
    airlines = pd.read_csv("data/airline_links_tripadvisor.csv", sep=",")

    # Go through all the pages of reviews
    for airline in airlines["airlines"]:
        print(airline)
        # Lists in which to feed the values for the final dataframe
        airline_name = []
        reviews = []
        dates = []
        scores = []
        itineraries = []
        regions = []
        classes = []

        # Access airline reviews page
        url = (
            "https://www.tripadvisor.com"
            + airlines.loc[airlines["airlines"] == airline]["links"].values[0]
        )
        [url_prefix, url_suffix] = url.split("Reviews-")
        driver.get(url)

        # Scroll down page to load it, and get the total number of pages
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        page = BeautifulSoup(driver.page_source)
        try:
            total_pages = int(
                page.find("div", {"class": "pageNumbers"})
                .find_all("a")[-1]
                .text
            )
        except:  # If there's only one page of reviews, the div block named pageNumbers will not be present at the bottom of the page
            total_pages = 1

        # Go through pages of reviews for one airline
        for i in tqdm(
            range(0, total_pages, 10)
        ):  # Skip pages to finish scraping before the end of the hackathon :)
            driver.get(url)

            # Scroll to load all reviews
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight)"
            )
            time.sleep(1)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight)"
            )

            # Use beautiful soup to read page contents
            page = BeautifulSoup(driver.page_source)

            # Go through all the reviews in one page, not all fields are available for every review, so we need to try extraction
            review_blocks = page.find_all("div", {"class": "oETBfkHU"})
            for review_block in review_blocks:
                # Review text
                try:
                    review = review_block.find("q", {"class": "IRsGHoPm"})
                    reviews.append(review.text)
                except:
                    break

                # Review scores (contained in the css class, so it needs to be extracted and converted to int)
                try:
                    score = review_block.find("div", {"class": "nf9vGX55"})
                    scores.append(int(score.find("span").get("class")[1][7]))
                except:
                    scores.append(-1)

                # Trip information, not all the time, but most times, we have the itinerary, the region of travel and the class of travel
                try:
                    tag = review_block.find("div", {"class": "hpZJCN7D"})
                    tags = tag.find_all("div", {"class": "_3tp-5a1G"})
                    if len(tags) == 1:
                        itineraries.append(tags[0].text)
                        regions.append("")
                        classes.append("")
                    elif len(tags) == 2:
                        itinerarie.append(tags[0].text)
                        regions.append(tags[1].text)
                        classes.append("")
                    else:
                        itinerarie.append(tags[0].text)
                        regions.append(tags[1].text)
                        classes.append(tags[2].text)
                except:
                    itineraries.append("")
                    regions.append("")
                    classes.append("")

            # Go to next page
            if total_pages > 1:
                url = (
                    url_prefix
                    + "Reviews-or"
                    + str((i + 1) * 5)
                    + "-"
                    + url_suffix
                )

        # Files are saved for each company, since the process is quite lengthy, it was easier that way in case there is an interruption
        reviews = pd.DataFrame(
            {
                "reviews": reviews,
                "scores": scores,
                "itineraries": itineraries,
                "regions": regions,
                "classes": classes,
            }
        )
        reviews.to_csv(
            "data/trip_advisor_reviews_" + airline + ".csv",
            sep=",",
            index=False,
        )

    # Merge all airline files into one
    from os import listdir
    from os.path import isfile, join

    # Load all files that contain airline reviews
    review_csvs = [
        f for f in listdir("../data/") if isfile(join("../data/", f))
    ]

    # Placeholder for final csv
    trip_advisor_reviews = pd.DataFrame(
        {
            "airline": [],
            "reviews": [],
            "scores": [],
            "itineraries": [],
            "regions": [],
            "classes": [],
        }
    )

    # Concatenate reviews
    for filename in tqdm(review_csvs):
        if "trip_advisor_reviews_" in filename:
            partial_reviews = pd.read_csv("../data/" + filename)
            partial_reviews["airline"] = filename.split("reviews_")[1].split(
                "."
            )[0]
            partial_reviews = partial_reviews.drop(
                partial_reviews.loc[partial_reviews["scores"] == -1].index
            )

            trip_advisor_reviews = pd.concat(
                [trip_advisor_reviews, partial_reviews]
            )

    # Write csv
    trip_advisor_reviews.to_csv(
        "../data/trip_advisor_reviews.csv", sep=",", encoding="utf8"
    )

    return True


if __name__ == "__main__":
    _ = scrape_tripadvisor()
