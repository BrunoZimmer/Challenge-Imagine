import requests
import json

r = requests.get('https://inputhc.onxzy.dev/api/night/usage/real', params={
    'date_start': '2019-01-23', 
    'date_end': '2020-12-30' 
})

reponse = r.json()
print(reponse)
r = requests.get('https://inputhc.onxzy.dev/api/night/usage/plan', params={
    'date_start': '2019-01-23', 
    'date_end': '2020-12-30' 
})

reponse = r.json()
print(reponse)



