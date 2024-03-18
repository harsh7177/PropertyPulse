import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import streamlit as st
import boto3
import pandas as pd
from io import StringIO
import json

@st.cache_data
def scrap_city(loc1):
    import os

# Access the GitHub secret
    endpoint_url = os.getenv("ENDPOINT_URL")
    post = {"loc": str(loc1),"href":"None"}
    response = requests.post(endpoint_url, json=post)
    z=response.text
    response_body_dict = json.loads(z)
    dic=json.loads(response_body_dict['body'])

    df=pd.DataFrame.from_dict(dic)
    return df,endpoint_url

def sub_scrap(href):
    endpoint_url = "https://stgpxl9ok3.execute-api.us-east-1.amazonaws.com/dev"
    post = {"loc": "None","href":href}
    response = requests.post(endpoint_url, json=post).text
    response_body_dict = json.loads(response)
    dic=json.loads(response_body_dict['body'])
    df=pd.DataFrame.from_dict(dic)
    return df
    
