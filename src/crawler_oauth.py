import tweepy

CONSUMER_KEY = "1ktK4InJjyRwqjCZb9phSQ"
CONSUMER_SECRET = "ziGTcGb0Wi802qL0Hc8IdKXnyZshHyoaeWVjSdqBQI"
CALLBACK = 'http://127.1.1.1:8080/oauth/callback'
    
def RequestAuthorization():
    pp_oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK)
    pp_oauth_url = pp_oauth.get_authorization_url()
    print pp_oauth.request_token
    print pp_oauth_url

    #store the request token for access token
    myfile = open('token.txt', 'w')
    myfile.write(pp_oauth.request_token.key + '\n')
    myfile.write(pp_oauth.request_token.secret + '\n')
    myfile.close()

def RequestAccessToken(oauth_token, oauth_verifier):
    myfile = open('token.txt', 'r')
    request_token = myfile.readlines()
    token_key = request_token[0].strip()
    token_secret = request_token[1].strip()
    myfile.close()
    
    pp_oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    pp_oauth.set_request_token(token_key, token_secret)

    try:
        pp_oauth.get_access_token(oauth_verifier)
    except tweepy.TweepError, e:
        print e
        return

    access_key = pp_oauth.access_token.key
    access_secret = pp_oauth.access_token.secret

    myfile = open('token.txt', 'a')
    myfile.write(access_key + '\n')
    myfile.write(access_secret + '\n')
    myfile.write(oauth_token + '\n')
    myfile.write(oauth_verifier + '\n')

def FetchDatawithOAuth():
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
    #set parameters ['q', 'per_page', 'page']
    search = auth_api.search_users(['apple', 20, 1])
    print search
    

if __name__ == '__main__':
    #RequestAuthorization()
    #RequestAccessToken('uuLKRUybyQsgWH3Vc3Eox2FWZlYwtQahhIMQXQpv8', 'zHESImg7RMffjwIjYkVhMsQpvYAolwMgW0gINHhUODk')
    FetchDatawithOAuth()
    
