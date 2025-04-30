#!/usr/bin/env python3
import argparse
import re
import socket
import ssl
from urllib.parse import quote_plus, urlparse
from bs4 import BeautifulSoup

class CustomHTTPRequest:
    """A custom implementation of HTTP requests without external libraries."""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
    def get(self, url, headers=None):
        """Make a GET request to the specified URL."""
        combined_headers = self.headers.copy()
        if headers:
            combined_headers.update(headers)
        
        parsed_url = urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path
        if not path:
            path = "/"
        if parsed_url.query:
            path += "?" + parsed_url.query
            
        # Determine if HTTPS or HTTP
        is_https = parsed_url.scheme == 'https'
        port = 443 if is_https else 80
        
        # Prepare request
        request = f"GET {path} HTTP/1.1\r\n"
        request += f"Host: {host}\r\n"
        
        # Add headers
        for key, value in combined_headers.items():
            request += f"{key}: {value}\r\n"
        
        request += "Connection: close\r\n\r\n"
        
        # Create socket connection
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            if is_https:
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=host)
                
            sock.connect((host, port))
            sock.sendall(request.encode())
            
            # Receive response
            response = b""
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                response += data
                
            sock.close()
            
            # Parse response
            response_str = response.decode('utf-8', errors='replace')
            headers_end = response_str.find('\r\n\r\n')
            
            if headers_end == -1:
                raise Exception("Invalid HTTP response")
                
            headers = response_str[:headers_end]
            body = response_str[headers_end + 4:]
            
            # Check status code
            status_line = headers.split('\r\n')[0]
            status_code = int(status_line.split(' ')[1])
            
            return Response(status_code, body, headers)
            
        except Exception as e:
            raise RequestException(f"Error during request: {e}")
            
class Response:
    """Simple response class to mimic requests.Response."""
    
    def __init__(self, status_code, text, headers):
        self.status_code = status_code
        self.text = text
        self.headers = headers
        
    def raise_for_status(self):
        """Raises an exception if the status code indicates an error."""
        if self.status_code >= 400:
            raise RequestException(f"HTTP Error: {self.status_code}")

class RequestException(Exception):
    """Exception class for request errors."""
    pass

class Go2Web:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        self.http_client = CustomHTTPRequest()
        
    def make_http_request(self, url):
        """Make an HTTP request and return clean text."""
        try:
            response = self.http_client.get(url, headers=self.headers)
            response.raise_for_status()
            # Remove HTML tags
            clean_text = re.sub('<[^<]+?>', '', response.text)
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            return clean_text
        except RequestException as e:
            return f"Error fetching URL: {e}"
            
    def search_web(self, query):
        """Perform a web search using Brave"""
        try:
            encoded_query = quote_plus(query)
            search_url = f"https://search.brave.com/search?q={encoded_query}"
            response = self.http_client.get(search_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            result_blocks = soup.find_all('div', class_='snippet')
            results = []
            for i, block in enumerate(result_blocks):
                a_tag = block.find('a', href=True)
                title_tag = block.find('h3') or block.find('span')
                if a_tag and title_tag:
                    url = a_tag['href']
                    title = title_tag.get_text(strip=True)
                    results.append(f"{i+1}. {title}\n\033[94m{url}\033[0m")
                if i == 10:
                    break
            return results if results else ["No search results found."]
        except RequestException as e:
            return [f"Search error: {e}"]
            
def main():
    parser = argparse.ArgumentParser(description="Go2Web CLI Tool", add_help=False)
    parser.add_argument('-u', '--url', type=str, help='URL to request')
    parser.add_argument('-s', '--search', type=str, help='Search term')
    parser.add_argument('-h', '--help', action='store_true', help='Show help')
    args = parser.parse_args()
    
    go2web = Go2Web()
    
    if args.help:
        parser.print_help()
        return
        
    if args.url:
        print(go2web.make_http_request(args.url))
        
    if args.search:
        results = go2web.search_web(args.search)
        for result in results:
            print(result)
            
    # If no arguments provided, show help
    if not (args.url or args.search or args.help):
        parser.print_help()
        
if __name__ == "__main__":
    main()