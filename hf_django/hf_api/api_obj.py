import pandas as pd
import requests
import json
import sys
from textblob import TextBlob
# from django.http import JsonResponse
from .s3_dataset_connector import _DL_URLS
#from urllib.parse import urlparse, parse_qs


class HF_API():

    def __init__(self,params):
            
        self.parseArgs(params)
        self.getData()
        self.filterResults()
        
        
        if self.facet:
            self.getAggregates()
            self.response = {'aggregate': self.agg_dict,
                     'data': self.df.to_dict('records'),
                     'HTTP Response': 200}
        
        else:
            self.response = {'HTTP Response': 200,
                'data' : self.df.to_dict('records')}

    def checkToken(self): 
        #Create env file for this token

        if self.token != 'test17502104bl3k2':
            raise ValueError("Wrong API token")
            return {"HTTP Response": 403, "Error": "Invalid API Token"}
        
    def parseArgs(self,params):  
        
        # parsed_url = urlparse(url)
        # args = parse_qs(parsed_url.query)
        args = params
        
        self.category = self.obtainCategory(args.get('category',None))
        self.token = args.get('api-key', None)
        self.query_text = args.get('q', None)
        self.start_date = args.get('startDate', None)
        self.end_date = args.get('endDate', None)
        self.date = args.get('date', None)
        self.star_rating = args.get('starRating', None)
        self.helpful_votes = args.get('helpfulVotes', None)
        self.review_id = args.get('reviewId', None)
        self.facet = dict(params).get('facet', [None]),
        self.limit = int(args.get('limit',25))
        
        self.checkToken()
        
    
    def getSentimentScore(self):
       scores = set()
       if not self.df.empty:
           for text in self.df['review_body']:
               testimonial = TextBlob(text)
               sScore = testimonial.sentiment.polarity
               scores.add(sScore)
           
           average_score = sum(scores)/len(scores)
           return average_score
    
    def getAggregates(self):
       
       self.agg_dict = {}
       self.facet = self.facet[0]
       desc = self.df.describe() 
       if 'avg' in self.facet:
           print("in")
           self.agg_dict['average'] = desc.loc['mean'].to_json()
       if 'max' in self.facet:
           self.agg_dict['max'] = desc.loc['max'].to_json()
       if 'min' in self.facet:
           self.agg_dict['min'] = desc.loc['min'].to_json()
       if 'sentiment' in self.facet:
           self.agg_dict['sentimentScore'] = self.getSentimentScore()
    
    def obtainCategory(self,cat):
        try: 
            if cat:
                data_option = cat+"_v1_00"
                _DL_URLS[data_option]
                return data_option
        
        except KeyError:
            print("category not found!")
            sys.exit({"HTTP Response": 400, "Error": "Invalid Category"})
        
    
    def getData(self):
        #Obtain entire dataset requested by user
        category = self.category
        hf_url = f"https://datasets-server.huggingface.co/first-rows?dataset=amazon_us_reviews&config={category}&split=train"
        
        response = requests.get(hf_url)
        data = json.loads(response.text)
        df = pd.json_normalize(data, 'rows', max_level=1, )
        df = df.drop(['truncated_cells','row_idx'], axis=1)
        df['row.review_date'] = pd.to_datetime(df['row.review_date'])
        
        self.df = df
        
    def filterResults(self):
        
        
        # Find queries in review body
        if self.query_text:
            self.df = self.df[self.df['row.review_body'].str.contains(self.query_text)]
        # Filter by start and end date
        if self.start_date and not self.date:
            self.df = self.df[self.df['row.review_date'] >= self.start_date ]
        if self.end_date and not self.date:
            self.df = self.df[self.df['row.review_date'] <= self.end_date ]
        # Sort by date
        if self.date and not self.end_date and not self.start_date:
            self.df = self.df[self.df['row.review_date'] == self.date ]
        # Sort by star rating
        if self.star_rating:
            self.df = self.df[self.df['row.star_rating'] == int(self.star_rating)]
        # Sort by helpful votes
        if self.helpful_votes:
            self.df = self.df[self.df['row.helpful_votes'] == int(self.helpful_votes)]
        # Sort by review id
        if self.review_id:
            self.df = self.df[self.df['row.review_id'] == self.review_id]
        
        self.df.columns = self.df.columns.str.removeprefix('row.')
        self.df['review_date'] = self.df['review_date'].astype(str)
        self.df = self.df.head(self.limit)
