# Using Twitter's User/search API to crawl data accoring to queries.
# @author: Tian LI (Email:leetian.pp@gmail.com)
# Date: Oct. 13, 2011

import tweepy
import time
import json
import sys

CONSUMER_KEY = "1ktK4InJjyRwqjCZb9phSQ"
CONSUMER_SECRET = "ziGTcGb0Wi802qL0Hc8IdKXnyZshHyoaeWVjSdqBQI"

#A dict that records the subcript of result file's name
#for a particular query.
LogCache = {}

#The rate limiting of users/search API is 350 per hour
UPPERSPEED = 5.5

#Calculate the request-sending speed (unit:times/min)
#and adjust it automatically when it runs above the
#rate limiting of Twitter.
def AdjustSpeed(starttime, reqtimes):
    curtime = time.time()
    interval = curtime - starttime
    print 'interval time:', interval
    curspeed = (reqtimes/interval) * 60
    print '[From def AdjustSpeed]Current speed:', curspeed, 'times/min.'
    if(curspeed >= UPPERSPEED):
        sleeptime = (reqtimes/UPPERSPEED)*60 - interval
        print '[From def AdjustSpeed]~~~Oh! O_O I have to sleep for ',sleeptime,'s~~~'
        #time.sleep(sleeptime)
        print "[From def AdjustSpeed]~~~Meow~ ^_~ I wake! Continue to crawl~~~"
    else:
        print '[From def AdjustSpeed]~~~Meow~ ^_^ Just take it easy. Our speed is ok~~~'


#Write LogCahce to LogFile.
def WriteLog():
    print '=======BEGIN WRITING LOG======='
    LOGFile = open('log_query.txt', 'w')
    for (k,v) in LogCache.items():
        LOGFile.flush()
        LOGFile.write(k + '\t' + str(v))
    LOGFile.close()
    print '======FINISHED WRITING LOG======'


#Load LogFile content into LogCache.
def LoadLog():
    print '=======BEGIN LOADING LOG======='
    LogFile = open('log_query.txt', 'r')
    lines = LogFile.readlines()
    for line in lines:
        tmp = line.split('\t')
        query = tmp[0]
        value = int(tmp[1])
        LogCache[query] = value
    print LogCache
    print '======FINISHED LOADING LOG======'
    

#Crawl statuses according to query file
def SearchMain():
    LoadLog()
    
    queryfile = open('queries.txt','r')
    queries = queryfile.readlines()
    
    myfile = open('token.txt', 'r')
    tokens = myfile.readlines()
    token_key = tokens[0].strip()
    token_secret = tokens[1].strip()
    access_key = tokens[2].strip()
    access_secret = tokens[3].strip()
    myfile.close()
    
    pp_oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    pp_oauth.set_request_token(token_key, token_secret)
    pp_oauth.set_access_token(access_key, access_secret)
    auth_api = tweepy.API(pp_oauth, secure = True)
    
    RequestCounter = 0
    starttime = time.time()
    
    #while(True):
    try:
        for query in queries:
            page = 1
            while(page <= 50):
                #set parameters ['q', 'per_page', 'page']
                results = auth_api.search_users(query, 20, page)
                data = json.loads(results)
                if(len(data) == 0):
                    page = 51
                    break
                    
                if( not LogCache.has_key(query) ):
                    LogCache[query] = -1
                LogCache[query] += 1
                filename = query + '_' + str(LogCache[query])
                jsonfile = open(filename,'w')
                jsonfile.write(results)
                
                RequestCounter += 1
                #below is for self-test
                print '#####################', len(data)
                for val in data:
                    sys.stdout.flush()
                    if(val.has_key('status')):
                        print val['screen_name'], '\t', val['status']['id'],'\t', val['status']['created_at']
                    else:
                        print 'no status'  
                print LogCache
                print '********************', len(data)
                    
                AdjustSpeed(starttime, RequestCounter)
                page += 1
                print '==========================='
            
        WriteLog()
    except KeyboardInterrupt:
        print '<<<WARNING>>>FORCED TO STOP!!!'
        WriteLog()
    except Exception, e:
        print e

if __name__ == '__main__':
    print '======START CRAWLING TASK======'
    SearchMain()
    print '=====FINISHED CRAWLING TASK====='
    print '========SEE YA~ meow ^_~========'
    
