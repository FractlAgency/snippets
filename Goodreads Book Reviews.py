#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv, datetime, os, json, requests, time
from bs4 import BeautifulSoup

def getReviews(url):
	reviews = []
	r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"})
	soup = BeautifulSoup(r.text, 'html.parser')
	for review in soup.select('.gr_review_container'):
		reviews.append(review)
	return reviews

def getReviewWidget(title):
	r = requests.get(f"https://www.goodreads.com/book/title.json?&key={os.environ(GOODREADS_API_KEY)}&title="+title, headers={"Accept":"application/json", "Content-Type":"text/plain;charset=utf-8"})
	widget_html = r.json()["reviews_widget"]
	widget_soup = BeautifulSoup(widget_html, 'html.parser')
	for iframe in widget_soup.select('iframe'):
		return iframe.get('src')
		
widget = getReviewWidget("Some Book Title")
reviews = getReviews(widget)
