from bs4 import BeautifulSoup
import requests
import string
from tqdm import tqdm
import pandas as pd
from datetime import datetime

BASE_URL = "https://flight-report.com"
AIRLINE_PAGE_URL = f"{BASE_URL}/en/airline/" + "?l={}"


def get_airline_links(url=AIRLINE_PAGE_URL):
    airline_links = {}
    alphabet = list(string.ascii_lowercase)
    for letter in tqdm(alphabet):
        soup = BeautifulSoup(requests.get(url.format(letter)).text, features="lxml")
        airlines_html = soup.findAll("article", {"class": "airline"})
        for element in airlines_html:
            name = element.find("span", {"itemprop": "name"}).text
            link = BASE_URL + element.find("a").get("href")
            airline_links[name] = link
    return airline_links


def get_review_links(url, base_url=BASE_URL):
    soup = BeautifulSoup(requests.get(url).text, features="lxml")
    review_links = [
        el.get("content")
        for el in soup.find(id="reports").find_all("meta", {"itemprop": "url"})
    ]
    review_links = [base_url + link for link in review_links]
    return review_links


def get_review(url):
    soup = BeautifulSoup(requests.get(url).text, features="lxml")
    review = "".join(
        [element.text for element in soup.find(id="Conclusion").find_all("p")]
    )
    return review


def get_ratings(url):
    rating_dict = {}
    soup = BeautifulSoup(requests.get(url).text, features="lxml")
    rating_rows = soup.find_all("div", {"class": "colRanking children"})
    for row in rating_rows:
        for i, element in enumerate(row.find_all("span")):
            if i % 3 == 0:
                key = element.text
            if i % 3 == 2:
                value = float(element.text)
                rating_dict[key] = value

    # get date
    date = datetime.strptime(
        soup.find("div", {"class": "publishing"})
        .text.strip()
        .replace("Published on ", "")
        .replace("st", "")
        .replace("nd", "")
        .replace("rd", "")
        .replace("th", "")
        .replace("Augu", "August"),
        "%d %B %Y",
    ).strftime("%Y-%m-%d")
    rating_dict["date"] = date

    return rating_dict


def scrape_flight_report():
    reviews = []
    airline_links = get_airline_links()
    for airline_name, airline_link in tqdm(airline_links.items()):
        review_links = get_review_links(airline_link)
        for link in tqdm(review_links):
            record = get_ratings(link)
            record["name"] = airline_name
            record["review"] = get_review(link)
            reviews.append(record)
    reviews_df = pd.DataFrame(reviews)
    return reviews_df


if __name__ == "__main__":
    scrape_flight_report()
