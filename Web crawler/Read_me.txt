FOCUSED CRAWLER/SPIDER
To run:
The file can be run in three of the following ways:
1. python crawl.py
2. python crawl.py "<Seed URL>" "<Keyword>"
	For example: python crawl.py "http://en.wikipedia.org/wiki/Hugh_of_Saint-Cher" "concordance"
3. python crawl.py "<Seed URL>"
	For example: python crawl.py "http://en.wikipedia.org/wiki/Hugh_of_Saint-Cher"

I have imported the following libraries:
urllib2
time
from bs4 : BeautifulSoup
from urlparse : urljoin
sys
re
If the system doesn't have any of these not installed, kndly install before running the crawl.py file.