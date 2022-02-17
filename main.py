from selenium import webdriver
from gtts import gTTS
from moviepy.editor import *
from PIL import ImageFont, Image, ImageDraw

import time
import random
import textwrap
import glob
import os

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.dir", '/image')
fp.set_preference("browser.preferences.instantApply", True)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk","text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml")
fp.set_preference("browser.helperApps.alwaysAsk.force", False)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.folderList", 2)
fp.set_preference('browser.helperApps.neverAsk.saveToDisk','image/jpeg,image/png,''application/octet-stream')

browser = webdriver.Firefox(firefox_profile=fp)

browser.get('https://www.reddit.com/r/story/top/?t=all')

time.sleep(3)

for i in range(4):
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)

urls = browser.find_elements_by_xpath('/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/a')

def getARandonUrl():
    global x
    def get():
        global x
        x = (random.randrange(0,len(urls)+1)-1)+2
        element = browser.find_elements_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[4]/div[1]/div[4]/div["+str(x)+"]/div/div/div[3]/div[1]/div/div[1]/span[2]/span") 
        if len(element)>0:
            get()
        else:
            x = x-2
            return urls[x].get_attribute("href")
    url = get()
    return url

url = getARandonUrl()

browser.get(url)

time.sleep(3)

tittle = browser.find_element_by_css_selector("._29WrubtjAcKqzJSPdQqQ4h > h1:nth-child(1)").text

content = browser.find_element_by_css_selector("._3xX726aBn29LDbsDtzr_6E > div:nth-child(1)").text

browser.get("https://unsplash.com/")

time.sleep(3)

browser.find_element_by_xpath('/html/body/div/div/div[3]/div[1]/div/div[2]/div[1]/div/div/div/div/div[1]/form/div[1]/input').send_keys(tittle)

browser.find_element_by_xpath('/html/body/div/div/div[3]/div[1]/div/div[2]/div[1]/div/div/div/div/div[1]/form/button').click()

time.sleep(2)

browser.find_element_by_xpath('/html/body/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[1]/div/button/span').click()

time.sleep(2)

browser.find_element_by_xpath('/html/body/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[1]/div/div/div/div/div/ul/li[2]/a/div/div[1]').click()

time.sleep(2)

browser.find_element_by_css_selector('html body.js-focus-visible div#app div div div div div.rJ2xz.bYpwS.U8eXG.M5vdR div div.mItv1 div.ripi6 figure div.YdIix div.L34o8 div.MbNnd div.zmDAx a.rEAWd div.omfF5 div.MorZF div.VQW0y.Jl9NH').click()

time.sleep(5)

browser.find_element_by_css_selector('.IDBf5').click()

time.sleep(15)

browser.close()

fp = []

browser = []

mp3file = gTTS(text=content, lang='en', slow=False)

mp3file.save("audio/audio.mp3")

mp3file = []

list_of_files = glob.glob('/image/*')

latest_file = max(list_of_files, key=os.path.getctime)

image = Image.open(latest_file)

draw = ImageDraw.Draw(image)

width, height = image.size

x, y = (width - 510, height-100)

para = textwrap.wrap(tittle, width=50)

font = ImageFont.truetype('AkayaTelivigala-Regular.ttf', 200)

current_h, pad = 200, 5

for line in para:
    w, h = draw.textsize(line, font=font)
    draw.rectangle(((width- w) / 2, current_h , ((width- w) / 2) + w, current_h + h), fill = "white")
    draw.text(((width- w) / 2, current_h), line, font=font , fill = "black")
    current_h += h + pad

image.save("image/picture.jpg",'JPEG')

image = []

draw = []

para = []

list_of_files = []

urls = []

audio = AudioFileClip('audio/audio.mp3')

video = ImageClip('image/picture.jpg').set_duration(audio.duration)

video = video.set_audio(audio)

video.write_videofile("video/Final.mp4", fps= 1,codec='libx264',audio_codec='aac',temp_audiofile='temp-audio.m4a',remove_temp=True)