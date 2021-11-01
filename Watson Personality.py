#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv, datetime, os, json, requests, time
from requests.auth import HTTPBasicAuth


inputfile = "sample.csv"
uid_index = 0
text_index = 1

api_key_username = os.getenv("WATSON_API_USERNAME")
api_key_password = os.getenv("WATSON_API_PASSWORD")

DEBUG = False

consumption_headers = ["Likely to like drama movies","Likely to like Latin music","Likely to read autobiographical books","Likely to like horror movies","Likely to like musical movies","Likely to like classical music","Likely to eat out frequently","Likely to be influenced by brand name when making product purchases","Likely to be sensitive to ownership cost when buying automobiles","Likely to like outdoor activities","Likely to be influenced by online ads when making product purchases","Likely to prefer quality when buying clothes","Likely to read often","Likely to like romance movies","Likely to be influenced by family when making product purchases","Likely to have experience playing music","Likely to prefer style when buying clothes","Likely to like documentary movies","Likely to like rap music","Likely to be influenced by product utility when making product purchases","Likely to volunteer for social causes","Likely to be influenced by social media when making product purchases","Likely to like historical movies","Likely to like R&B music","Likely to read financial investment books","Likely to like hip hop music","Likely to read non-fiction books","Likely to read entertainment magazines","Likely to like action movies","Likely to consider starting a business in next few years","Likely to like science-fiction movies","Likely to like country music","Likely to like adventure movies","Likely to be concerned about the environment","Likely to have a gym membership","Likely to prefer comfort when buying clothes","Likely to attend live musical events","Likely to indulge in spur of the moment purchases","Likely to prefer using credit cards for shopping","Likely to like war movies","Likely to prefer safety when buying automobiles","Likely to like rock music"]
personality_headers = ["Altruism","Cautiousness","Dutifulness","Excitement-seeking","Outgoing","Trust","Cheerfulness","Assertiveness","Fiery","Cooperation","Prone to worry","Melancholy","Artistic interests","Immoderation","Intellect","Activity level","Gregariousness","Susceptible to stress","Imagination","Adventurousness","Self-efficacy","Self-consciousness","Modesty","Self-discipline","Emotionality","Uncompromising","Authority-challenging","Achievement striving","Orderliness","Sympathy"]
big5_headers = ["Big5 - Openness","Big5 - Conscientiousness","Big5 - Extraversion","Big5 - Agreeableness","Big5 - Emotional range"]

def processPersonality(data):
	consumptions = { "consumption_preferences_movie_drama": { "value": "", "name": "Likely to like drama movies" }, "consumption_preferences_music_latin": { "value": "", "name": "Likely to like Latin music" }, "consumption_preferences_books_autobiographies": { "value": "", "name": "Likely to read autobiographical books" }, "consumption_preferences_movie_horror": { "value": "", "name": "Likely to like horror movies" }, "consumption_preferences_movie_musical": { "value": "", "name": "Likely to like musical movies" }, "consumption_preferences_music_classical": { "value": "", "name": "Likely to like classical music" }, "consumption_preferences_eat_out": { "value": "", "name": "Likely to eat out frequently" }, "consumption_preferences_influence_brand_name": { "value": "", "name": "Likely to be influenced by brand name when making product purchases" }, "consumption_preferences_automobile_ownership_cost": { "value": "", "name": "Likely to be sensitive to ownership cost when buying automobiles" }, "consumption_preferences_outdoor": { "value": "", "name": "Likely to like outdoor activities" }, "consumption_preferences_influence_online_ads": { "value": "", "name": "Likely to be influenced by online ads when making product purchases" }, "consumption_preferences_clothes_quality": { "value": "", "name": "Likely to prefer quality when buying clothes" }, "consumption_preferences_read_frequency": { "value": "", "name": "Likely to read often" }, "consumption_preferences_movie_romance": { "value": "", "name": "Likely to like romance movies" }, "consumption_preferences_influence_family_members": { "value": "", "name": "Likely to be influenced by family when making product purchases" }, "consumption_preferences_music_playing": { "value": "", "name": "Likely to have experience playing music" }, "consumption_preferences_clothes_style": { "value": "", "name": "Likely to prefer style when buying clothes" }, "consumption_preferences_movie_documentary": { "value": "", "name": "Likely to like documentary movies" }, "consumption_preferences_music_rap": { "value": "", "name": "Likely to like rap music" }, "consumption_preferences_influence_utility": { "value": "", "name": "Likely to be influenced by product utility when making product purchases" }, "consumption_preferences_volunteer": { "value": "", "name": "Likely to volunteer for social causes" }, "consumption_preferences_influence_social_media": { "value": "", "name": "Likely to be influenced by social media when making product purchases" }, "consumption_preferences_movie_historical": { "value": "", "name": "Likely to like historical movies" }, "consumption_preferences_music_r_b": { "value": "", "name": "Likely to like R&B music" }, "consumption_preferences_books_financial_investing": { "value": "", "name": "Likely to read financial investment books" }, "consumption_preferences_music_hip_hop": { "value": "", "name": "Likely to like hip hop music" }, "consumption_preferences_books_non_fiction": { "value": "", "name": "Likely to read non-fiction books" }, "consumption_preferences_books_entertainment_magazines": { "value": "", "name": "Likely to read entertainment magazines" }, "consumption_preferences_movie_action": { "value": "", "name": "Likely to like action movies" }, "consumption_preferences_start_business": { "value": "", "name": "Likely to consider starting a business in next few years" }, "consumption_preferences_movie_science_fiction": { "value": "", "name": "Likely to like science-fiction movies" }, "consumption_preferences_music_country": { "value": "", "name": "Likely to like country music" }, "consumption_preferences_movie_adventure": { "value": "", "name": "Likely to like adventure movies" }, "consumption_preferences_concerned_environment": { "value": "", "name": "Likely to be concerned about the environment" }, "consumption_preferences_gym_membership": { "value": "", "name": "Likely to have a gym membership" }, "consumption_preferences_clothes_comfort": { "value": "", "name": "Likely to prefer comfort when buying clothes" }, "consumption_preferences_music_live_event": { "value": "", "name": "Likely to attend live musical events" }, "consumption_preferences_spur_of_moment": { "value": "", "name": "Likely to indulge in spur of the moment purchases" }, "consumption_preferences_credit_card_payment": { "value": "", "name": "Likely to prefer using credit cards for shopping" }, "consumption_preferences_movie_war": { "value": "", "name": "Likely to like war movies" }, "consumption_preferences_automobile_safety": { "value": "", "name": "Likely to prefer safety when buying automobiles" }, "consumption_preferences_music_rock": { "value": "", "name": "Likely to like rock music" } }
	personalities = { "facet_altruism": { "name": "Altruism", "percentile": "" }, "facet_cautiousness": { "name": "Cautiousness", "percentile": "" }, "facet_dutifulness": { "name": "Dutifulness", "percentile": "" }, "facet_excitement_seeking": { "name": "Excitement-seeking", "percentile": "" }, "facet_friendliness": { "name": "Outgoing", "percentile": "" }, "facet_trust": { "name": "Trust", "percentile": "" }, "facet_cheerfulness": { "name": "Cheerfulness", "percentile": "" }, "facet_assertiveness": { "name": "Assertiveness", "percentile": "" }, "facet_anger": { "name": "Fiery", "percentile": "" }, "facet_cooperation": { "name": "Cooperation", "percentile": "" }, "facet_anxiety": { "name": "Prone to worry", "percentile": "" }, "facet_depression": { "name": "Melancholy", "percentile": "" }, "facet_artistic_interests": { "name": "Artistic interests", "percentile": "" }, "facet_immoderation": { "name": "Immoderation", "percentile": "" }, "facet_intellect": { "name": "Intellect", "percentile": "" }, "facet_activity_level": { "name": "Activity level", "percentile": "" }, "facet_gregariousness": { "name": "Gregariousness", "percentile": "" }, "facet_vulnerability": { "name": "Susceptible to stress", "percentile": "" }, "facet_imagination": { "name": "Imagination", "percentile": "" }, "facet_adventurousness": { "name": "Adventurousness", "percentile": "" }, "facet_self_efficacy": { "name": "Self-efficacy", "percentile": "" }, "facet_self_consciousness": { "name": "Self-consciousness", "percentile": "" }, "facet_modesty": { "name": "Modesty", "percentile": "" }, "facet_self_discipline": { "name": "Self-discipline", "percentile": "" }, "facet_emotionality": { "name": "Emotionality", "percentile": "" }, "facet_morality": { "name": "Uncompromising", "percentile": "" }, "facet_liberalism": { "name": "Authority-challenging", "percentile": "" }, "facet_achievement_striving": { "name": "Achievement striving", "percentile": "" }, "facet_orderliness": { "name": "Orderliness", "percentile": "" }, "facet_sympathy": { "name": "Sympathy", "percentile": "" } }
	if "personality" not in data:
		print(data)
	else:
		for personality in data["personality"]:
			for child in personality["children"]:
				personalities[child["trait_id"]]["percentile"] = child["percentile"]

		for v in data["consumption_preferences"]:
			for pref in v["consumption_preferences"]:
				consumptions[pref["consumption_preference_id"]]["value"] = pref["score"]
		
		row = []
		traits = {}
		for trait in data["personality"]:
			traits[trait["name"]] = trait["percentile"]
			
		row.append(traits["Openness"])
		row.append(traits["Conscientiousness"])
		row.append(traits["Extraversion"])
		row.append(traits["Agreeableness"])
		row.append(traits["Emotional range"])
		
		for p in dict(personalities):
			row.append(personalities[p]["percentile"])

		for c in dict(consumptions):
			row.append(consumptions[c]["value"])
		return row

def getPersonality(text):
	url =  os.getenv("WATSON_URL")
	r = requests.post(url, data = text.encode('latin-1', 'replace'), auth=HTTPBasicAuth(api_key_username, api_key_password), headers={"Accept":"application/json", "Content-Type":"text/plain;charset=utf-8"})
	if DEBUG:
		print(r.text)
	return processPersonality(json.loads(r.text))


output = csv.writer(open(inputfile.lower().replace(".csv","_watson-personality_"+datetime.date.today().strftime("%d%m%Y")+".csv"), 'wt')) 
output.writerow(["Name"]+big5_headers+personality_headers+consumption_headers)

with open(inputfile) as f:
	reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL)
	for line in reader:
		data = getPersonality(line[text_index])
		output.writerow([line[uid_index]]+data)
			
	
