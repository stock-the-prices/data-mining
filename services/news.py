import logging
import pprint
import requests


class News(object):
    results_per_page = 20               # num articles per page of query results

    def __init__(self, api_key: str, article_search_url: str):
        self.api_key = api_key
        self.article_search_url = article_search_url

    def create_article_search_payload(self, q: str, start_date: str, end_date: str, page: int) -> dict:
        payload = {'apiKey': self.api_key, 'q': q, 'language': 'en', 'page': page}
        if start_date is not None:
            payload['from'] = start_date
        if end_date is not None:
            payload['to'] = end_date
        return payload

    def get_articles(self, query: str, num_articles, start_date=None, end_date=None):
        articles = []
        for page in range(1, int(num_articles/self.results_per_page) + 1 + 1):
            payload = self.create_article_search_payload(query, start_date, end_date, page)
            r = requests.get(self.article_search_url, params=payload)

            if r.status_code == 200:
                raw_articles = r.json()['articles']
                articles += raw_articles[:min(num_articles - len(articles), 20)]
            # else throw

        return articles
