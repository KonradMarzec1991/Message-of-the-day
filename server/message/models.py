"""
Module with models
"""
import random
from datetime import datetime
import requests


class RandomQuote:
    """
    `RandomQuote` class requests from external API a quote. If it fails
    (status_code is different than 200), class gets quotes from backup tuple
    """
    RANDOM_QUOTES_URL = 'https://api.forismatic.com/api/1.0/'
    BACKUP_QUOTES = (
        "The winds and waves are always on the side of the ablest navigators.",
        "To accomplish great things, we must dream as well as act.",
        "Nobody can do everything, but everybody can do something."
    )

    def __init__(self, method='getQuote', lang='en', resp_format='json'):
        self.method = method
        self.lang = lang
        self.format = resp_format

    @property
    def get_url(self):
        """
        Gets instance dict and connect it to base url - creates
        full path for requesting
        :return: plain string
        """
        params = [f'{key}={value}' for key, value in self.__dict__.items()]
        return self.RANDOM_QUOTES_URL + '?' + '&'.join(params)

    def get_backup_quote(self):
        """Gets random value from backup quotes"""
        return random.choice(self.BACKUP_QUOTES)

    def get_quote(self):
        """
        Requests from external API a quote.
        if impossible, gets quote from backup tuple
        """
        response = requests.get(self.get_url)
        if response.status_code == 200:
            text = response.json()
            quote = text.get('quoteText', None)
            if not quote:
                return self.get_backup_quote()
            return quote.strip()
        else:
            return self.get_backup_quote()

    def __str__(self):
        return f'RandomQuote({self.method}, {self.lang}, {self.format})'


class MessageOfTheDay:
    """
    `MessageOfTheDay` class enables creating instances with quotes and
    creation time
    """
    def __init__(self):
        self.content = RandomQuote().get_quote()
        self.createdAt = datetime.utcnow()

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return f'Message({self.content})'