import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import os
#pd.options.display.float_format = '{:.2f}'.format
sns.set_theme(rc={'axes.formatter.limits': (-8, 9)})

st.title("K-Means Clustering")
#load dataset
@st.cache_data
def load_data(path: str):
    data = pd.read_csv(path)
    return data

st.subheader("Clustering Data")
df = load_data("final_KMeans.csv")
rfm = load_data("final_RFM.csv")
transaction = load_data("final_transaction.csv")

#merging data 
df["CustomerID"] = rfm["CustomerID"]
df["Segment"] = rfm.groupby('CustomerID')['Segment'].first().values
df["Gender"] = transaction.groupby('CustomerID')['CustGender'].first().values
df["Location"] = transaction.groupby('CustomerID')['CustLocation'].first().values

df = df.drop('Unnamed: 0', axis=1)

st.write(df)

csv = df.to_csv(index = False).encode('utf-8')
st.download_button("Download Data", data = csv, file_name = "KMeans_Data.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')


#population per cluster
st.subheader("How many customer per cluster")
population = df.groupby("Cluster").agg(
    total_customer = ("CustomerID","count")
)
population = population.reset_index()

fig1 = px.bar(population, x = "Cluster", y = "total_customer", text = ['{:,}'.format(x) for x in population["total_customer"]],
                 template = "seaborn", color= "Cluster")
st.plotly_chart(fig1,use_container_width=True, height = 200)


#age per cluster
st.subheader("Age per cluster")
fig, ax = plt.subplots(figsize=(12, 4))
sns.countplot(x="Age", hue="Cluster", data=df, ax = ax)
st.pyplot(fig,use_container_width=True, height = 200)

#Segment per cluster
st.subheader('Segment per cluster')
cluster0 = df.loc[df["Cluster"] == 0]
cluster1 = df.loc[df["Cluster"] == 1]
cluster2 = df.loc[df["Cluster"] == 2]

segment0 = cluster0.groupby('Segment').agg(
    total_customer = ("CustomerID", "count")
)
segment0 = segment0.reset_index()

segment1 = cluster1.groupby('Segment').agg(
    total_customer = ("CustomerID", "count")
)
segment1 = segment1.reset_index()

segment2 = cluster2.groupby('Segment').agg(
    total_customer = ("CustomerID", "count")
)
segment2 = segment2.reset_index()

c1,c2,c3 = st.columns((3))
with c1:
    st.write(segment0)
    fig2 = px.pie(segment0, values = "total_customer", names = "Segment", template = "plotly_dark")
    fig2.update_traces(text = segment0["Segment"], textposition = "inside")
    st.plotly_chart(fig2,use_container_width=True)
with c2:
    st.write(segment1)
    fig3 = px.pie(segment1, values = "total_customer", names = "Segment", template = "plotly_dark")
    fig3.update_traces(text = segment1["Segment"], textposition = "inside")
    st.plotly_chart(fig3,use_container_width=True)
with c3:
    st.write(segment2)
    fig4 = px.pie(segment2, values = "total_customer", names = "Segment", template = "plotly_dark")
    fig4.update_traces(text = segment2["Segment"], textposition = "inside")
    st.plotly_chart(fig4,use_container_width=True)

#Transaction Amount per cluster
st.subheader('Average transaction per cluster')
amount = df.groupby("Cluster").agg(
    Average_amount = ("AverageAmount", "mean"),
    total_amount = ("TotalAmount","sum")
)
amount = amount.reset_index()
fig5 = px.bar(amount, x = "Cluster", y = "Average_amount", text = ['INR {:,.2f}'.format(x) for x in amount["Average_amount"]],
                 template = "seaborn", color= "Cluster")
st.plotly_chart(fig5,use_container_width=True, height = 200)

with st.expander("Transaction per Gender table"):
    st.write(amount)
    csv = amount.to_csv(index = False).encode('utf-8')
    st.download_button("Download Data", data = csv, file_name = "Transaction_amount_cluster.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')


st.subheader("Conclusion:")
st.write("Cluster 1 consist of customers at the age of 29-42 with most of them fall into other and hibernating customer categories. The customers in this cluster should be paid more attention to minimize the loss of customers")
st.write("Cluster 2 consist of customers from all age with 40.8% of them being big spenders and can be seen from the average amount of transactions.")
st.write("Cluster 3 is similar to cluster 1 but for younger customers and that may cause the average amount of transactions is less than cluster 1 & 2")