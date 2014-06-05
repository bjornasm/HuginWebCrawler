import httplib
import urlparse
import urllib2

def get_server_status_code(link):
    # http://stackoverflow.com/questions/1140661
    host, path = urlparse.urlparse(link)[1:3]    # elems [1] and [2] hmmm hva er dette
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

def fetch_links(page):
	#fetch all the links on the webpage

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

