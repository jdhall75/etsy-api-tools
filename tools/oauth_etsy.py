from requests_oauthlib import OAuth1Session
from ..config import Config

myConfig = Config()

client_token = myConfig.client_token
client_secret = myConfig.client_secret

token_request_url = myConfig.etsy_api_url + "/v2/oauth/request_token?email_r"
token_access_url =  myConfig.etsy_api_url + 'v2/oauth/access_token'

oauth = OAuth1Session(client_token, client_secret=client_secret)

# the fetch request toke will return:
#   login_url
#   oauth_token
#   oauth_token_secret
fetch_response = oauth.fetch_request_token(token_request_url)
print("Temporary tokens")
print(fetch_response)
resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')

print("=======================================================================")
print("Please follow the url and authorize this application\n{}".format(fetch_response['login_url']))
print("")
verification_code = input("Please enter in the verification code: ")

oauth = OAuth1Session(client_token, 
                      client_secret=client_secret,
                      resource_owner_key=resource_owner_key,
                      resource_owner_secret=resource_owner_secret,
                      verifier=verification_code)

oauth_tokens = oauth.fetch_access_token(token_access_url)
print("=======================================================================")
print("Access Tokes")
print(oauth_tokens)

resource_owner_key = oauth_tokens.get('oauth_token')
resource_owner_secret = oauth_tokens.get('oauth_token_secret')
