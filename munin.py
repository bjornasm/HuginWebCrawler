from bs4 import BeautifulSoup
import httplib
import urlparse
import urllib2

def parent_link(link):
    #Check if parent or child - how? What defines a parent?
    #A parent link is at the same domain as the main link, so i just need to strip it for everything before and after domain.no
    #and check if that matches the stripped links in urlsToCrawl_Parent

def saveState():
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
 
def valid_link(link):
	# http://stackoverflow.com/questions/2924422
    good_codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]
    return get_server_status_code(link) in good_codes

def fetch_webpage(url):
	webpage = urllib2.urlopen(url)
	return webpage

def fetch_links(webpage):
	html = webpage.read()
    soup = BeautifulSoup(html)
    links = soup.find_all("a")
    return links

def schedule_link(link):
	if valid_link(link):
		if parent_link(link):
			urlsToCrawl_Parent.append(link)
		else:
			urlsToCrawl_Child.append(link)
		#Puts the links in the queue

def havent_visited(link):
	if link in urlsToCrawl_Parent or link in urlsToCrawl_Child:
        return false
    else:
        return true

def crawl(url):
    webpage = fetch_webpage(url)
    links = fetch_links(webpage)
    for link in links:
        if havent_visited(link):
              schedule_link(link)

if __name__ == "__main__":
    urls_Crawled = []
    urlsToCrawl_Parent = []
    urlsToCrawl_Child = []

    #Add a method to read from file if exist.
    #Add a method to traverse and start the call.