import os
from bs4 import BeautifulSoup
import requests
from firebase import Storage, Firebase
from dotenv import load_dotenv

load_dotenv()

data = {
    "name":os.getenv("name"),
    "api": os.getenv("api"),
    "secret": os.getenv("secret")
}

db = Firebase(os.getenv("projectid"), os.getenv("dbsecret"))
cloud = Storage(data)

# url = cloud.Upload("Bengal_Tiger_Karnataka.jpg", "animals")
# db.push("quotesdata",{"url": url})

qurl = "https://quotefancy.com/motivational-quotes"

response = requests.get(qurl)
soup = BeautifulSoup(response.content, 'html.parser')
directory = 'quotes'
if not os.path.exists(directory):
    os.makedirs(directory)

img_tags = soup.find_all('img', alt=True)

for img in img_tags:
    # Check if the img tag has a src attribute
    if 'data-original' in img.attrs:
        # Get the image source URL
        img_url = img['data-original']

        # Make a GET request to the image URL
        img_response = requests.get(img_url)

        # Extract the filename from the URL
        filename = os.path.join(directory, os.path.basename(img_url))

        # Save the image to the images directory
        with open(filename, 'wb') as f:
            f.write(img_response.content)
        url = cloud.Upload(filename, "quotes")
        db.push("quotesdata",{"url": url})
    else:
        print("Skipping image without src attribute:", img)
