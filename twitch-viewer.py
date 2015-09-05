import requests, subprocess, json, sys, multiprocessing, time, random

channel_url = "twitch.tv/"
processes = []

def getChannel():
	# Reading the channel name - passed as an argument to this script
	if len(sys.argv) >= 2:
		global channel_url
		channel_url += sys.argv[1]
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
		response = subprocess.Popen(["livestreamer", channel_url , "-j"], stdout=subprocess.PIPE).communicate()[0]
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
	# Explicitly opening the session
	session = requests.Session()
	
	# Sending HEAD requests
	while True:
		try:
			response = session.head(url, proxies=proxy)
			print "Sent HEAD request with %s" % proxy["http"]
			time.sleep(20)
			response.connection.close()
		except requests.exceptions.Timeout:
			print "  Timeout error for %s" % proxy["http"]
		except requests.exceptions.ConnectionError:
			print "  Connection error for %s" % proxy["http"]
		
def prepareProcesses():
	global processes
	proxies = getProxies()

	if len(proxies) < 1:
		print "An error has occurred while preparing the process: Not enough proxy servers."
		sys.exit(1)
	
	for proxy in proxies:
		# Preparing the process and giving it its own proxy
		processes.append(multiprocessing.Process(target=openUrl, kwargs={"url" : getUrl(), "proxy" : {"http" : proxy}}))
		
if __name__ == "__main__":
	getChannel()
	print "Obtained the channel"
	prepareProcesses()
	print "Prepared the processes"
	
	# Starting up the processes
	for process in processes:
		time.sleep(random.randint(1, 5))
		process.daemon = True
		process.start()
	
	# Running infinitely
	while True:
		time.sleep(1)