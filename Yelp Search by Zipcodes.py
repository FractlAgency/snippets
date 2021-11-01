#!/usr/bin/python
from urllib.parse import quote
from urllib.parse import urlencode
import requests, os, time, csv, urllib, json, datetime

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
API_KEY = os.environ("YELP_API_KEY_1")
API_KEY_2 = os.environ("YELP_API_KEY_2")
SEARCH_LIMIT = 50
RADIUS = 100


terms = ["restaurants"]
locations = [{"zip": "000000", "city": "CITY_NAME", "state": "STATE_NAME"}]


ids = []
output = csv.writer(open("yelp_"+"+".join(terms)+"_"+datetime.date.today().strftime("%m%d%y")+".csv", 'wt'))
output.writerow(["search term","location","page","id","alias","name","rating","review_count","price","phone","categories","latitude","longitude","display_address","city","state","zip_code","url"])

def request(host, path, api_key, url_params=None):
	url_params = url_params or {}
	url = '{0}{1}'.format(host, quote(path.encode('utf8')))
	headers = {
		'Authorization': 'Bearer %s' % api_key,
	}
	response = requests.request('GET', url, headers=headers, params=url_params, verify=False)
	return response.json()

def search(api_key, term, location, p):
	url_params = {
		'term': term.replace(' ', '+'),
		'location': location.replace(' ', '+'),
		#'radius':RADIUS,
		'limit': SEARCH_LIMIT,
		'sort_by':'distance',
		'offset':(SEARCH_LIMIT*p)
	}
	print(json.dumps(url_params))
	return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)
	
def write(term,location,page,d):
	r = []
	cats = []
	for c in d["categories"]:
		cats.append(c["title"])
	r.append(d["id"])
	r.append(d["alias"])
	r.append(d["name"])

	if "rating" in d: r.append(d["rating"])
	else: r.append("")
	if "review_count" in d: r.append(d["review_count"])
	else: r.append("")
	if "price" in d: r.append(d["price"])
	else: r.append("")
	if "phone" in d: r.append(d["phone"])
	else: r.append("")
	r.append(",".join(cats))
	r.append(d["coordinates"]["latitude"])
	r.append(d["coordinates"]["longitude"])
	r.append(" ".join(d["location"]["display_address"]))
	r.append(d["location"]["city"])
	r.append(d["location"]["state"])
	r.append(d["location"]["zip_code"])
	r.append(d["url"])
	output.writerow([term,location,page]+r)

def query_api(term, location):
	run = True
	i=0
	while run is True:
		response = search(API_KEY, term, location["zip"], i)
		try:
			businesses = response["businesses"]
		except Exception as e:
			print(e)
			print(response)
			run = False
		for d in businesses:
			if d["id"] not in ids:
				ids.append(d["id"])
				write(location["zip"],location["city"]+", "+location["state"],i,d)
		i+=1

for term in terms:
	for location in locations:
		query_api(term, location)
		
