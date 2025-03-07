import pandas as pd
import streamlit as st
import matplotlib as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import os
#pd.options.display.float_format = '{:.2f}'.format
sns.set_theme(rc={'axes.formatter.limits': (-8, 9)})

st.title("RFM Analysis")
#load dataset
@st.cache_data
def load_data(path: str):
    data = pd.read_csv(path)
    return data

#st.subheader("After RFM Analysis")
st.write("RFM analysis is used to analyze existing customer behavior and stands for Recency, Frequency and Monetary value")

st.write("Recency: How recent a customer made a transaction")
st.write("Frequency: How frequently they've made a transaction")
st.write("Monetary: How much money they've transacted")

df = load_data("final_RFM.csv")
df = df.drop('Unnamed: 0', axis=1)
st.write(df)

csv = df.to_csv(index = False).encode('utf-8')
st.download_button("Download Data", data = csv, file_name = "RFM_Data.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')

#pie chart for segment and information
chart1, chart2 = st.columns((2))

segment = df.groupby("Segment").agg(
    total_count = ("CustomerID","count"),
    Average_amount = ("AverageAmount", "mean"),
    Average_age = ("Age","mean")
)
segment = segment.reset_index()
segment['Average_age'] = segment['Average_age'].astype(int)

with chart1:
    st.subheader('Average amount per segment')
    fig = px.pie(segment, values = "Average_amount", names = "Segment", template = "plotly_dark")
    fig.update_traces(text = df["Segment"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

with chart2:
    st.subheader('Detail table')
    st.write(segment)
    csv = segment.to_csv(index = False).encode('utf-8')
    st.download_button("Download Data", data = csv, file_name = "Segmentation.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')
    
st.write("Big spenders          : Low recency, Low frequency, High monetary -> customers who may not transact oftern but when they do, they transacted a significant amount of money")
st.write("Best customer         : High recency, frequency and monetary -> customers who made transaction often, spent the most, and recently made a transaction")
st.write("Loyal customer        : Low recency, High monetary, High frequency -> customers who visited often with medium to high spending")
st.write("Hibernating customer  : Low recency, monetary, frequency -> customer's last visit was long back, visit are not often and has not spent much")
st.write("New customer          : High recency, low frequency and monetary -> recent customers who have made a small or one-time purchases")
st.write("Other                 : Medium recency, frequency, monetary -> customers who have moderate engagement")

    
#Recency
st.subheader("Recency")
recency = df.copy()
bins = [0, 120, 200, float('inf')]  # Define the bin edges
labels = ['0-120 days', '120-200 days', '>200 days']  # Define the labels for the bins

# Create a new column 'Recency_Bucket' based on the defined bins
recency['Recency_Bucket'] = pd.cut(recency['Recency'], bins=bins, labels=labels, right=False)

recency1 = recency.groupby("Recency_Bucket").agg(
    total_customer = ("CustomerID","count")
)
recency1 = recency1.reset_index()
#st.write(recency1)
fig1 = px.bar(recency1, x = "Recency_Bucket", y = "total_customer", text = ['{:,}'.format(x) for x in recency1["total_customer"]],
                 template = "seaborn", color= "Recency_Bucket",labels={
                     "Recency_Bucket": "Duration from last transaction",
                     "total_customer": "total_customer"
                 })
st.plotly_chart(fig1,use_container_width=True, height = 200)
    




