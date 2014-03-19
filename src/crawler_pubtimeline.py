import urllib2
import simplejson
import time
import csv

#The rate limiting of Public Timeline is 150 per hour
UPPERSPEED = 2.5
'''
calculate the request-sending speed (unit:times/min)
and adjust it automatically when it runs above the
rate limiting of Twitter.
'''

cookies = '__utma=43838368.1149310522.1262412702.1269612588.1269695495.11; __utmz=43838368.1262412702.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=43838368.lang%3A%20en; __qca=P0-2060112157-1268910696397; auth_token=1269591657%7C4f45f046b0d2ce733bdbc26d57d35c6ec394e937; guest_id=1269695487536; lang=en; _twitter_sess=BAh7DjoTcGFzc3dvcmRfdG9rZW4iLTk3ZjZhOGU2OWMzODIyMTdiMjAxM2Ji%250ANjhlMTUxNTE0ZDAyNGNjMTA6FWluX25ld191c2VyX2Zsb3cwOhF0cmFuc19w%250Acm9tcHQwOg9jcmVhdGVkX2F0bCsITJ6%252FnycBOgl1c2VyaQRuvz0BIgpmbGFz%250AaElDOidBY3Rpb25Db250cm9sbGVyOjpGbGFzaDo6Rmxhc2hIYXNoewAGOgpA%250AdXNlZHsAOgdpZCIlNjM4NDQxNGQ4OWUxYTlhN2YyMGM0OTQwZmM3ODIyMjgi%250AJ3Nob3dfZGlzY292ZXJhYmlsaXR5X2Zvcl9KdWxpdXN0Y2gwOgxjc3JmX2lk%250AIiU4MjVlNGU4YTBhMzgyNDkxNGE0ZDY2NjQ1M2Q1MmMzZA%253D%253D--94466103ec87cfa7fb2bec5ab18cec293d7c9029; __utmb=43838368.4.10.1269695495; __utmc=43838368; original_referer=4bfz%2B%2BmebEkRkMWFCXm%2FCUOsvDoVeFTl'
#url = "https://api.twitter.com/1/followers/ids.json?cursor=-1&screen_name=twitterapi&user_id=219572129"
headers = {}
headers['User-Agent'] = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.8) Gecko/20100214 Ubuntu/9/10 (karmic) Firefox/3.5.8'
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1'
headers['Cookies'] = cookies

#extractfile = open("tweets_pub.csv", "ab")
#fout = csv.writer(extractfile)

i = 0
try:
    print ('hi')
    while(i < 1):
        time1 = time.time()
        filename = "pub_timeline_20111010_" + str(i)
        jsonfile = open(filename, "w")
        url = "https://api.twitter.com/1/statuses/public_timeline.json?"
        req = urllib2.Request(url, None, headers)
        res = urllib2.urlopen(req)
        content = res.read()
        jsonfile.write(content)
        jsonfile.close()

        '''extract info into csv file'''
        data = simplejson.loads(content)
        '''
        for val in data:
            created_time = val['created_at']
            tweet_id = val['id_str']
            text = val['text']
            user_id = val['user']['id_str']
            user_statuses = str(val['user']['statuses_count'])
            user_followers = str(val['user']['followers_count'])
            user_friends = str(val['user']['friends_count'])
            #fout.writerow([created_time, tweet_id, text, user_id, user_statuses, user_followers, user_friends])
            
            print ('time:'+ created_time)
            print ('tweet_id:' + tweet_id)
            print ('text:' + text)
            print ('user_id:' + user_id)
            print ('user_statuses:' + user_statuses)
            print ('user_followers:' + user_followers)
            print ('user_friends:' + user_friends)
        '''    
        time2 = time.time()
        print ("***time:" + str(time2-time1)+ "s.***")
        i += 1
        #time.sleep(8)
finally:
    #extractfile.close()
    print "litian"
print '===PROGRAM END==='
