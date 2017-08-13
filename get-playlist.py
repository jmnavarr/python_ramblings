
import os
import urllib2
from BeautifulSoup import BeautifulSoup

def get_playlist():
   playlist_info = urllib2.urlopen("http://gdata.youtube.com/feeds/api/playlists/RD7_weSk0BonM").read()
   #playlist_info = urllib2.urlopen("http://gdata.youtube.com/feeds/api/playlists/RDYXnjy5YlDwk?start-index=1&max-results=50").read() #backbone lessons
   parsed = BeautifulSoup(playlist_info)
   print parsed.title.string

   i = 0
   for link in parsed.findAll('media:content'):
      url = link.get('url')
      if url.find('http') != -1 and url.find('/v/') != -1 :
         i = i + 1
         print "Processing #", str(i), ": ", url, ":"
         #os.popen("youtube-dl -x --audio-format mp3 " + url, "w")
         os.popen("youtube-dl " + url, "w")
         print "\n"


if __name__ == "__main__":
   
   try:
      get_playlist()
   except HttpError, e:
      print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
