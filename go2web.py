#!/usr/bin/env python3

import argparse
import requests
import re
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

class Go2Web:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        self.lang_to_cc = {
            'en': 'US',
            'de': 'DE',
            'fr': 'FR',
            'es': 'ES',
            'zh': 'CN',
            'ja': 'JP',
            'it': 'IT',
            'ru': 'RU',
            'pt': 'BR'
            # Add more if needed
        }

    def make_http_request(self, url):
        """Make an HTTP request and return clean text."""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Remove HTML tags
            clean_text = re.sub('<[^<]+?>', '', response.text)
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            
            return clean_text
        except requests.RequestException as e:
            return f"Error fetching URL: {e}"

    def search_bing(self, query, lang='en'):
        """Perform a web search using Bing with optional language support."""
        try:
            encoded_query = quote_plus(query)
            cc = self.lang_to_cc.get(lang, 'US')
            search_url = f"https://www.bing.com/search?q={encoded_query}&setlang={lang}&cc={cc}"
            
            response = requests.get(search_url, headers=self.headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            for i, result in enumerate(soup.find_all('li', class_='b_algo'), 1):
                link = result.find('a')
                if link and link.get('href'):
                    title = result.find('h2')
                    title_text = title.get_text(strip=True) if title else 'Untitled'
                    url = link.get('href')
                    # Print title + clickable URL
                    results.append(f"{i}. {title_text}\n\033[94m{url}\033[0m")
                if i == 10:
                    break
            return results if results else ["No search results found."]
        except requests.RequestException as e:
            return [f"Search error: {e}"]

def main():
    parser = argparse.ArgumentParser(description="Go2Web CLI Tool", add_help=False)
    parser.add_argument('-u', '--url', type=str, help='URL to request')
    parser.add_argument('-s', '--search', type=str, help='Search term')
    parser.add_argument('-l', '--lang', type=str, default='en', help='Language code (e.g., en, de, fr, zh)')
    parser.add_argument('-h', '--help', action='store_true', help='Show help')

    args = parser.parse_args()
    go2web = Go2Web()

    if args.help:
        parser.print_help()
        return

    if args.url:
        print(go2web.make_http_request(args.url))

    if args.search:
        results = go2web.search_bing(args.search)
        for result in results:
            print(result)

    # If no arguments provided, show help
    if not (args.url or args.search or args.help):
        parser.print_help()

if __name__ == "__main__":
    main()