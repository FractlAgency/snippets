import os, csv
from google.cloud import bigquery

subreddit = "SUBREDDIT_HERE"

config = {
	"dataset":"data",
	"project": os.environ("PROJECT_ID"),
	"table":'reddit_'+subreddit+'_comments',
}
query = "SELECT * FROM `fh-bigquery.reddit_comments.2*` WHERE subreddit = \""+subreddit+"\";"
client = bigquery.Client(project=config["project"])
job_config = bigquery.QueryJobConfig()
table_ref = client.dataset(config["dataset"]).table(config["table"])
job_config.destination = table_ref
query_job = client.query(
    query,
    location="US",
    job_config=job_config,
) 

query_job.result() 

tb = client.dataset(config["dataset"], project=config["project"]).table(config["table"])
extract_job = client.extract_table(
    tb,
    "gs://{}/{}".format('fractl-reddit-comments', config["table"]+'_*.csv'),
    location="US",
) 
extract_job.result()
os.system('gsutil -m cp -r gs://fractl-reddit-comments/'+config["table"]+'_*.csv .')
