# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 21:08:39 2023

@author: nicol
"""

cat = "Automotive"
my_token= 'test17502104bl3k2'
query = "work"
start = "2015-08-24"
end = "2015-08-26"
star = 2
helpv = 0

url = f"https://<ec_instance_ip>/api/search/v1/data.json?category=Tools&starRating=2&limit=2&facet=sentiment&api-key={my_token}"

