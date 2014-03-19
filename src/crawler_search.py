import urllib2
import urllib
import simplejson
import time
import sys

'''  
reload(sys)
sys.setdefaultencoding('UTF-8')
print sys.getdefaultencoding()
'''
print "begin"
cookies = '__utma=43838368.1149310522.1262412702.1269612588.1269695495.11; __utmz=43838368.1262412702.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=43838368.lang%3A%20en; __qca=P0-2060112157-1268910696397; auth_token=1269591657%7C4f45f046b0d2ce733bdbc26d57d35c6ec394e937; guest_id=1269695487536; lang=en; _twitter_sess=BAh7DjoTcGFzc3dvcmRfdG9rZW4iLTk3ZjZhOGU2OWMzODIyMTdiMjAxM2Ji%250ANjhlMTUxNTE0ZDAyNGNjMTA6FWluX25ld191c2VyX2Zsb3cwOhF0cmFuc19w%250Acm9tcHQwOg9jcmVhdGVkX2F0bCsITJ6%252FnycBOgl1c2VyaQRuvz0BIgpmbGFz%250AaElDOidBY3Rpb25Db250cm9sbGVyOjpGbGFzaDo6Rmxhc2hIYXNoewAGOgpA%250AdXNlZHsAOgdpZCIlNjM4NDQxNGQ4OWUxYTlhN2YyMGM0OTQwZmM3ODIyMjgi%250AJ3Nob3dfZGlzY292ZXJhYmlsaXR5X2Zvcl9KdWxpdXN0Y2gwOgxjc3JmX2lk%250AIiU4MjVlNGU4YTBhMzgyNDkxNGE0ZDY2NjQ1M2Q1MmMzZA%253D%253D--94466103ec87cfa7fb2bec5ab18cec293d7c9029; __utmb=43838368.4.10.1269695495; __utmc=43838368; original_referer=4bfz%2B%2BmebEkRkMWFCXm%2FCUOsvDoVeFTl'
basicUrl = "https://api.twitter.com/1/users/search.json?"
#basicUrl = "https://api.twitter.com/1/users/search.json?reputable=true&display_location=search-component&pc=true&q=appale"
headers = {}
#headers['User-Agent'] = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.8) Gecko/20100214 Ubuntu/9/10 (karmic) Firefox/3.5.8'
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1'
headers['Cookies'] = cookies
headers['oauth_token'] = '343939083-DRYYk1BTNtRpLgIz6A16zHbm2K5l8yC4QkiseDdo'
headers['oauth_token_secret'] = 'NGPUE1ahMrhOJ0YtcsgTesAzfzGGp6yrvWetDOw8yE'

post_data = urllib.urlencode({
    'oauth_token': '343939083-DRYYk1BTNtRpLgIz6A16zHbm2K5l8yC4QkiseDdo',
    'oauth_token_secret': 'NGPUE1ahMrhOJ0YtcsgTesAzfzGGp6yrvWetDOw8yE',
    'status': 'muhaha'
})


query = "microsoft"
#url = basicUrl + "&q=" + query
url = "https://api.twitter.com/1/users/search.json?q=Twitter API"
#req = urllib2.Request(url, post_data, headers)
#res = urllib2.urlopen(req)
#content = res.read()
#print content

dic = {"aaa": 1, "bbb": 2}
print dic.get("ccc", 0)
dic.pop('aaa', 0)
print dic

print '===PROGRAM END==='
