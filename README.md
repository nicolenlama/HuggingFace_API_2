# Hugging Face API for US Amazon Reviews
API to access public Hugging Face US Amazon Review Dataset using Django framework
The API is currently hosted on an EC2 Instance and using Hugging Face's first row API 

* Django is a Python web framework that is comprehensive and secure. I choose it because it scales for large applications. Python is my preferred language so I choose it for this project. Additionally, Python's readibility, large community, and valuable, useful libraries made it the most appealing choice in lieu of Rust, C#/Java, or JavaScript.
* EC2 allows users to easily upload their web applications to the cloud. I have used an elastic IP address to make the server public. I used an EC2 instance for ease of use for the purposes of this assignment
* NGINX and Gunicorn are used as the web server for the Django app. I choose these technologies because they tend to perform best in production (as opposed to Apache) and are more secure.
* Pandas, Textblob, JSON, Requests libraries were used to query, filter, process and return json data as HTTP response. 
* Please visit the todo list below to see how I would improve this API. 

*Note: For now, please use token test17502104bl3k2*

# Review Search
## Overview

Use the Hugging Face Amazon US API to look up reviews by keyword. You can refine your search using filters and facets.
Must specify category in the URL. Limit results with limit parameter

Example Call

Get Tool reviews with "good" and their aggregated sentiment score, and limit 10 results
`http://3.233.212.196/hf_api/api/search/v1/data.json?q=good&category=Tools&limit=10&facet=avg&facet=sentiment&api-key=test17502104bl3k2`


**Categories**


* Wireless
* Watches
* Video_Games
* Video_DVD
* Video
* Toys
* Tools
* Sports
* Software
* Shoes
* Pet_Products
* Personal_Care_Appliances
* PC
* Outdoors
* Office_Products
* Musical_Instruments
* Music
* Mobile_Electronics
* Mobile_Apps
* Major_Appliances
* Luggage
* Lawn_and_Garden
* Kitchen
* Jewelry
* Home_Improvement
* Home_Entertainment
* Home
* Health_Personal_Care
* Grocery
* Gift_Card
* Furniture
* Electronics
* Digital_Video_Games
* Digital_Video_Download
* Digital_Software
* Digital_Music_Purchase
* Digital_Ebook_Purchase
* Camera
* Books
* Beauty
* Baby
* Automotive
* Apparel
* Digital_Ebook_Purchase
* Books


## FILTERING YOUR SEARCH

Use filters to narrow the scope of your search. You can specify the fields and the values that your query will be filtered on.

Filter Query Parameters

* starRating
* helpfulVotes
* date
* startDate
* endDate
* category
* reviewID

Example call querying for Beauty reviews with "hair" and startdate 2015-03-31 and limit 2 results

`http://3.233.212.196/hf_api/api/search/v1/data.json?q=hair&category=Beauty&startDate=2015-03-31&limit=2&api-key={token}`

Example call for Furniture reviews with the word "nice" in them and a star rating of 4

`http://3.233.212.196/hf_api/api/search/v1/data.json?q=nice&category=Furniture&starRating=4&api-key={token}`


USING FACETS
Use facets to view the aggregates of the search terms.

The following fields can be used as facet fields: 
* avg 
* sentiment
* max
* min

Specify facets using the facet parameter. Set facet=<field> and the response will contain an array with a count for the top 3 terms that have the highest count for each facet.

Query with aggregates average and sentiment:

`http://3.233.212.196/hf_api/api/search/v1/data.json?category=Health_Personal_Care&facet=avg&facet=sentiment&api-key={my_token}`

By default facet counts ignore all filters and return the count for all results of a query. 

Here is the facet array response to the query.
```json
{'aggregate': {'average': star_rating          2.000000
helpful_votes        0.166667
total_votes          0.500000
vine                 0.000000
verified_purchase    0.833333
'max': star_rating          2.0
helpful_votes        1.0
total_votes          1.0
vine                 0.0
verified_purchase    1.0
, 'min': star_rating          2.0
helpful_votes        0.0
total_votes          0.0
vine                 0.0
verified_purchase    0.0
, 'sentimentScore': -0.06798941798941802}
      ...
```
Examples Requests
      
`https://<ec_instance_ip>/hf_api/api/search/v1/data.json?category=Automotive&facet=avg&facet=max&facet=min&facet=sentiment&starRating=4&api-key={my_token}`

Example Response
Here is an partial example response.

```json
{
   "aggregate":{
      "average":"star_rating          2.000000
helpful_votes        0.166667
total_votes          0.500000
vine                 0.000000
verified_purchase    0.833333
Name":"mean",
      "dtype":float64,
      "max":"star_rating          2.0
helpful_votes        1.0
total_votes          1.0
vine                 0.0
verified_purchase    1.0
Name":"max",
      "dtype":float64,
      "min":"star_rating          2.0
helpful_votes        0.0
total_votes          0.0
vine                 0.0
verified_purchase    0.0
Name":"min",
      "dtype":float64,
      "sentimentScore":-0.06798941798941802
   },
   "data":[
      {
         "marketplace":"US",
         "customer_id":"23260912",
         "review_id":"R2XYDBMHUVJCSX",
         "product_id":"B00PFZFD8Y",
         "product_parent":"344168617",
         "product_title":"NatraCure Plantar Fasciitis Wrap (One Wrap) - 1291-S CAT Arch Support (Small/Medium)",
         "product_category":"Health & Personal Care",
         "star_rating":2,
         "helpful_votes":0,
         "total_votes":1,
         "vine":0,
         "verified_purchase":1,
         "review_headline":"Two Stars",
         "review_body":"I wear it a few times only but the fabric cover the jelly pad already broken.",
         "review_date":"Timestamp(""2015-08-31 00:00:00"")"
      },
              ...
```
Limit Fields in Response
You can limit the number fields returned in the response with the limit parameter.

Resource Types
URIs are relative to https://<EC2_Instance_API_Address>/hf_api/api/search/v1 unless otherwise noted.

Review Data
For more information see Review Data.
Method	Endpoint	Description
GET	/reviewdata.json	
Search Hugging Face US Amazon Review Data Set by keywords and filters.


## TODO

* Get data on proper database such as DynamoDB (right now data is pulled in via HF website using first rows)
* Query data use ORM like SQLAlchemy or pyscopgy2
* Add error handling for date and start/end date. Can only add either or. 
* Add error handling for when users add an end date that is sooner than start date
* Add pagination to api functionality
* Add proper authorization
* Remove all tokens from script. 
* Encrypt tokens and/or add as environment variable (.env)
* Add tokenization to sentiment score to make score more accurate
* Add HTTPS to api
* Add Route53 domain name to instance
* utilize modules folder in Django for better organization
* Refactor code for efficiency
* Increase EC2 instance resources
* Add load balancer to account for increases in API calls
* Add API call limit. for example: 10 queries per second
* Add a front page for API      
      

