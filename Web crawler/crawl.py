__author__ = 'Himanshi'

# Importing of Libraries
import urllib2
import time
from bs4 import BeautifulSoup
from urlparse import urljoin
import sys
import re

base_seed = "http://en.wikipedia.org/wiki/"
main_wiki_page = "http://en.wikipedia.org/wiki/Main_Page"
maximum_depth = 5                   # Maximum depth till which the crawler would crawl
limit_of_urls = 1000                # Maximum number of URLs the crawler would crawl
wait_time = 1                       # Wait in seconds


def get_html(url):
    print "Waiting to create connection with: " + url
    time.sleep(wait_time)           # delay for "wait_time" seconds
    try:
        conn = urllib2.urlopen(url, timeout=5)
        print "Established connection with: " + url
        return conn.read()
    except:
        print "Could not Established connection with: " + url
        return ""


def match_keyword(text_from_page, keyword):
    if re.search(keyword, text_from_page, re.IGNORECASE):
        print "Keyword " + keyword + " found on the Page. Crawling now"
        return True
    else:
        print "Keyword " + keyword + " not found on the Page. Skipping crawl on this page."
        return False


def get_all_links(content, keyword):
    links = []
    soup = BeautifulSoup(content, 'html5lib')
    if keyword:
        if not match_keyword(soup.text.encode("utf-8"), keyword):
            return 0                # Function get_all_links return 0 in case keyword match not found
    print "Collecting URLs from current URL..."
    a_links = soup.find_all('a')
    for tag in a_links:
        href_link = tag.get('href')
        if href_link is not None and ":" not in href_link and "#" not in href_link:
            full_url_link = ((urljoin(base_seed, href_link)))
            if base_seed in full_url_link \
                    and main_wiki_page not in full_url_link:
                    links.append(full_url_link)
    return links


def crawl_web(seed, keyword):
    to_crawl = [seed]
    crawled = []
    next_depth = []
    depth = 1
    while to_crawl and depth <= maximum_depth:
        current_crawl = to_crawl.pop()
        print "current_crawl: " + current_crawl
        if current_crawl not in crawled:
            content = get_html(current_crawl)
            url_links = get_all_links(content, keyword)

            if url_links:
                if len(crawled) < limit_of_urls:
                    crawled.append(current_crawl)
                    next_depth.extend(url_links)
                else:
                    print "Reached limit to read Urls. Ending crawling now."
                    return crawled

        if not to_crawl:
            print "Nothing more to crawl in current depth"
            to_crawl = next_depth
            next_depth = []
            depth += 1
            print "Going to next depth now"
    if depth == maximum_depth - 1:
        print "Max Depth ", depth - 1, " reached. Exiting now !"
    else:
        print "Something's not right with the connection. Try again in a little bit."

    return crawled


def main():
    seed = "http://en.wikipedia.org/wiki/Hugh_of_Saint-Cher"
    keyword = ""
    args = sys.argv
    if len(args) == 2:              # crawl.py seed_url
        seed = args[1]              # changing value of seed to the value from the arguments
    elif len(args) == 3:            # crawl.py seed_url keyword
        seed = args[1]              # changing value of seed to the value from the arguments
        keyword = args[2]           # changing value of keyword to the value from the arguments

    output = crawl_web(seed, keyword)
    print "Writing crawled URLs to file..."
    fw = open('crawled_URLs.txt', 'w')
    fw.write('\n'.join(output) + '\n')


if __name__== '__main__':
    main()