from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

# Define driver
driver = webdriver.Chrome(
    "../../../chromedriver"
)  # adapt based on your arborescence

# Write function to iterate through pages
def _find_element_click(
    driver,
    by,
    expression,
):
    """Find the element and click then  handle all type of exception during click
    Args:
        driver (selenium.driver): Selenium driver
        by (selenium.webdriver.common.by): Type of selector
            (By.XPATH, By.CSS_SELECTOR ...)
        expression (str): Selector expression to the element to click on
    Returns:
        bool: True if successfully clicked on the element
    """
    end_time = time.time() + 60
    while True:
        try:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight)"
            )
            time.sleep(2)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight)"
            )
            web_element = driver.find_element(by=by, value=expression)
            web_element.click()
            return True
        except:
            if time.time() > end_time:
                time.sleep(4)
                break
    return False


def get_tripadvisor_airlines():
    # Get airlines
    url = "https://www.tripadvisor.com/Airlines"
    driver.get(url)
    page = BeautifulSoup(driver.page_source)

    # Get all airlines that are still operating
    airlines = []
    links = []
    review_count = []
    i = 0
    total_pages = int(
        page.find("div", {"class": "pageNumbers"}).find_all("span")[-1].text
    )
    for i in range(total_pages - 1):
        page = BeautifulSoup(driver.page_source)

        for airline in page.find(
            "div", {"class": "mainColumnContent"}
        ).find_all("div", {"class": "airlineSummary"}):
            if "[no longer operating]" not in airline.text:
                airlines.append(airline.find("div").text)
                links.append(airline.find("a").get("href"))
                try:
                    review_string = (
                        airline.find("div", {"class": "airlineReviews"})
                        .text.split(" review")[0]
                        .replace(",", "")
                    )
                    review_count.append(int(review_string))
                except:
                    review_count.append(0)

        result = _find_element_click(
            driver, webdriver.common.by.By.CSS_SELECTOR, ".next"
        )
        if result == False:
            break
            print("Failure to go to next page")

    # Write to csv
    airline_info = pd.DataFrame(
        {"airlines": airlines, "links": links, "review_count": review_count}
    )
    airline_info.to_csv(
        "data/airline_links_tripadvisor.csv", sep=",", index=False
    )

    return True


if __name__ == "__main__":
    _ = get_tripadvisor_airlines()
