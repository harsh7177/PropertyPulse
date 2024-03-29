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
    endpoint_url = st.secrets["endpoint_url"]
    post = {"loc": str(loc1),"href":"None"}
    response = requests.post(endpoint_url, json=post)
    z=response.text
    response_body_dict = json.loads(z)
    dic=json.loads(response_body_dict['body'])

    df=pd.DataFrame.from_dict(dic)
    return df

def sub_scrap(href):
    endpoint_url = st.secret["endpoint_url_2"]
    post = {"loc": "None","href":href}
    response = requests.post(endpoint_url, json=post).text
    response_body_dict = json.loads(response)
    dic=json.loads(response_body_dict['body'])
    df=pd.DataFrame.from_dict(dic)
    return df
def area(href):
        url=href
        result = {
                    'BHK': [],
                    'Status': [],
                    'Size(Sq/ft)': [],
                    'Price/Sqft': [],
                    'Price': [],
                    'bath':[]
                }
                
        scrap = bs(requests.get(url).text, 'html.parser')
        for i in scrap.find_all('div',class_='search-result-footer'):
            x=i.text
            if '...' in x:
                area_page=x.split('...')[-1].strip()
            else:
                for j in x.strip():
                    area_page=j
        for i in range(int(area_page)):
                    sub_url = url if i == 0 else f'{url}?page={i + 1}'
                    area_scrap = bs(requests.get(sub_url).text, 'html.parser')
                    
                    for td in area_scrap.find_all('td', class_='lbl rate'):
                        result['Price/Sqft'].append(int(td.text.split('/')[0].replace(',', '')))
                        
                    for ul in area_scrap.find_all('ul', class_='listing-details'):
                        try:
                            result['bath'].append(ul.find(title='Bathrooms').text.split('Bathrooms')[0])
                        except AttributeError:
                            result['bath'].append(None)
                        
                    for td in area_scrap.find_all('td', class_='size'):
                        result['Size(Sq/ft)'].append(td.text)
                        
                    for td in area_scrap.find_all('td', class_='val'):
                        result['Status'].append(td.text)
                        
                    for td in area_scrap.find_all('td', class_='price'):
                        price_text = td.text.strip()
                        if 'Cr' in price_text:
                            result['Price'].append(round(float(price_text.split('Cr')[0].strip()) * 10000000, 1))
                        elif 'L' in price_text:
                            result['Price'].append(round(float(price_text.split('L')[0].strip()) * 100000, 1))
                            
                    for div in area_scrap.find_all('div', class_='title-line'):
                        bhk_text = div.text.split('BHK')[0].strip()
                        result['BHK'].append(int(bhk_text) if bhk_text.isdigit() else None)
        df=pd.DataFrame(result)
        return df
