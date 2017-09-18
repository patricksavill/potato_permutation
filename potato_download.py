from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import cookielib
import json


# modified from
# https://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search

def get_soup(url, header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url, headers=header)), 'html.parser')


def grab_image(image_search_name, num_images):
    potato_search_name = '+'.join(image_search_name.split())
    # add the directory for your image here
    DIR = "Potatos"

    if os.path.exists(DIR +'/' + potato_search_name + '.jpg'):
        return
    url = "https://www.google.co.in/search?q=" + potato_search_name + "&source=lnms&tbm=isch"
    print url
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }
    soup = get_soup(url, header)

    ActualImages = []  # contains the link for Large original images, type of  image
    for a in soup.find_all("div", {"class": "rg_meta"}):
        link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
        ActualImages.append((link, Type))
        num_images += -1
        if num_images == 0:
            break

    # print  "there are total", len(ActualImages), "images"

    if not os.path.exists(DIR):
        os.mkdir(DIR)


    # print images
    for i, (img, Type) in enumerate(ActualImages):
        try:
            req = urllib2.Request(img, headers={'User-Agent': header})
            raw_img = urllib2.urlopen(req).read()

            cntr = len([i for i in os.listdir(DIR) if potato_search_name in i]) + 1
            print cntr
            if len(Type) == 0:
                f = open(os.path.join(DIR, potato_search_name + ".jpg"), 'wb')
            else:
                f = open(os.path.join(DIR, potato_search_name + "." + Type), 'wb')

            f.write(raw_img)
            f.close()
        except Exception as e:
            print "could not load : " + img
            print e


potato_file = raw_input('file name: ')
all_potatos = open(potato_file)
for potato in all_potatos:
    grab_image('potato+' + potato.rstrip('\n'), 1)
    print potato
