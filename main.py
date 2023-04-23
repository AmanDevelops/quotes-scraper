import os
from bs4 import BeautifulSoup
import requests
from firebase import Storage, Firebase
from dotenv import load_dotenv

# Import Required Variables
load_dotenv()

# Used to initialize cloudinary object

data = {
    "name":os.getenv("name"),
    "api": os.getenv("api"),
    "secret": os.getenv("secret")
}

# Used to initialize firebase object

db = Firebase(os.getenv("projectid"), os.getenv("dbsecret"))
cloud = Storage(data)

# URL To Scrape
qurl = "https://quotefancy.com/motivational-quotes"

# Gets the Content
response = requests.get(qurl)
soup = BeautifulSoup(response.content, 'html.parser')

# Creates a directory 
directory = 'quotes'
if not os.path.exists(directory):
    os.makedirs(directory)

# Find All The Images of a page
img_tags = soup.find_all('img', alt=True)

for img in img_tags:
    # See quotefancy html page
    if 'data-original' in img.attrs:
        # Check if the quote text exists
        if (img.get("alt", "")).startswith("Motivational Quotes: "):
            quote = img.get("alt", "")[20:] # Quote Text
            img_url = img['data-original'] # Image URLS
            
            # Downloads Image
            img_response = requests.get(img_url)
            filename = os.path.join(directory, os.path.basename(img_url))
            with open(filename, 'wb') as f:
                f.write(img_response.content)
            
            # Uploads to Cloudinary Server. See firebase.py
            url = cloud.Upload(filename, "quotes")

            # Pushes The Data to Firebase database. See firebase.py
            db.push("quotesdata",{"url": url, "text": quote})
    else:
        print("Skipping image without src attribute:", img)
