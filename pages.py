import streamlit as st
from scrapping import scrap_city,sub_scrap
import matplotlib.pyplot as plt
import time
import seaborn as sns
from streamlit_lottie import st_lottie
import json
from streamlit_lottie import st_lottie_spinner
st.set_option('deprecation.showPyplotGlobalUse', False)
def city_page(loc1):
    try:
        if len(loc1)>0:
            df,endpoint_url=scrap_city(loc1) 
            df=df.rename(columns={'ProjectC':'ProjectCount'}) 
            if True:
    
                    sort_df = df[['Area', 'ProjectCount']].sort_values('ProjectCount', ascending=False).head(10)
    
                    # Create a bar chart with Matplotlib
                    fig, ax = plt.subplots(figsize=(10,6))  # Adjust the size as needed
                    ax.bar(sort_df['Area'], sort_df['ProjectCount'])
    
                    # Customize the chart
                    ax.set_xlabel('Area')
                    ax.set_ylabel('Listed Properties')
                    ax.set_title('Top 10 Areas by Properties Count')
                    ax.tick_params(axis='x', rotation=90) 
                    plt.style.use('ggplot') 
    
                    st.pyplot(fig)
                    
                    st.divider()
    except:
        df,endpoint_url=scrap_city(loc1) 
        st.write("Please select some different city")
        st.write(endpoint_url)

def load_lot(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)                
                    
def suburbs_page(loc1):
    
    sns.set_style("whitegrid")
    sns.set_palette("colorblind")
    lottie_cod=load_lot("anime/Animation.json")
    try:
        df=scrap_city(loc1) 
        df=df.rename(columns={'ProjectC':'ProjectCount'}) 
            # Simulate a long-running process
        df=scrap_city(loc1) 
        df=df.rename(columns={'ProjectC':'ProjectCount'}) 
        suburb = st.selectbox("Select Suburbs/Area", ["None"]+df['Area'].to_list())
        if suburb== "None":
            st.info('Please Select Area from SelectBox')
        
        else:
            count=round( df.loc[df['Area'] == suburb, 'ProjectCount'].iloc[0],2)
            href_sub=df.loc[df['Area'] == suburb, 'href'].iloc[0]
            apx_time= round(count * 0.05,2) 
            with st_lottie_spinner(lottie_cod):
                df=sub_scrap(href_sub) 
            sfig, axs = plt.subplots(1, 2, figsize=(12, 6))
    
    # Plot status counts
            status_counts = df['Status'].value_counts()
            axs[0].bar(status_counts.index, status_counts.values)
            axs[0].set_xlabel('Status')
            axs[0].set_ylabel('Count')
            axs[0].set_title('Status Counts')
            bhk_counts = df['BHK'].value_counts()
            axs[1].bar(bhk_counts.index, bhk_counts.values)
            axs[1].set_xlabel('BHK')
            axs[1].set_ylabel('Count')
            axs[1].set_title('BHK Counts')
    
    
    
            # Adjust layout
            plt.tight_layout()
            st.pyplot()
            st.caption(f"<b>This graph displays the distribution of 'Ready to Move' and 'Under Construction' properties across different BHK categories in {suburb}.</b>", unsafe_allow_html=True)
            st.divider()
            
            average_price_by_bhk = df.groupby('BHK')['Price'].mean()
            plt.bar(average_price_by_bhk.index, average_price_by_bhk.values)
            plt.xlabel('BHK')
            plt.ylabel('Average Price')
            plt.title('Average Price by BHK')
            
            st.pyplot()
            st.caption("Insights from the bar graph:")
            for i in range(len(average_price_by_bhk)):
                average_price_formatted = "{:,.2f}".format(average_price_by_bhk.values[i])
                st.caption(f"<b>Average Price of <b>{average_price_by_bhk.index[i]} BHK</b> in <b>{suburb}</b> is <b>₹{average_price_formatted}</b></b>", unsafe_allow_html=True)
            
            
            average_price = df.groupby(['BHK', 'Status'])['Price'].mean().unstack()
            st.divider()
    
            # Plot grouped bar chart
            average_price.plot(kind='bar')
            plt.xlabel('BHK')
            plt.ylabel('Average Price')
            plt.title('Average Price by BHK and Status')
            plt.xticks(rotation=0)
    
            plt.legend(title='Status')
    
            # Show plot
            st.pyplot()
            st.caption(f"<b>This graph illustrates the average property prices categorized by BHK configuration and status. It provides insights into the pricing dynamics based on the number of bedrooms (BHK) and the property's current status (Ready to Move or Under Construction) within the {suburb} area.</b>", unsafe_allow_html=True)
    except:
        st.info("Some Error Encountered")
        
def about_page():

    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='font-size: 36px; color: #333;'>Welcome to PropertyPulse</h1>
        <p style='font-size: 18px; color: #666; line-height: 1.6;'>
            PropertyPulse revolutionizes real estate insights with the seamless integration of AWS Lambda technology. No longer do users need to sift through countless listings or navigate confusing interfaces—PropertyPulse streamlines the real estate hunt by leveraging AWS Lambda for web scraping, delivering the latest property data tailored to your location with unparalleled efficiency.
        </p>
        <p style='font-size: 18px; color: #666; line-height: 1.6;'>
            With PropertyPulse, gaining access to a comprehensive overview of your local real estate landscape is as simple as a few clicks. From market trends to property listings, our app empowers users with a wealth of information at their fingertips, all thanks to the robust capabilities of AWS Lambda.
        </p>
        <p style='font-size: 18px; color: #666; line-height: 1.6;'>
            But the benefits don't end there. By harnessing the power of AWS Lambda, we go beyond mere data presentation. Through the integration of Exploratory Data Analysis (EDA), PropertyPulse provides users with insightful visualizations and analytics, enabling them to make informed decisions about buying, selling, or investing in real estate like never before.
        </p>
        <p style='font-size: 18px; color: #666; line-height: 1.6;'>
            And the future holds even greater promise. With AWS Lambda at the helm, PropertyPulse is poised to roll out cutting-edge predictive models, forecasting property prices, rental trends, and much more. Our vision is clear—to redefine the real estate landscape, one innovative feature at a time, all powered by the unparalleled capabilities of AWS Lambda.
        </p>
    </div>
    """, unsafe_allow_html=True)
