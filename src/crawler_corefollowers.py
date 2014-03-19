import urllib2
import simplejson
import time

#cookies = '__utma=43838368.1149310522.1262412702.1269612588.1269695495.11; __utmz=43838368.1262412702.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=43838368.lang%3A%20en; __qca=P0-2060112157-1268910696397; auth_token=1269591657%7C4f45f046b0d2ce733bdbc26d57d35c6ec394e937; guest_id=1269695487536; lang=en; _twitter_sess=BAh7DjoTcGFzc3dvcmRfdG9rZW4iLTk3ZjZhOGU2OWMzODIyMTdiMjAxM2Ji%250ANjhlMTUxNTE0ZDAyNGNjMTA6FWluX25ld191c2VyX2Zsb3cwOhF0cmFuc19w%250Acm9tcHQwOg9jcmVhdGVkX2F0bCsITJ6%252FnycBOgl1c2VyaQRuvz0BIgpmbGFz%250AaElDOidBY3Rpb25Db250cm9sbGVyOjpGbGFzaDo6Rmxhc2hIYXNoewAGOgpA%250AdXNlZHsAOgdpZCIlNjM4NDQxNGQ4OWUxYTlhN2YyMGM0OTQwZmM3ODIyMjgi%250AJ3Nob3dfZGlzY292ZXJhYmlsaXR5X2Zvcl9KdWxpdXN0Y2gwOgxjc3JmX2lk%250AIiU4MjVlNGU4YTBhMzgyNDkxNGE0ZDY2NjQ1M2Q1MmMzZA%253D%253D--94466103ec87cfa7fb2bec5ab18cec293d7c9029; __utmb=43838368.4.10.1269695495; __utmc=43838368; original_referer=4bfz%2B%2BmebEkRkMWFCXm%2FCUOsvDoVeFTl'
cookies = '__utma=43838368.1908184253.1288187069.1293457708.1293457927.10; __utmz=43838368.1288187069.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=43838368.lang%3A%20en; phx_seen_dialog-190540069=true; k=137.189.207.31.1293456446443751; guest_id=12934564465104481; __utmb=43838368.27.10.1293457927; _twitter_sess=BAh7CToOcmV0dXJuX3RvIjlodHRwOi8vdHdpdHRlci5jb20vYWNjb3VudC9y%250AZXNlbmRfY29uZmlybWF0aW9uX2VtYWlsOg9jcmVhdGVkX2F0bCsI%252FQsfKC0B%250AIgpmbGFzaElDOidBY3Rpb25Db250cm9sbGVyOjpGbGFzaDo6Rmxhc2hIYXNo%250AewAGOgpAdXNlZHsAOgdpZCIlOGY5NGJmMjk1MGVjODE1ZTMyYWI4OTgzNjU5%250ANjM3ZmE%253D--358ad410834e99f332a4b321098acfcca6061dcb; original_referer=4bfz%2B%2BmebEkRkMWFCXm%2FCUOsvDoVeFTl; __utmc=43838368; tz_offset_sec=28800'
baseurl = "https://api.twitter.com/1/followers/ids.json?"
headers = {}
#headers['User-Agent'] = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.8) Gecko/20100214 Ubuntu/9/10 (karmic) Firefox/3.5.8'
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1'
headers['Cookies'] = cookies

inputfile = open("core_seeds_0.txt","r")
logfile = open("log.txt","w")

lines = inputfile.readlines()
for line in lines:
    screen_name = line.strip()
    print screen_name
    filename = "followers_" + screen_name + ".txt"
    followfile = open(filename, "w")

    try:
        counter = 0
        cursor = -1
        while cursor != 0:
            time1 = time.time()
            url = baseurl + '&screen_name=' + screen_name + '&cursor=' + str(cursor)
            time1 = time.time()
            req = urllib2.Request(url, None, headers)
            res = urllib2.urlopen(req)
            content = res.read()
            data = simplejson.loads(content)
            ids = data['ids']
            previous = data['previous_cursor']
            next_cursor = data['next_cursor']
            for eachid in ids:
                followfile.flush()
                followfile.write(str(eachid) + '\n')
            counter += len(ids)
            time2 = time.time()
            print ("***" + str(cursor) + "***" + str(counter) + "\t" + str(time2-time1) + 's')
            cursor = next_cursor
    finally:
        followfile.close()
        print ('Followers :' + str(counter))
        print ('====================================')
#logfile.write(str(counter) + "\n")

logfile.close()
print '===PROGRAM END==='

'''
Useful attributes (https://api.twitter.com/1/users/show.json?screen_name=tian_pp&include_entities=false)
name
listed_count
protected:ture/false
followers_count
verified:true/false
friends_count:(which is following_count)
status_count
screen_name
'''

