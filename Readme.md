# Hugin Web Crawler

#### A minimal webcrawler

This is a minimal webcrawler written in Python as a coding excercise done over a day. I have commented it excessively to make the readability of the code better. 

__Assumptions__:

* I can use python libraries

* I do not need to store the actual website pages on disk, the key point is to gather URLs

* Because of the time limit i have taken the freedom of not implementing local storage of the URL queue (see first point under 'Limitations of the task')

__Limitations__:
	
* The crawler will not be able to assume operation if shut down. Because the time limit of this task i omitted this point, even though it easily can be implemented. The fastes way would be by writing the URL lists to a file on disk. This would on a other hand require many read/write operations, and could make this code slower for this demonstration.
	
* The crawler are limited to the file endings and the domains in the allowed list, it can be run without a allowed list, but then it could be using bandwith to load pictures and other files on the server not relevant for web crawling.
	
* The crawler is very verboose and has many if statements - this could probably be implemented better.

__Future improvements__:

* __Scaling of the crawler__ I would implement a better work distributor that could distribute the URL queue dynamically to different crawlers on different machines/nodes. I would distibrute the unique domains (http://telenor.com, http://ap.no etc), so every crawler would only crawl one domain at the time, as well as submit all the children URLs (i.e URL for other domains) back to the distributor for distribution.

* __Saving the URL queue__ to a file or to a database so it can resume if shut down, and so that the work can be viewed while running.

* Utilizing a selection policy, f.ex a point system for the domains to prioritize the crawling.

* Saving the date of the last time a website was crawled so we could implement a re-visiting policy based on this.

* Saving the list of visited URLs in a heap or another data structure better suited for searching, this is especially important when the amount of data gets bigger.

* Visiting the robots exclusion protocol, robots.txt, on every domain before crawling it. This is done to avoid the parts of the servers that should not be accessed by the crawler.

* URL normalization - have a better normalization of URLs to avoid re-entering the same page.



