from bs4 import BeautifulSoup
import httplib
import urlparse
import urllib2

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
			#Schedule parent
		else:
			#Schedule child
		#Puts the links in the queue

def havent_visited(link):
	#Search algorithm to check set of visited

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