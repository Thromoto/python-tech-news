from tech_news.database import search_news
from datetime import datetime


# Requisito 7
def search_by_title(title):
    result = search_news({"title": {"$regex": title, "$options": "i"}})

    news_list = [(news["title"], news["url"]) for news in result]

    return news_list


# Requisito 8
def search_by_date(date):
    try:
        format_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')

        result = search_news(
            {"timestamp": {"$regex": format_date, "$options": "i"}})

        news_list = [(news["title"], news["url"]) for news in result]

        return news_list
    except ValueError:
        raise ValueError('Data inválida')


# Requisito 9
def search_by_category(category):
    result = search_news({"category": {"$regex": category, "$options": "i"}})

    news_list = [(news["title"], news["url"]) for news in result]

    return news_list
