# Go2Web

A lightweight, dependency-free CLI tool for making HTTP requests and performing web searches directly from your terminal.

## Features

- **Zero External Dependencies**: Implements its own HTTP client with socket-based connections
- **Web Search**: Search the web with Brave Search and view results in your terminal
- **Direct Content Fetching**: Retrieve and display web content for any URL
- **Search Result Navigation**: Access specific search results with a single command
- **Persistent Caching**: Save search results locally to reduce network requests
- **Clean Output Formatting**: Colored output for better readability

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/go2web.git
cd go2web
```

2. Make the script executable:
```bash
chmod +x go2web.py
```

3. Optional: Create a symbolic link to use the tool from anywhere:
```bash
sudo ln -s $(pwd)/go2web.py /usr/local/bin/go2web
```

## Usage

### Command Line Options

```
usage: go2web.py [-u URL] [-s SEARCH] [-a SEARCH_TERM RESULT_NUMBER] [-c] [-h]

Go2Web CLI Tool

optional arguments:
  -u URL, --url URL     URL to request
  -s SEARCH, --search SEARCH
                        Search term
  -a SEARCH_TERM RESULT_NUMBER, --access SEARCH_TERM RESULT_NUMBER
                        Access a specific search result by number (e.g., -a "python tutorial" 3)
  -c, --clear-cache     Clear the search cache
  -h, --help            Show help
```

### Examples

#### Make a Direct HTTP Request

Fetch and display the content of a specific URL:

```bash
./go2web.py -u https://example.com
```

#### Search the Web

Search the web for a specific term:

```bash
./go2web.py -s "python tutorial"
```

This will display a list of search results with titles and URLs.

#### Access a Specific Search Result

Search for a term and directly access one of the results by its number:

```bash
./go2web.py -a "python tutorial" 3
```

This will search for "python tutorial", then fetch and display the content of the 3rd result.

#### Clear the Cache

Remove all cached search results:

```bash
./go2web.py -c
```

## How It Works

Go2Web implements its own HTTP client using Python's built-in `socket` and `ssl` modules, eliminating the need for external dependencies like `requests`. It handles:

1. Socket connections for both HTTP and HTTPS
2. HTTP headers and request formatting
3. Response parsing and error handling
4. HTML cleaning for better readability

For search functionality, it:
1. Connects to Brave Search
2. Parses the search results page with BeautifulSoup
3. Extracts and displays titles and URLs
4. Caches results in `~/.go2web_cache/` for faster repeat searches

## Technical Details

- **Custom HTTP Implementation**: Uses raw socket connections instead of high-level libraries
- **SSL Support**: Handles HTTPS connections securely
- **Persistent Cache**: Stores search results in JSON format with 24-hour expiration
- **Error Handling**: Robust error handling throughout the code
- **Output Formatting**: Uses ANSI color codes for better terminal output

## Requirements

- Python 3.6+
- BeautifulSoup4 (for HTML parsing)

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request