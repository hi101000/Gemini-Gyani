import requests
from bs4 import BeautifulSoup
import os
import sys
import webbrowser

import helpers


def get_news(topic: str) -> list:
    """Gives the user a list of headlines.

        Args:
            topic: the topic which a user specified (e.g. 'Ukraine situation')

        Returns:
            A list containing headlines related to the user-specified topic.
        """
    url = f'https://apnews.com/search?q={topic}#nt=navsearch'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    titles = soup.find_all(class_="PagePromoContentIcons-text")
    articles = []
    for title in titles:
        articles.append(title.text)
    return articles

def open_app(name: str)->None:
    """Opens a user-specified app
            Args:
                name: the name of the app to open
            Returns:
                Nothing
    """
    files = helpers.find_file_in_directories(name)
    for file in files:
        if sys.platform == 'darwin':
            os.system(f"open {file}")

def leave():
    """Quits the application if the user requests it.
            Args:
                Nothing

            Returns:
                Nothing
            """
    sys.exit(0)