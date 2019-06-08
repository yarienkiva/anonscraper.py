# coding: utf8
import requests
from bs4 import BeautifulSoup
import re
import wget

TAG_RE = re.compile(r'<[^>]+>')

paste_url = input("Raw pastebin link : ") or "https://pastebin.com/raw/HU8qWibZ" 
response = requests.get(paste_url)

paste_links = response.content.splitlines()

for paste in paste_links:
		
	print("Base url : " + str(paste))

	# get the link that we are normally redirected to by 
	# extracting it from the title tag  
	# this is not the only way to do this the link can be found
	# in multiple tags in the page (it's also the only link on the page)
	response = requests.get(paste)
	soup = BeautifulSoup(response.text, "html.parser")
	
	anon_title = str(soup.findAll('title')[0])
	anon_title = TAG_RE.sub('', anon_title)
	anon_url = anon_title.split(" ")[2] 

	print("Redirected to : " + anon_url)
	
	# get the link to the dump
	# this time it's nested in the middle of the page
	# and there are multiple links so it has to be done in
	# a rather static way
	response = requests.get(anon_url)
	soup = BeautifulSoup(response.text, "html.parser")

	dump_content = soup.find("div",{"class":"col-xs-12 col-md-4 text-center"})
	dump_link = dump_content.find("a").get('href')
	
	print("Dump link : " + dump_link)

	# I really couldn't care less about not using urllib
	wget.download(dump_link)
