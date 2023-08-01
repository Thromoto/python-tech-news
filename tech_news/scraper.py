from parsel import Selector
import requests
import time
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    try:
        time.sleep(1)
        response = requests.get(
            url, headers={"user-agent": "Fake user-agent"}, timeout=3
        )
        if response.status_code == 200:
            return response.text
        else:
            return None

    except requests.Timeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(text=html_content)
    links = selector.css(".entry-title a::attr(href)").getall()
    return links


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    links = selector.css(".next.page-numbers::attr(href)").get()
    if links:
        return links
    else:
        return None


# Requisito 4
def scrape_news(html_content):
    content = {}

    selector = Selector(text=html_content)

    content["url"] = selector.css("head link[rel=canonical]::attr(href)").get()
    content["title"] = selector.css(".entry-title::text").get().strip()
    content["timestamp"] = selector.css(".meta-date::text").get()
    content["writer"] = selector.css(".author a::text").get()
    content["reading_time"] = int(
        selector.css(".meta-reading-time::text").re_first(r"\d+")
    )
    content["summary"] = "".join(
        selector.css(".entry-content > p:first-of-type *::text").getall()
    ).strip()
    content["category"] = selector.css(".label::text").get()

    return content


# Requisito 5
def get_tech_news(amount):
    all_news = []
    url = "https://blog.betrybe.com/"

    while len(all_news) < amount:
        html_content = fetch(url)
        news_links = scrape_updates(html_content)
        all_news.extend(news_links)
        url = scrape_next_page_link(html_content)

    news_data_list = []

    for news_url in all_news[:amount]:
        news_html = fetch(news_url)
        news_data = scrape_news(news_html)
        news_data_list.append(news_data)

    create_news(news_data_list)

    return news_data_list[:amount]
