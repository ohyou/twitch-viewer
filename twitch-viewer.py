import requests, subprocess, json, sys, threading, time, random

channel = "twitch.tv/"
threads = []

def getChannel():
	# Reading the channel name - passed as an argument to this script
	if len(sys.argv) >= 2:
		global channel
		channel += sys.argv[1]
	else:
		print "An error has occurred while trying to read arguments."
		sys.exit(1)

def getProxies():
	# Reading the list of proxies
	try:
		lines = [line.rstrip("\n") for line in open("proxylist.txt")]
	except IOError as e:
		print "An error has occurred while trying to read the list of proxies: %s" % e.strerror
		sys.exit(1)
		
	return lines

def getUrl():
	# Getting the json with all data regarding the stream
	try:
		response = subprocess.Popen(["livestreamer", "twitch/tv/tv", "-j"], stdout=subprocess.PIPE).communicate()[0]
	except subprocess.CalledProcessError as e:
		print "An error has occurred while trying to get the stream data."
		sys.exit(1)
		
	# Decoding the url to the worst quality of the stream
	try:
		url = json.loads(response)['streams']['worst']['url']
	except (ValueError, KeyError):
		print "An error has occurred while trying to process the response."
		sys.exit(1)
		
	return url

def openUrl(url, proxy):
	while True:
		# Trying to make it look "realistic" by adding a random delay
		time.sleep(random.randint(5, 15))
		
		# Sending the HEAD request using a specific proxy
		try:
			requests.head(url, proxies=proxy)
			print "Sent HEAD request with %s" % proxy["http"]
		except requests.exceptions.Timeout as e:
			print "  Timeout error for %s" % proxy["http"]
		except requests.exceptions.ConnectionError as e:
			print "  Connection error for %s" % proxy["http"]
		
def prepareThreads():
	global threads
	proxies = getProxies()

	if len(proxies) < 1:
		print "An error has occurred while preparing the threads: Not enough proxy servers."
		sys.exit(1)
	
	for proxy in proxies:
		# Preparing the thread and giving it its own proxy
		threads.append(threading.Thread(target=openUrl, kwargs={"url" : getUrl(), "proxy" : {"http" : proxy}}))
		
if __name__ == "__main__":
	getChannel()
	prepareThreads()
	
	# Starting up the threads
	for thread in threads:
		thread.daemon = True
		thread.start()
	
	# Running infinitely
	while True:
		time.sleep(1)