#! /usr/bin/python3
# coding: utf8
import requests, re

import wget
import argparse
from bs4 import BeautifulSoup

TAG_RE = re.compile(r'<[^>]+>')

parser = argparse.ArgumentParser(description='Rah c\'est bien les scripts python')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--file',
                    metavar='DumpFile',
                    type=str,
                    help='A file of anonfile urls',
                    required=False)

group.add_argument('-p', '--link',
                    metavar='PasteLink',
                    type=str,
                    help='A link to a pastebin of anonfile urls',
                    required=False)

parser.add_argument('--no-download',
                    action='store_true',
                    help='Don\'t download files, only get the redirected urls',
                    required=False)

parser.add_argument('-o', '--output', 
                    metavar='OutputFile',
                    type=str,
                    help='Output file',
                    required=False)

args = parser.parse_args()

if args.file:
	with open(args.file, "r") as f:
		paste_links  = f.read().splitlines()
elif args.link:
	r =  requests.get(paste_url)
	paste_links = r.content.splitlines()

for paste in paste_links:
		
	print("[+] Base url : ", str(paste))
	
	response = requests.get(paste)
	if response.ok:
		soup = BeautifulSoup(response.text, "html.parser")
		anon_url = soup.find(id='download-url')['href']

		print("[+] Redirected to : ", anon_url)

		if not args.no_download:
			print("[+] Downloading : ", anon_url)
			wget.download(anon_url)

		if args.output:
			with open(args.output, "a") as f:
				f.write(anon_url)
	else:
		print("[-] 404 on", str(paste))
