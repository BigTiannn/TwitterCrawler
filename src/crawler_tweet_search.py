# Using Twitter's User/search API to crawl data accoring to queries.
# @author: Tian LI (Email:leetian.pp@gmail.com)
# Date: Oct. 13, 2011

import urllib2
import urllib
import time
import json
import sys

# A dict that records the max id and min id of tweets relevant to
# a particular query respectively.
MaxIdCache = {}
MinIdCache = {}

FilenameCache= {}

# The rate limiting of users/search API is 350 per hour
UPPERSPEED = 5.5

# Calculate the request-sending speed (unit:times/min)
# and adjust it automatically when it runs above the
# rate limiting of Twitter.
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


# Write MaxIdCahce, MinIdCache and FilenameCache into
# MaxLogFile, MinIdFile and FilenameFile respectively.
def WriteLog():
    print '=======BEGIN WRITING LOG======='
    LogFile = open('log\log_query_max.txt', 'w')
    for (k,v) in MaxIdCache.items():
        LogFile.flush()
        LogFile.write(k + '\t' + str(v) + '\n')
    LogFile.close()
        
    LogFile = open('log\log_query_min.txt', 'w')
    for (k,v) in MinIdCache.items():
        LogFile.flush()
        LogFile.write(k + '\t' + str(v) + '\n')
    LogFile.close()
        
    LogFile = open('log\log_query_filename.txt', 'w')
    for (k,v) in FilenameCache.items():
        LogFile.flush()
        LogFile.write(k + '\t' + str(v) + '\n')
    LogFile.close()
    print '======FINISHED WRITING LOG======'


# Load MaxIdCahce, MinIdCache and FilenameCache into
# MaxLogFile, MinIdFile and FilenameFile respectively.
def LoadLog(loadFilenameLog, loadMaxLog, loadMinLog):
    print '=======BEGIN LOADING LOG======='
    if(loadFilenameLog):
        LogFile = open('log\log_query_filename.txt', 'r')
        lines = LogFile.readlines()
        LogFile.close()
        for line in lines:
            tmp = line.split('\t')
            query = tmp[0].strip()
            value = int(tmp[1].strip())
            FilenameCache[query] = value
        print FilenameCache
    
    if(loadMaxLog):
        LogFile = open('log\log_query_max.txt', 'r')
        lines = LogFile.readlines()
        LogFile.close()
        for line in lines:
            tmp = line.split('\t')
            query = tmp[0].strip()
            value = int(tmp[1].strip())
            MaxIdCache[query] = value
        print MaxIdCache
    
    if(loadMinLog):
        LogFile = open('log\log_query_min.txt', 'r')
        lines = LogFile.readlines()
        LogFile.close()
        for line in lines:
            tmp = line.split('\t')
            query = tmp[0].strip()
            value = int(tmp[1].strip())
            MinIdCache[query] = value
        print MinIdCache
    print '======FINISHED LOADING LOG======'


# Crawl statuses according to query file
def SearchMain():
    #You can choose whether to load the logfile or not
    LoadLog(True, False, False)
    
    queryfile = open('queries.txt','r')
    queries = queryfile.readlines()
    
    RequestCounter = 0
    starttime = time.time()
    
    cookies = '__utma=43838368.1149310522.1262412702.1269612588.1269695495.11; __utmz=43838368.1262412702.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=43838368.lang%3A%20en; __qca=P0-2060112157-1268910696397; auth_token=1269591657%7C4f45f046b0d2ce733bdbc26d57d35c6ec394e937; guest_id=1269695487536; lang=en; _twitter_sess=BAh7DjoTcGFzc3dvcmRfdG9rZW4iLTk3ZjZhOGU2OWMzODIyMTdiMjAxM2Ji%250ANjhlMTUxNTE0ZDAyNGNjMTA6FWluX25ld191c2VyX2Zsb3cwOhF0cmFuc19w%250Acm9tcHQwOg9jcmVhdGVkX2F0bCsITJ6%252FnycBOgl1c2VyaQRuvz0BIgpmbGFz%250AaElDOidBY3Rpb25Db250cm9sbGVyOjpGbGFzaDo6Rmxhc2hIYXNoewAGOgpA%250AdXNlZHsAOgdpZCIlNjM4NDQxNGQ4OWUxYTlhN2YyMGM0OTQwZmM3ODIyMjgi%250AJ3Nob3dfZGlzY292ZXJhYmlsaXR5X2Zvcl9KdWxpdXN0Y2gwOgxjc3JmX2lk%250AIiU4MjVlNGU4YTBhMzgyNDkxNGE0ZDY2NjQ1M2Q1MmMzZA%253D%253D--94466103ec87cfa7fb2bec5ab18cec293d7c9029; __utmb=43838368.4.10.1269695495; __utmc=43838368; original_referer=4bfz%2B%2BmebEkRkMWFCXm%2FCUOsvDoVeFTl'
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1'
    headers['Cookies'] = cookies
    
    #basicURL = 'https://search.twitter.com/search.json?&lang=en&&with_twitter_user_id=true&result_type=mixed&show_user=true'
    basicUrl = 'https://twitter.com/phoenix_search.phoenix'
    parameters={'include_entities':1,
                'include_available_features': 1,
                'include_available_features': 1,
                'contributor_details': 'true',
                'mode': 'relevance'}
    
    while(True):
        try:
            for query in queries:
                query = query.strip()
                parameters['q'] = query
                if(parameters.has_key('max_id')):
                    parameters.pop('max_id')
                times = 1
                max_id = 0
                while(times <= 3):
                    url = '%s?%s' % (basicUrl, urllib.urlencode(parameters))
                    req = urllib2.Request(url, None, headers)
                    res = urllib2.urlopen(req)
                    results = res.read()
                    data = json.loads(results)
                    if(len(data) == 0):
                        times = 11
                        break
                        
                    if( not FilenameCache.has_key(query) ):
                        FilenameCache[query] = -1
                    FilenameCache[query] += 1
                    filename = query + '_' + str(FilenameCache[query])
                    jsonfile = open(filename,'w')
                    jsonfile.write(results)
                    
                    RequestCounter += 1
                    
                    i = 0
                    for val in data['statuses']:
                        sys.stdout.flush()
                        print i,'\t',val['id_str'], '\t', val['created_at'],'\t', val['text']
                        min_id = int(val['id_str'])
                        if(max_id < int(val['id_str'])):
                            max_id = int(val['id_str'])
                        i += 1
                    
                    if(not MaxIdCache.has_key(query)):
                        MaxIdCache[query] = max_id
                    if(not MinIdCache.has_key(query)):
                        MinIdCache[query] = min_id
                    
                    if(min_id < MaxIdCache[query]):
                        print '######Change crawl mode#####'
                        MaxIdCache[query] = max_id
                        min_id = min_id < MinIdCache[query] and min_id or MinIdCache[query]
                        MinIdCache[query] = min_id
                    
                    parameters['max_id'] = min_id
                    
                    print 'mmmmmmmmmmmmmax_id:', max_id
                    print 'mmmmmmmmmmmmmin_id:', min_id
                    print MaxIdCache
                    print MinIdCache
                        
                    times += 1
                    AdjustSpeed(starttime, RequestCounter)
                    print '----------------------------'
                    
                print '================================'
                
            WriteLog()
        except KeyboardInterrupt:
            print '<<<WARNING>>>FORCED TO STOP!!!'
            WriteLog()
        #except Exception, e:
        #    print e

if __name__ == '__main__':
    print '======START CRAWLING TASK======'
    SearchMain()
    print '=====FINISHED CRAWLING TASK====='
    print '========SEE YA~ meow ^_~========'
    
