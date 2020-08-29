from django.db import models
from django.conf import settings

from datetime import datetime
import json


class NewsRepository:

    @staticmethod
    def load_all(query: str = None):
        with open(settings.NEWS_JSON_PATH, 'r') as news_file:
            news = json.load(news_file)
            if query:
                return list(filter(lambda x: query in x['title'], news))
            else:
                return news

    @staticmethod
    def load_by_link(link: int):
        with open(settings.NEWS_JSON_PATH, 'r') as news_file:
            news = json.load(news_file)
            for it in news:
                if it['link'] == link:
                    return it
            return None

    @staticmethod
    def get_next_link():
        with open(settings.NEWS_JSON_PATH, 'r') as news_file:
            news = json.load(news_file)
            max_link = 0
            for it in news:
                if it['link'] > max_link:
                    max_link = it['link']
            return max_link + 1

    @staticmethod
    def save_news(title: str, text: str):
        news = {
            'link': NewsRepository.get_next_link(),
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'title': title,
            'text': text
        }
        all_news = NewsRepository.load_all()
        all_news.append(news)
        with open(settings.NEWS_JSON_PATH, 'w') as news_file:
            json.dump(all_news, news_file)
