import urllib2
import simplejson
import time
import sys

def transDate(dateStr):
    #dateStr: Thu Oct 06 00:38:09 +0000 2011
    array = dateStr.split(" ")
    month = array[1]
    day = array[2]
    year = array[5]
    
    if(month == 'Jan'):
        month = 1
    elif(month == 'Feb'):
        month = 2
    elif(month == 'Mar'):
        month = 3
    elif(month == 'Apr'):
        month = 4
    elif(month == 'May'):
        month = 5
    elif(month == 'Jun'):
        month = 6
    elif(month == 'Jul'):
        month = 7
    elif(month == 'Aug'):
        month = 8
    elif(month == 'Sep'):
        month = 9
    elif(month == 'Oct'):
        month = 10
    elif(month == 'Nov'):
        month = 11
    elif(month == 'Dec'):
        month = 12

    rtnDate = year, month, day
    print rtnDate[0],rtnDate[1],rtnDate[2]
    return rtnDate

'''  
reload(sys)
sys.setdefaultencoding('UTF-8')
print sys.getdefaultencoding()
'''
cookies = '__utma=43838368.1149310522.1262412702.1269612588.1269695495.11; __utmz=43838368.1262412702.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=43838368.lang%3A%20en; __qca=P0-2060112157-1268910696397; auth_token=1269591657%7C4f45f046b0d2ce733bdbc26d57d35c6ec394e937; guest_id=1269695487536; lang=en; _twitter_sess=BAh7DjoTcGFzc3dvcmRfdG9rZW4iLTk3ZjZhOGU2OWMzODIyMTdiMjAxM2Ji%250ANjhlMTUxNTE0ZDAyNGNjMTA6FWluX25ld191c2VyX2Zsb3cwOhF0cmFuc19w%250Acm9tcHQwOg9jcmVhdGVkX2F0bCsITJ6%252FnycBOgl1c2VyaQRuvz0BIgpmbGFz%250AaElDOidBY3Rpb25Db250cm9sbGVyOjpGbGFzaDo6Rmxhc2hIYXNoewAGOgpA%250AdXNlZHsAOgdpZCIlNjM4NDQxNGQ4OWUxYTlhN2YyMGM0OTQwZmM3ODIyMjgi%250AJ3Nob3dfZGlzY292ZXJhYmlsaXR5X2Zvcl9KdWxpdXN0Y2gwOgxjc3JmX2lk%250AIiU4MjVlNGU4YTBhMzgyNDkxNGE0ZDY2NjQ1M2Q1MmMzZA%253D%253D--94466103ec87cfa7fb2bec5ab18cec293d7c9029; __utmb=43838368.4.10.1269695495; __utmc=43838368; original_referer=4bfz%2B%2BmebEkRkMWFCXm%2FCUOsvDoVeFTl'
basicUrl = "https://api.twitter.com/1/statuses/user_timeline.json?"
#url = "https://api.twitter.com/1/followers/ids.json?cursor=-1&screen_name=twitterapi&user_id=219572129"
headers = {}
#headers['User-Agent'] = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.8) Gecko/20100214 Ubuntu/9/10 (karmic) Firefox/3.5.8'
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1'
headers['Cookies'] = cookies

inputfile = open("followers.txt", "r")
logfile = open("log_max.txt","a")

lines = inputfile.readlines()

print "I am crawling the statuses according to user id~ ^_~"
for line in lines:
    print ("===============================")
    page = 1
    flag = True
    total = 0
    while(flag):
        try:
            user_id = line.strip()
            url = basicUrl + "user_id=" + user_id + "&page=" + str(page)
            #url = "https://api.twitter.com/1/statuses/user_timeline.json?&screen_name=tian_pp&count=20"
            req = urllib2.Request(url, None, headers)
            res = urllib2.urlopen(req)
            content = res.read()
            data = simplejson.loads(content)
            if(len(data)==0):
                flag = False
                break
            filename = "tweet_" + user_id + "_" + str(page)
            print filename
            jsonfile = open(filename, "w")
            jsonfile.write(content)
            jsonfile.close()
            sub_counter = 1;
            for val in data:
                total += 1
                sub_counter += 1
                createDate_raw = val['created_at']
                createDate = transDate(createDate_raw)
                statuses_count = val['user']['statuses_count']
                print createDate_raw
                print (str(statuses_count))
                #filter tweets before 2011-Aug-1
                if(createDate[1] < 8):
                    maxTweetId = str(val['id'])
                    userId = val['user']['id']
                    logfile.flush()
                    logfile.write(str(userId)+'\t'+str(maxTweetId)+'\n')
                    flag = False
                    break
                if(sub_counter == len(data) and statuses_count < page*20):
                    maxTweetId = str(val['id'])
                    userId = val['user']['id']
                    logfile.flush()
                    logfile.write(str(userId)+'\t'+str(maxTweetId)+'\n')
                    flag = False
                    break
            
            page += 1
        except Exception, e:
            print "<<<ERROR>>>"
            print e.code,':', e.msg
            if(e.code == 400 or e.code == 401):
                print "~~~meow~~~"
                time.sleep(10)
            flag = False
    print user_id, 'has', total, 'statuses.'
    print '-----------Finished-------------'
    print '~~~~~Begin Sleeping for 10s~~~~~'
    time.sleep(10)
    print '----------------------------Next'
    
inputfile.close()
logfile.close()
print '===PROGRAM END==='
