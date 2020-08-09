import collections
import colorama
import requests
import sys
import os

from bs4 import BeautifulSoup


class Browser:
    def __init__(self, local_dir):
        self.local_dir = local_dir
        self.history = collections.deque()
        self.shortened_cache = {}
        self.previous_page = None

    def load_from_cache(self, shortened_url):
        if shortened_url in self.shortened_cache:
            with open(self.shortened_cache[shortened_url]) as local_file:
                return local_file.read()

    def back(self):
        if len(self.history) > 0:
            return self.load_from_cache(self.history.pop())
        else:
            return None

    def load(self, url):
        response = requests.get('https://' + url)
        soup = BeautifulSoup(response.content, 'html.parser')
        tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li'])

        shortened_ulr = website[:website.rindex('.')]
        local_file = self.local_dir + shortened_ulr
        with open(local_file, mode='w') as file:
            for tag in tags:
                if tag.name == 'a':
                    file.write(colorama.Fore.BLUE + tag.text)
                else:
                    file.write(tag.text)

        self.shortened_cache[shortened_ulr] = local_file
        if self.previous_page is not None:
            self.history.append(self.previous_page)
        self.previous_page = shortened_ulr

        return self.load_from_cache(shortened_ulr)


args = sys.argv
if len(args) != 2:
    print('You should specify folder for storing files as input parameter')
    exit(-1)

directory = args[1]
if not directory.endswith('/'):
    directory += '/'
os.makedirs(directory, exist_ok=True)

browser = Browser(directory)
colorama.init()

while True:
    command = input('> ')
    if command == 'exit':
        break
    elif command == 'back':
        history_content = browser.back()
        if history_content is not None:
            print(history_content)
    else:
        website = command
        cache_content = browser.load_from_cache(website)
        if cache_content is not None:
            print(cache_content)
            continue

        if '.' not in website:
            print('Error: Incorrect URL')
            continue

        loaded_content = browser.load(website)
        if loaded_content is None:
            print('Error: Incorrect URL')
        else:
            print(loaded_content)
