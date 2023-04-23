import os
import requests
from cloudinary.uploader import upload
import cloudinary

class Firebase:
    def __init__(self, projectid, authtoken, domain=False):
        self.base_url = "https://{}-default-rtdb.firebaseio.com".format(projectid)
        self.apikey = authtoken
        self.auth_token = "?auth="+ authtoken
        self.domain = domain

    def push(self, endpoint, data):
        if endpoint[0] == "/":
            if endpoint[-5:-1] == ".jso":
                return requests.post(self.base_url+endpoint+self.auth_token, json=data).json()
            else:
                return requests.post(self.base_url+endpoint+".json"+self.auth_token, json=data).json()
        else:
            if endpoint[-5:-1] == ".jso":
                return requests.post(self.base_url+"/"+endpoint+self.auth_token, json=data).json()
            else:
                return requests.post(self.base_url+"/"+endpoint+".json"+self.auth_token, json=data).json()
                
    
    def put(self, endpoint, data):
        if endpoint[0] == "/":
            if endpoint[-5:-1] == ".jso":
                return requests.put(self.base_url+endpoint+self.auth_token, json=data).json()
            else:
                return requests.put(self.base_url+endpoint+".json"+self.auth_token, json=data).json()
        else:
            if endpoint[-5:-1] == ".jso":
                return requests.put(self.base_url+"/"+endpoint+self.auth_token, json=data).json()
            else:
                return requests.put(self.base_url+"/"+endpoint+".json"+self.auth_token, json=data).json()
    
    def update(self, endpoint, data):
        if endpoint[0] == "/":
            if endpoint[-5:-1] == ".jso":
                return requests.patch(self.base_url+endpoint+self.auth_token, json=data).json()
            else:
                return requests.patch(self.base_url+endpoint+".json"+self.auth_token, json=data).json()
        else:
            if endpoint[-5:-1] == ".jso":
                return requests.patch(self.base_url+"/"+endpoint+self.auth_token, json=data).json()
            else:
                return requests.patch(self.base_url+"/"+endpoint+".json"+self.auth_token, json=data).json()

    
    def delete(self, endpoint):
        if endpoint[0] == "/":
            if endpoint[-5:-1] == ".jso":
                return requests.delete(self.base_url+endpoint+self.auth_token).json()
            else:
                return requests.delete(self.base_url+endpoint+".json"+self.auth_token).json()
        else:
            if endpoint[-5:-1] == ".jso":
                return requests.delete(self.base_url+"/"+endpoint+self.auth_token).json()
            else:
                return requests.delete(self.base_url+"/"+endpoint+".json"+self.auth_token).json()

    def get(self, endpoint):
        if endpoint[0] == "/":
            if endpoint[-5:-1] == ".jso":
                return requests.get(self.base_url+endpoint+self.auth_token).json()
            else:
                return requests.get(self.base_url+endpoint+".json"+self.auth_token).json()
        else:
            if endpoint[-5:-1] == ".jso":
                return requests.get(self.base_url+"/"+endpoint+self.auth_token).json()
            else:
                return requests.get(self.base_url+"/"+endpoint+".json"+self.auth_token).json()
      
    def upload(self, location, file_path):
        if self.domain:
            url = "https://{}.pythonanywhere.com/upload".format(self.domain)
            files = {'file': open(file_path, 'rb')}
            data = {'path': location, 'key': self.apikey}
            response = requests.post(url, files=files, data=data).json()
            return response
        else:
            return "Please Enter Domain URL"

    def delete_file(self, location):
        url = "https://{}.pythonanywhere.com/delete".format(self.domain)
        data = {'path': location, 'key': self.apikey}
        response = requests.post(url, data=data)
        if response.ok:
            return True
        else:
            return response.json()

class Storage:
    def __init__(self, data):
        self.data = data

    def Upload(self,filename,folder):
        nfolder = folder if folder[-1] == "/" else folder+"/"
        cloudinary.config(cloud_name=self.data["name"],api_key=self.data["api"],api_secret=self.data["secret"],secure=True)
        data = upload(filename,public_id=os.path.basename(filename),folder=nfolder)
        return data["secure_url"]
