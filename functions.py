import requests
from bs4 import BeautifulSoup
import os
import sys
import webbrowser
import newspaper
import helpers
import wikipedia
import re
import subprocess


def get_headlines(topic: str) -> dict:
    """Gives the user a list of headlines.

        Args:
            topic: the topic which a user specified (e.g. 'Ukraine situation')

        Returns:
            A dictionary containing headlines related to the user-specified topic, as well as the source for each headline
        """
    url = f'https://apnews.com/search?q={topic}#nt=navsearch'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    titles = soup.find_all(class_="PagePromoContentIcons-text")
    articles = {}
    for title in titles:
        articles[title.text]="AP"
    url = f'https://www.reuters.com/site-search/?query={topic}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    titles = soup.find_all(class_="text__text__1FZLe text__inherit-color__3208F text__medium__1kbOh text__heading_6__1qUJ5 heading__base__2T28j heading__heading_6__RtD9P title__heading__s7Jan")
    for title in titles:
        articles[title.text]="Reuters"
    buff = {}
    for article in articles.keys():
        if helpers.jaccard_distance(set(article.lower().split(" ")), set(topic.lower().split(" "))) > 0.5:
            buff[article] = articles[article]
    articles = buff
    del buff

    return articles

def open_app(name: str)->str:
    """Opens a user-specified app, such as Discord, Google Chrome, etc.

            Args:
                name: the name of the app to open

            Returns:
                A string which either certifies that the app was opened or explaining any errors which occurred
    """

    if sys.platform == 'darwin':
        files = helpers.find_file_in_directories(name)
        for file in files:
            os.system(f"open {file}")
        return "successfully opened the app"
    elif sys.platform == 'win32':
        try:
            subprocess.Popen(f"{name}.exe")
            return "successfully opened the application"
        except FileNotFoundError:
            return "No such file exists"
        except Exception as e:
            return f"Error: {e}"
    elif sys.platform == 'linux2':
        from google import genai
        directories = ['/']
        matching_files = []

        for directory in directories:
            if os.path.exists(directory):
                for root, dirs, files in os.walk(directory):
                    for file in dirs:
                        # Case-insensitive search with option for case-sensitive matching
                        if file.lower().startswith(name.lower()):
                            matching_files.append(os.path.join(root, file))
        client = genai.Client(api_key=os.getenv("API_KEY"))
        config = {
            "tools": [helpers.run_application_linux_with_path]
        }
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Please decide which of the following files to execute and execute them:\n {'\n'.join(matching_files)}",
            config=config,
        )
        return response.text


def leave():
    """Quits/closes the application if the user requests it.

            Args:
                Nothing

            Returns:
                Nothing
            """
    sys.exit(0)

def open_website(url: str)->str:
    """Opens a user-specified website

            Args:
                url: the url of the website to open

            Returns:
                A String certifying that the page was opened
    """
    if 'https://' or "http://" in url:
        webbrowser.open(url)  # Open the link in the default web browser
    else:
        webbrowser.open('https://' + url)
    return f"Successfully opened {url}"

def get_news(topic: str) -> str:
    """
    Returns the text of news articles relating to the topic for the AI model to answer user questions about the news.
    Args:
        topic: the topic which a user specified (e.g. 'Ukraine situation', 'White House Press Conference')
    Returns:
        A string containing the text of some news articles from the AP and Reuters.
    """
    url = f'https://apnews.com/search?q={topic}#nt=navsearch'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    titles = soup.find_all("a", class_="Link", href=True)
    links = []
    for titl in titles[:9]:
        links.append(titl['href'])
        print(titl['href'])
    del titles
    url = f'https://san.com/?s={topic}&post_type=sa_core_content'
    page = requests.get(url)
    #print(page.content)
    soup = BeautifulSoup(page.content, 'html.parser')
    titles = soup.find_all("a", class_="search-result__image")
    print(titles)
    for titl in titles[:9]:
        links.append(titl['href'])
        print(titl['href'])
    del titles

    #text extraction
    text = []
    for link in links:
        article = newspaper.Article(link)
        article.download()
        article.parse()
        if "The Associated Press is an independent global news organization" in article.text:
            pass
        else:
            text.append(article.text)
    print(text)
    return " ".join(text)

def wikipedia_summary(topic: str) -> str:
    """Returns the summary of the Wikipedia article.

            Args:
                topic: the topic which a user specified (e.g. 'Abraham Lincoln')

            Returns:
                A short summary of the wikipedia article
    """
    return wikipedia.summary(topic, sentences=5)




if __name__ == "__main__":
    get_news("Gaza")