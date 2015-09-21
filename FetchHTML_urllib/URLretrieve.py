import urllib, sys, time
#url = 'http://wallpaperswide.com/download/city_veins_2-wallpaper-1680x1260.jpg'
url = 'http://mirrors.rit.edu/backtrack/'

def Retriever(blocks,block_size,filesize):

	while blocks*block_size < filesize:
 		percent = int(blocks*block_size*100/filesize)
 		sys.stdout.write(" Downloading: " + url + " \r%2d%%"%percent)
 		sys.stdout.write("\n")
		sys.stdout.flush()
		time.sleep(1)

filename = url[url.rfind('/')+1:]

urllib.urlretrieve(url, filename, reporthook=Retriever)
print "\nFinished downloading, file saved as %s"%filename
