import requests
import json
from pprint import pprint

class Authenticator(object):
    base_uri = None
    token = None
    HEADER = {'content-type': 'application/json'}
    # in case of https endpoint
    verify = False
    
    def __init__(self, uri = None):
        Authenticator.base_uri = uri
        
    @classmethod
    def set_auth_base_uri(cls, uri):
        cls.base_uri = uri
        
    @classmethod
    def logon(cls, username, password):
        ret = False
        if not cls.token:
            if cls.base_uri:
                authuri = "%s/login/" % cls.base_uri
                data = {"username": username, "password": password}
                r = requests.post(authuri,
                                  data=json.dumps(data),
                                  headers = cls.HEADER,
                                  verify = cls.verify)
                try:
                    cls.token = r.json()["key"]
                except:
                    ret = False
                ret = cls.token
        else:
            ret = cls.token
        return ret
    
    @classmethod
    def logoff(cls):
        ret = True
        if cls.token:
            if cls.base_uri:
                authuri = "%s/logout/" % cls.base_uri
                header = cls.HEADER
                header['Authorization'] = "Token %s" % cls.token
                r = requests.post(authuri,
                                  headers = header,
                                  verify = cls.verify)
                cls.token = None
            else:
                ret = False
        return ret
    
    @classmethod
    def status(cls):
        ret = False
        if cls.token:
            ret = True
        return ret

def main():
    url = "http://localhost:8080/rest-auth"
    auth = Authenticator(url)
    
    # change user, password to proper value as set in django
    # in shell, we may ask user input
    user = "USER"
    password = "PASS"
    print auth.status()
    print auth.logon(user, password)
    print auth.status()
    print auth.logoff()
    print auth.status()
    print auth.logoff()

def test_get_cluster_list():

    token = ''
    print "\nTEST 1: Get without logon"
    print "-" * 80
    authheader = {'content-type': 'application/json', "Authorization": 'Token %s' % token}
    geturl = "http://localhost:8080/v1/cluster/"
    r = requests.get(geturl, headers = authheader)
    pprint (r.json())
    
    print "\nTEST 2: Auth and then get cluster list"
    print "-" * 80
    authurl = "http://localhost:8080/rest-auth"
    auth = Authenticator(authurl)
    # change user, password to proper value as set in django
    # in shell, we may ask user input
    user = "USER"
    password = "PASS"
    token = auth.logon(user,password)
    
    # construct a header with auth token after login
    # for all the following calls before log out
    authheader = {'content-type': 'application/json', "Authorization": 'Token %s' % token}
    geturl = "http://localhost:8080/v1/cluster/"
    r = requests.get(geturl, headers = authheader)
    pprint (r.json())
    
    print "\nTEST 3: Get cluster 'OSG'"
    print "-" * 80
    geturl1 = "%s%s" % (geturl, "osg/")
    r1 = requests.get(geturl1, headers = authheader)
    pprint (r1.json())
    
    print "\nTEST 4: logoff and get cluster list again"
    print "-" * 80
    auth.logoff()
    authheader = {'content-type': 'application/json', "Authorization": 'Token %s' % token}
    geturl = "http://localhost:8080/v1/cluster/"
    r = requests.get(geturl, headers = authheader)
    pprint (r.json())
    
if __name__ == "__main__":
    test_get_cluster_list()
        