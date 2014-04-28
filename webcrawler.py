import urllib
import re

# This is the 'input' parameteres - the depth parameter indicates how deep the crawler gets, i.e how many different websites
# it visits, while the max_url gives how many different url it's gonna crawl. This is implemented to give a better control of
# the runtime of this crawler.
starturl = "http://www.telenor.com"
depth = 3
max_urls = 100

# This is simple lists to hold the urls crawled, the parent urls, i.e the 'local' urls on the current page, while the 
# child urls are urls for other web pages found on a parent page.

urls_crawled = []
urlsToCrawl_Parent = []
urlsToCrawl_Child = []

# To avoid crawl links to pictures (.jpeg) and other files i have made an list over allowed url-endings.
allowList = ['html', 'htm', 'php', 'no', 'com', 'net', 'org', 'se', 'dk']

# The input parameters is the url the crawler is gonna crawl.
def crawler(url):

	# The crawler find links by utilizing pythons urllib and the href tag
	for new_url in re.findall('''href=["'](.[^"']+)["']''', urllib.urlopen(url).read()):

		# A bit ugly, but this is to be sure that the new url is not in the urls already crawled, or scheduled for crawling, a check for if it's a HTML element that have escape the regex, or a "link" to a html class on the same page, and that the url ending is in the allowed list
		if not any(new_url in word for word in urls_crawled) and not any(new_url in word for word in urlsToCrawl_Parent) and not any(new_url in word for word in urlsToCrawl_Child) and '<' not in new_url and '#' not in new_url and any(word in new_url.split('.')[-1] for word in allowList):
			
			# If the url is in the new url, f.ex http://www.telenor.com is inside http://www.telenor.com/no/personvern/feed
			# the latter should be appended in the parent list as i prioritize the local urls first.
			if url in new_url:
				urlsToCrawl_Parent.append(new_url)

			# Another check, this is if we deal with a local link on the form /no/personvern/feed/
			elif "http" not in new_url and "www" not in new_url:

				# To better store local links, f.ex /no/personvern/feed/ forward slash (/) is omitted
				new_url = re.sub('^\/*', '', new_url)
				new_url = re.sub('\/*$', '', new_url)
				url = re.sub('\/*$', '', url)

				# The /no/personvern/feed/ url is stored as www.telenor.com/no/personvern/feed/
				urlsToCrawl_Parent.append(url+"/"+new_url)

			# If we are not dealing with an local URL we are dealing with a child URL 
			else:
				urlsToCrawl_Child.append(new_url)

	# We are done crawling this URL and thus we remove it from the list, and we add it to the list over urls crawled.
	urlsToCrawl_Parent.pop(0)
	urls_crawled.append(url)

# Here we write the list over urls crawled to a txt file
def writetofile(urls):

	with open('CrawledURLs.txt','w') as file:
		for item in urls:
		    print>>file, item

if __name__ == "__main__":

	# We start to append the starturl
	urlsToCrawl_Parent.append(starturl)

	# A while loop is utilized so we crawl the next url in the list until we have sucessfully crawled the amount of 
	# URLs wanted, or until we have reached the depth specified.
	d = 0
	while (d<=depth) and (len(urls_crawled) < max_urls):
	  	
	  	# A while loop is utilized to always crawl the parent URLs first
	  	while urlsToCrawl_Parent and (len(urls_crawled) < max_urls):

	  		# An extra check if the url is already crawled, if not we crawl this url
	  		if urlsToCrawl_Parent[0] in urls_crawled:
	  			urlsToCrawl_Parent.pop(0)
	  		else:
	  			crawler(urlsToCrawl_Parent[0])

	  	# When we are done with all the URLs in the parent list, we add the first URL in the children list
	 	urlsToCrawl_Parent.append(urlsToCrawl_Child[0])
	 	urlsToCrawl_Child.pop(0)

	 	d += 1

	writetofile(urls_crawled)
