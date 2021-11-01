import os, csv, requests, time

key = os.environ("MEETUP_API_KEY")

locations = ["Birmingham, Alabama","Anchorage, Alaska","Phoenix, Arizona","Little Rock, Arkansas","Los Angeles, California","Denver, Colorado","Bridgeport, Connecticut","Wilmington, Delaware","Jacksonville, Florida","Atlanta, Georgia","Boise, Idaho","Chicago, Illinois","Indianapolis, Indiana","Des Moines, Iowa","Wichita, Kansas","Louisville, Kentucky","New Orleans, Louisiana","Portland, Maine","Baltimore, Maryland","Boston, Massachusetts","Detroit, Michigan","Minneapolis, Minnesota","Jackson, Mississippi","Kansas City, Missouri","Billings, Montana","Omaha, Nebraska","Las Vegas, Nevada","Manchester, New Hampshire","Newark, New Jersey","Albuquerque, New Mexico","New York City, New York","Charlotte, North Carolina","Columbus, Ohio","Oklahoma City, Oklahoma","Portland, Oregon","Philadelphia, Pennsylvania","Providence, Rhode Island","Charleston, South Carolina","Sioux Falls, South Dakota","Nashville, Tennessee","Houston, Texas","Salt Lake City, Utah","Burlington, Vermont","Virginia Beach, Virginia","Seattle, Washington","Charleston, West Virginia","Milwaukee, Wisconsin","Cheyenne, Wyoming","Honolulu, Hawaii","Fargo, North Dakota"] # top 50 most populus cities in each US state

headers = {'Authorization':'Bearer '+ key}

def getgroups(location, df):
    params = {'location':location,}
    r = requests.get('https://api.meetup.com/find/groups', params=params, headers=headers)
    response = r.json()
    pageloop = 0
    pagenum = 0
    newpage = ''
    while pageloop == 0:
        pagenum += 1
        if newpage:
            r = requests.get(newpage, headers=headers)
            response = r.json()
        print("\rCollecting data for: "+location+" ("+str(pagenum)+")...", end=' '*40)
        for item in response:
            try:    itemid      = item['id']
            except: itemid      = 'NA'
            try:    name        = item['name']
            except: name        = 'NA'
            try:    category    = item['category']['shortname']
            except: category    = 'NA'
            try:    status      = item['status']
            except: status      = 'NA'
            try:    urlname     = item['urlname']
            except: urlname     = 'NA'
            try:    city        = item['city']
            except: city        = 'NA'
            try:    state       = item['state']
            except: state       = 'NA'
            try:    reqlocation = location
            except: reqlocation = 'NA'
            try:    join_mode   = item['join_mode']
            except: join_mode   = 'NA'
            try:    visibility  = item['visibility']
            except: visibility  = 'NA'
            try:    membercount = item['members']
            except: membercount = 'NA'
            try:    description = item['description'].replace('\n','')
            except: description = 'NA'
            try:    metacategory = item['meta_category']['shortname']
            except: metacategory = "NA"

            
            df.writerow([itemid,name,category,metacategory,status,urlname,city,state,reqlocation,join_mode,visibility,membercount,description])
    
        try:
            header_response = requests.utils.parse_header_links(r.headers['Link'].rstrip('>').replace('>,<', ',<'))
            if header_response[0]['rel'] == 'next':
                newpage = header_response[0]['url']
            else:
                pageloop = 1
        except:
            pageloop = 1

with open('output.csv','a',encoding='utf8',newline='') as csvfile:
    df = csv.writer(csvfile)
    for location in locations:
        getgroups(location, df)
