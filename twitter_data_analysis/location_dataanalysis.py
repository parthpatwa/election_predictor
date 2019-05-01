import pandas as pd 
from .dataanalysis import get_stats_for_df
import re
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def get_popular_hashtags(lst,n):
	hashes = {}
	for tweet in lst:
		tweet_hash = [word  for word in tweet.split() if word.startswith("#") ]
		for hashtag in tweet_hash:
			if hashtag in hashes:
				hashes[hashtag] += 1
			else:
				hashes[hashtag] = 0
	sorted_hashes = sorted(hashes.items(), key=lambda kv: kv[1])
	return sorted_hashes[:n]
def get_stats_for_location(location):
	directory = os.path.join(os.path.join(BASE_DIR,'tweets'),'location')
	fname = location + '_english.csv'
	df = pd.read_csv(os.path.join(directory,fname))
	df['text length'] = df['tweet'].apply(len)
	popular_hashes = get_popular_hashtags(lst,10)
	stats = get_stats_for_df(df)
	return stats , popular_hashes