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
    endpoint_url = "https://stgpxl9ok3.execute-api.us-east-1.amazonaws.com/dev"
    post = {"loc": str(loc1),"href":"None"}
    response = requests.post(endpoint_url, json=post)
    z=response.text
    response_body_dict = json.loads(z)
    dic=json.loads(response_body_dict['body'])

    df=pd.DataFrame.from_dict(dic)
    return df

def sub_scrap(href):
    endpoint_url = "https://stgpxl9ok3.execute-api.us-east-1.amazonaws.com/dev"
    post = {"loc": "None","href":href}
    response = requests.post(endpoint_url, json=post).text
    response_body_dict = json.loads(response)
    dic=json.loads(response_body_dict['body'])
    df=pd.DataFrame.from_dict(dic)
    return df
def area(href):
        result = {
            'BHK': [],
            'Status': [],
            'Size(Sq/ft)': [],
            'Price/Sqft': [],
            'Price': [],
            'bath': []
        }
        
        try:
            scrap = bs(requests.get(url).text, 'html.parser')
        except (requests.RequestException, bs4.FeatureNotFound, bs4.SoupStrainer) as e:
            print(f"Error occurred while scraping: {e}")
            return pd.DataFrame(result)  # Return an empty DataFrame if there's an error
        
        for i in scrap.find_all('div', class_='search-result-footer'):
            x = i.text
            if '...' in x:
                area_page = x.split('...')[-1].strip()
            else:
                for j in x.strip():
                    area_page = j
        try:
            for i in range(int(area_page)):
                sub_url = url if i == 0 else f'{url}?page={i + 1}'
                try:
                    area_scrap = bs(requests.get(sub_url).text, 'html.parser')
                except (requests.RequestException, bs4.FeatureNotFound, bs4.SoupStrainer) as e:
                    print(f"Error occurred while scraping: {e}")
                    continue  # Skip to the next iteration if there's an error
                
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
        except Exception as e:
            print(f"Error occurred while scraping: {e}")
        
        df = pd.DataFrame(result)
        return df
    
    # Example usage
               
