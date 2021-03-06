from bs4 import BeautifulSoup
import httplib
import urlparse
import urllib
import time

import cProfile

def sanitize(url, parent):
    if is_internal_link(url):
        if parent.endswith("/") or url.startswith("/"):
            return parent + url
        else:
            return parent + "/" + url
    return url

def is_internal_link(url):
    return not url.startswith("http")

def hostname(link):
    #Check if parent or child - how? What defines a parent?
    #A parent link is at the same domain as the main link, so i just need to strip it for everything before and after domain.no
    #and check if that matches the stripped links in urlsToCrawl_Parent
    return urlparse.urlparse(link).hostname

#def saveState():
    #Lagre til fil

def get_server_status_code(link):
    # http://stackoverflow.com/questions/1140661
    host, path = urlparse.urlparse(link)[1:3]
    try:
        conn = httplib.HTTPConnection(host)
        conn.request('HEAD', path)
        return conn.getresponse().status
    except StandardError:
        return None
 
def is_valid_link(link):
    link = sanitize(link, hostname(urlsToCrawl_Parent[0]))
	# http://stackoverflow.com/questions/2924422
    good_codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]
    return get_server_status_code(link) in good_codes

def fetch_webpage(url):
	webpage = urllib.urlopen(url).read()
	return webpage

def fetch_links(webpage):
    soup = BeautifulSoup(webpage)
    links = soup.find_all("a", href=True)
    return links

def schedule_link(link):
    if is_valid_link(link):    
        if hostname(link) in urlsToCrawl_Parent[0]:
            urlsToCrawl_Parent.append(link)
        else:
            urlsToCrawl_Child.append(link)
            #Puts the links in the queue

def havent_visited(link):
    if link not in urls_Crawled and link not in urlsToCrawl_Parent and	 link not in urlsToCrawl_Child:
        return True
    else:
        return False

def crawl(url):
    webpage = fetch_webpage(url)
    links = fetch_links(webpage)
    for link in links:
        link = link['href'] #This is not done on a good way at all, should clearly do this in fetch_links?
        if havent_visited(link):
            schedule_link(link)

def prepareCrawl():
    target = urlsToCrawl_Parent.pop(0)
    crawl(target)
    urls_Crawled.append(target)

if __name__ == "__main__":
#def main():
    urls_Crawled = []
    urlsToCrawl_Parent = []
    urlsToCrawl_Child = []

    #Add a method to read from file if exist.
    urlsToCrawl_Parent.append("http://www.telenor.no/")
    while (len(urls_Crawled) < 5):
        if (len(urlsToCrawl_Parent) > 0):
            prepareCrawl()

        elif (len(urlsToCrawl_Child) > 0):
            urlsToCrawl_Parent.append(urlsToCrawl_Child[0])
            prepareCrawl()

        #Add a method to traverse and start the call.
    print len(urlsToCrawl_Parent) + len(urlsToCrawl_Child) + len(urls_Crawled)

#cProfile.run('main()')
