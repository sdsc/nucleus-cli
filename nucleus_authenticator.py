import requests
import json
import time
from pprint import pprint

# for unit testing only.
USERNAME=""
PASSWORD=""

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
                header = dict(cls.HEADER)
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

'''
# To make GET calls for synchronous or asynchronous API
def hop_get(url, headers=None, timeout=10):
    r = requests.get(url, headers=headers)
    ret = None
    # responded immediately
    if r.status_code == 200:
        ret = r.json()
    # code 202, accepted call and processing
    elif r.status_code == 202:
        success = 0
        ntried = 0
        # status check by visiting another URL
        newurl = r.headers["Location"]
        ret = requests.get(newurl, headers=headers).json()
        while not success and ntried<timeout:
            # result ready, status was set to 1; otherwise 0
            success = ret['status']
            if success:
                ret = ret['data']
            else:
                #print "trying again %s out of %s" % (ntried, timeout)
                time.sleep(1)
                ret = requests.get(newurl, headers=headers).json()
                ntried += 1
        if timeout == ntried:
            ret = None
    return ret
'''

# To make GET calls for synchronous or asynchronous API
def hop_http(url, action="get", headers=None, data=None, cacert=False):
    if 'post' == action:
        r = requests.post(url, headers=headers, data=json.dumps(data), verify=cacert)
    else:
        r = requests.get(url, headers=headers, verify=cacert)

    ret = None

    # responded immediately
    if r.status_code == 200:
        try:
            ret = r.json()
        except:
            ret = r
    # code 202, accepted call and processing
    elif r.status_code == 202:
        # now automatically redirect to result page
        # thus no need to check status periodically.
        # Currently it works well for cluster listing
        # However not sure if the delay is large, what the behaviour would be
        finished = False
        newurl = r.headers["Location"]
        while not finished:
            ret = requests.get(newurl, headers=headers, verify=cacert)
            try:
                ret = ret.json()
            except:
                pass
            # in some occasions, when the result is not ready,
            # the result still has 'status' in it (value as '0')
            # otherwise it's the correct value after redirection 
            if 'status' not in ret:
                finished = True
            else:
                time.sleep(1)
    elif r.status_code == 401:
        ret = {"error": "Not Authenticated"}
    elif r.status_code == 403:
        ret = {"error": "Permission denied"}

    return ret

def main():
    url = "http://localhost:8080/rest-auth"
    auth = Authenticator(url)
    
    # change user, password to proper value as set in django
    # in shell, we may ask user input
    user = USERNAME
    password = PASSWORD
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
    geturl = "https://localhost:8443/nucleus/v1/cluster/"
    r = requests.get(geturl, headers = authheader, verify=False)
    #pprint (r)
    pprint (r.json())
    
    print "\nTEST 2: Auth and then get cluster list"
    print "-" * 80
    authurl = "https://localhost:8443/nucleus/rest-auth"
    auth = Authenticator(authurl)
    # change user, password to proper value as set in django
    # in shell, we may ask user input
    user = USERNAME
    password = PASSWORD
    token = auth.logon(user,password)
    
    # construct a header with auth token after login
    # for all the following calls before log out
    authheader = {'content-type': 'application/json', "Authorization": 'Token %s' % token}
    geturl = "https://localhost:8443/nucleus/v1/cluster/"
    r = hop_http(geturl, headers=authheader)
    pprint (r)
    
    # as of 2:40pm ET Oct 15, this is changed to 'not implemented'
    # as of 5:30pm ET this is now fixed and working
    # Getting only cluster details for those owned by the caller.
    print "\nTEST 3a: Get cluster 'OSG'"
    print "-" * 80
    geturl1 = "%s%s" % (geturl, "osg/")
    r1 = hop_http(geturl1, headers=authheader)
    pprint (r1)
    
    print "\nTEST 3b: Get cluster 'vc1'"
    print "-" * 80
    geturl1 = "%s%s" % (geturl, "vc1/")
    r1 = hop_http(geturl1, headers=authheader)
    pprint (r1)

    print "\nTEST 4: logoff and get cluster list again"
    print "-" * 80
    auth.logoff()
    authheader = {'content-type': 'application/json', "Authorization": 'Token %s' % token}
    geturl = "https://localhost:8443/nucleus/v1/cluster/"
    r = requests.get(geturl, headers = authheader, verify=False)
    pprint (r.json())

def test_power_on_nodes():
    
    print "\nTEST: power on a list of nodes"
    print "-" * 80

    print "\nAuthenticating...\n"
    # always logon first
    authurl = "https://localhost:8443/nucleus/rest-auth"
    auth = Authenticator(authurl)
    user = USERNAME
    password = PASSWORD
    token = auth.logon(user,password)
    authheader = {'content-type': 'application/json', "Authorization": 'Token %s' % token}

    url = "https://localhost:8443/nucleus/v1/"
    vcname = "vc2"
    vmnames = ["vm-vc2-0", "vm-vc2-1"]
    vmhosts = {}
    vmhosts[vmnames[0]] = "comet-01-05aaa"
    vmhosts[vmnames[1]] = "comet-01-06bbb"
    data = {"computes":[{"name":vm,"host":vmhosts[vm]} for vm in vmnames],"cluster":"%s" % vcname}

    print "Issuing request to poweron nodes..."
    posturl = "%s/computeset/" % (url)
    #posturl = "%s%s/compute/poweron" % (url, vcname)
    r = hop_http(posturl, action="post", headers=authheader, data=data)
    print "RETURNED RESULTS:"
    print (r)

if __name__ == "__main__":
    test_get_cluster_list()
    #main()
    test_power_on_nodes()
