from rauth import OAuth1Service, OAuth2Service
from rauth.utils import parse_utf8_qsl as prs_utf8
from time import time
from json import loads

class oauth:
    def __init__(self, c_key, c_sec, name, req_tkn_url, auth_url, acc_tkn_url,
      bs_url, cb_uri=None, tkn=None, tkn_sec=None, use_handle=False, 
      handle=None, json=False):

        self.oas = OAuth1Service(name = name, consumer_key = c_key, 
          consumer_secret = c_sec, access_token_url = acc_tkn_url,
          authorize_url = auth_url, request_token_url = req_tkn_url,
          base_url = bs_url)

        if use_handle == True:
            self.use_handle = True
            self.handle = handle
        else:
            self.use_handle = False

        if tkn is not None and tkn_sec is not None:
            self.token = tkn
            self.token_secret = tkn_sec

        if cb_uri is not None:
            self.callback_uri = cb_uri

        if json == True:
            self.json = True
        else:
            self.json = False

        self.expires = time()
        self.expire_int = 0

    def get_req_tkn(self):
        if self.callback_uri is None:
            req_tkn, req_tkn_sec = self.oas.get_request_token() 
        else:
            req_tkn, req_tkn_sec = self.oas.get_request_token( \
              params = {"oauth_callback" : self.callback_uri} )
 
        self.rt = req_tkn
        self.rts = req_tkn_sec

        au_url = self.oas.get_authorize_url(req_tkn)

        self.au = au_url

    def get_auth_sess(self, oauth_verif):
        self.session = self.oas.get_auth_session(self.rt, self.rts, \
          params = { "oauth_verifier" : oauth_verif }) 

        if self.use_handle == True:
            raw_tkn = self.oas.get_raw_access_token(self.rt, self.rts, \
              params = { "oauth_verifier" : oauth_verif }) 
            self.handle = prs_utf8(raw_tkn.content)['oauth_session_handle']

        self.expire_int = int(prs_utf8(raw_tkn.content)['oauth_expires_in'])
        self.expires = self.expire_int + time()

        self.token = self.session.access_token
        self.token_secret = self.session.access_token_secret

    def refresh_acc_tkn(self):
        prms = {}
        if self.use_handle is True:
            prms = { "oauth_session_handle" : self.handle }

        acc_tkn, acc_tkn_sec = \
          self.oas.get_access_token(self.token, self.token_secret,
            params = prms)

        self.session = self.oas.get_session((acc_tkn, acc_tkn_sec))

        if self.expire_int == 0:
            raw_tkn = self.oas.get_raw_access_token(self.token, \
              self.token_secret, params = prms)
            self.expire_int = int(prs_utf8(raw_tkn.content)['oauth_expires_in']) 
        self.expires = self.expire_int + time()

    def request(self, url):
        if self.expires < time():
            self.refresh_acc_tkn()

        prms = {}
        if self.json == True:
            prms = { 'format' : 'json' }
 
        return self.session.get(url, params = prms).text

class oauth2:
    def __init__(self, c_id, c_sec, name, auth_url, acc_tkn_url, bs_url, 
      cb_uri=None, exp=None, refresh_tkn=None, json=False):

        self.oas = OAuth2Service(name = name, client_id = c_id, 
          client_secret = c_sec, access_token_url = acc_tkn_url,
          authorize_url = auth_url, base_url = bs_url)

        if refresh_tkn is not None:
            self.ref_token = refresh_tkn
        else:
            self.ref_token = ''

        if cb_uri is not None:
            self.callback_uri = cb_uri
        else:
            self.callback_uri = 'oob'

        if json == True:
            self.json = True
        else:
            self.json = False

        if exp == True:
            self.expires = time()
            self.expire_int = 0
        else:
            self.expires = False

    def get_auth_url(self):
        params = {'response_type': 'code', 'redirect_uri' : self.callback_uri}
        
        self.au = self.oas.get_authorize_url(**params)

    def get_auth_sess(self, auth_code):
        params = {'grant_type': 'authorization_code', 'code' : auth_code,
          'redirect_uri' : self.callback_uri}
        
        self.session = self.oas.get_auth_session(data = params, 
          decoder = self.decode_resp)

    def refresh_acc_tkn(self):
        params = {'grant_type': 'refresh_token',
          'refresh_token' : self.ref_token, 'redirect_uri' : self.callback_uri}
        
        self.session = self.oas.get_auth_session(data = params, 
          decoder = self.decode_resp)

    def decode_resp(self, raw_response):
        resp = loads(raw_response)

        if 'refresh_token' in resp:
            self.ref_token = resp['refresh_token']
    
        self.expires_int = resp['expires_in']
        self.expires = self.expires_int + time()

        return resp

    def request(self, url):
        if self.expires != False:
            if self.expires < time() or self.ref_token == '':
                self.refresh_acc_tkn()

        params = {}
        if self.json == True:
            params = { 'format' : 'json' }
 
        return self.session.get(url, params = params).text