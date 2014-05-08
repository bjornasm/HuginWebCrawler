import urllib
import re
import os

# The parameter is the url the crawler is gonna crawl.
def crawler(url):
	# The crawler find links by utilizing pythons urllib and the href tag
	for new_url in re.findall('''href=["'](.[^"']+)["']''', urllib.urlopen(url).read()): 
        	new_url = re.sub('\/*$', '', new_url)

		# A bit ugly, but this is to be sure that the new url is not in the urls already crawled, or scheduled for crawling, a check for if it's a HTML element that have escape the regex, or a "link" to a html class on the same page, and that the url ending is in the allowed list
		if not any(new_url in word for word in urls_Crawled) and not any(new_url in word for word in urlsToCrawl_Parent)and not any(new_url in word for word in urlsToCrawl_Child) and '<' not in new_url and '#' not in new_url and any(word in new_url.split('.')[-1] for word in allowedList) and 'https://wow' not in new_url and 'mailto' not in new_url:
			
			# If the url is in the new url, f.ex http://www.telenor.com is inside http://www.telenor.com/no/personvern/feed
			# the latter should be appended in the parent list as i prioritize the local urls first.
			if url.replace("http://","").replace("www.","").split('/', 1)[0] in new_url:
				urlsToCrawl_Parent.append(new_url)

			# Another check, this is if we deal with a local link on the form /no/personvern/feed/
			elif new_url.startswith('/'):
				# To better store local links, f.ex /no/personvern/feed/ forward slash (/) is omitted
				new_url = re.sub('\/*$', '', new_url)
				url = re.sub('\/*$', '', url)

				# The /no/personvern/feed/ url is stored as www.telenor.com/no/personvern/feed/
				urlsToCrawl_Parent.append(url+new_url)

			# If we are not dealing with an local URL we are dealing with a child URL 
			else:
				urlsToCrawl_Child.append(new_url)

	# We are done crawling this URL and thus we remove it from the list, and we add it to the list over urls crawled.
	urlsToCrawl_Parent.pop(0)
	urls_Crawled.append(url)

	# A fast implemention of a "blind" saving of state so the program can be resumed after an error
	writetofile(urls_Crawled, 'URLsCrawled')
	writetofile(urlsToCrawl_Parent, 'parentURLs')
	writetofile(urlsToCrawl_Child, 'childURLs')

# Here we write the list over urls crawled to a txt file
def writetofile(urls, filename):

	with open(filename,'w') as file:
		for item in urls:
		    print>>file, item

if __name__ == "__main__":

	# This is the 'input' parameteres the max_url gives how many different url it's gonna crawl. 
	# this is implemented to give a better control of the runtime of this crawler.
	starturl = ""
	max_urls = 500

	if not os.path.exists('parentURLs') or not os.path.getsize('parentURLs') > 0 or not os.path.exists('childURLs') or not os.path.getsize('childURLs') > 0:
		
		# This is simple lists to hold the urls crawled, the parent urls, i.e the 'local' urls on the current page, while the 
		# child urls are urls for other web pages found on a parent page.
		urls_Crawled = []
		urlsToCrawl_Parent = []
		urlsToCrawl_Child = []

		# We start to append the starturl
		urlsToCrawl_Parent.append(starturl)

	else:
		with open('URLsCrawled', 'r') as f:
		    urls_Crawled = [line.rstrip('\n') for line in f]
		with open('parentURLs', 'r') as f:
		    urlsToCrawl_Parent = [line.rstrip('\n') for line in f]
		with open('childURLs', 'r') as f:
		    urlsToCrawl_Child = [line.rstrip('\n') for line in f]

	# To avoid crawl links to pictures (.jpeg) and other files i have made an list over allowed url-endings.
	allowedList = ['html', 'htm', 'php', 'jsp', 'jspx', 'asp', 'no', 'com', 'net', 'org', 'se', 'dk']

	# A while loop is utilized so we crawl the next url in the list until we have sucessfully crawled the amount of 
	# URLs wanted, or until we have reached the depth specified.
	while (len(urls_Crawled) < max_urls):
	  	
	  	# A while loop is utilized to always crawl the parent URLs first
	  	while urlsToCrawl_Parent and (len(urls_Crawled) < max_urls):

	  		# An extra check if the url is already crawled, if not we crawl this url
	  		if urlsToCrawl_Parent[0] in urls_Crawled:
	  			urlsToCrawl_Parent.pop(0)
	  		elif ('http://' in urlsToCrawl_Parent[0] or 'https://' in urlsToCrawl_Parent[0]):
					try:
					 	crawler(urlsToCrawl_Parent[0])
					except:
			 			urlsToCrawl_Parent.pop(0) 
			else:
				urlsToCrawl_Parent[0] = "http://"+urlsToCrawl_Parent[0]
				try:
				 	crawler(urlsToCrawl_Parent[0])
			 	except:
				 	urlsToCrawl_Parent.pop(0)

	  	# When we are done with all the URLs in the parent list, we add the first URL in the children list
	 	urlsToCrawl_Parent.append(urlsToCrawl_Child[0])
	 	urlsToCrawl_Child.pop(0)

	os.remove('childURLs')
	os.remove('parentURLs')
