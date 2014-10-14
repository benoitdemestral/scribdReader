import os.path
import urllib.request

# HANDLE TIMEOUT
url = input("Enter URL to a scribd doc (images only, no text support yet.)\n")
if not ("http://" in url) and ("scribd.com" in url) and ("/doc/" in url):
	url = "http://fr.scribd.com/doc/38812967/Teach-Yourself-Russian-Grammar"
	# Default url if the entered one is wrong. Would be better with a regex match.
request = urllib.request.Request(url)
request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36')
page = urllib.request.urlopen(request,None,timeout=10)
html = page.read()
src = str(html.decode("utf-8"))
prefixLocation = src.find("docManager.assetPrefix = \"")
# check for -1
prefix = prefixLocation + len("docManager.assetPrefix = \"")
assetPrefix = src[prefix:][:src[prefix:].find("\"")]

os.mkdir("scribd_crawler_output")

lines = src.splitlines()
i = 0
for line in lines:
	findSpot = line.find(assetPrefix)
	if findSpot != -1:
		if ".jpg" in line:
			i += 1
			url = line[line.find(assetPrefix) - len("http://html.scribd.com/"):]
			url = url[:url.find("\"")]
			file_name = "Page_"
			file_name += str(i)
			complete_path = os.path.abspath("scribd_crawler_output/%s.jpg" % file_name)
			image = open(complete_path, "wb")
			image.write(urllib.request.urlopen(url).read())
			image.close()
			print("Saved page",i)
		elif ".json" in line:
			i += 1
			url = line[line.find(assetPrefix) - len("http://html2.scribdassets.com/"):]
			url = url[:url.find("\"")]
			request = urllib.request.Request(url)
			request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36')
			page = urllib.request.urlopen(request,None,timeout=10)
			html = page.read()
			src = str(html)
			imgloc = src.find("orig")
			imgloc += len("orig=\\\\\"")	
			img_url = src[imgloc:]
			img_url = img_url[:img_url.find("\\")]
			file_name = "Page_"
			file_name += str(i)
			complete_path = os.path.abspath("scribd_crawler_output/%s.jpg" % file_name)
			image = open(complete_path, "wb")
			image.write(urllib.request.urlopen(img_url).read())
			image.close()
			print("Saved page",i)
print("All done.")
