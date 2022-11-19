import json
from msilib.schema import Class
import requests

class auth():
    def validToken(self, token): 
        url="http://localhost:7240/api/Users/ValidToken?token="+token
        r = requests.post(url, verify=False)
        result = r.json()
        data = bool(result['msg'])
        return data

    def getTokenHeader(self, request):
        headers = request.META.get("HTTP_AUTHORIZATION", None)
        if(headers == None):
            return ""
        parts = headers.split()
        token = parts[1]
        return token

class sharedServices():
    def getUsers(self):
        url = "http://localhost:7240/api/Users/GetUsers"
        r = requests.get(url, verify=False)
        users = r.json()
        return users
        #users = json.load(result)

