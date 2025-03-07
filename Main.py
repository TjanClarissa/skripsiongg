import pandas as pd
import streamlit as st
import matplotlib as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import os
pd.options.display.float_format = '{:.2f}'.format
sns.set_theme(rc={'axes.formatter.limits': (-8, 9)})

#set title of the page

st.set_page_config(page_title="Segmentation", page_icon=":bank:",layout="wide")
#st.sidebar.success("Select pages below")

st.title(" :bank: Customer Segmentation Dashboard")
st.write("This data used in this dashboard is taken from an official site Kaggle")
st.write("Total entries were 1,048,567 and for this analysis, only 52,402 entries are used for the sake of time efficiency")
st.write("Steps of this analysis: EDA (Exploratory Data Analysis) -> RFM Analysis -> Clustering")
#load dataset
@st.cache_data
def load_data(path: str):
    data = pd.read_csv(path)
    return data

st.subheader("Let's see the original data :mag_right:")
df = load_data("final_transaction.csv")
df = df.drop('Unnamed: 0', axis=1)
st.write(df)

st.write("Columns explanation: :bell:")
cul1, cul2 = st.columns((2))
with cul1:
    st.write("1. TransactionID      : Unique value for each transaction made :bellhop_bell:")
    st.write("2. CustomerID         : Unique value for each customer :bald_person:")
    st.write("3. CustomerDOB        : Date of birth of customer :calendar:")
    st.write("4. CustGender         : Gender of customer (F/M) :woman-frowning: :man-frowning:")
    st.write("5. CustLocation       : Location of the customer :world_map:")
with cul2:
    st.write("6. CustAccountBalance : Balance in the customer's account :heavy_dollar_sign:")
    st.write("7. TransactionDate    : Date when the transaction was made :lower_left_paintbrush:")
    st.write("8. TransactionTime    : Time of the transaction :mantelpiece_clock:")
    st.write("9. TransactionAmount  : Amount of money transacted in INR :money_with_wings:")

#create 2 column 
col1, col2 = st.columns((2))

#create bar chart for 1st column
with col1:
    st.subheader("Amount of transactions per Gender")
    sum1 = df.groupby('CustGender')['TransactionAmount'].sum()
    df_new = sum1.reset_index()
    fig = px.bar(df_new, x = "CustGender", y = "TransactionAmount", text = ['INR {:,.2f}'.format(x) for x in df_new["TransactionAmount"]],
                 template = "seaborn", color= "CustGender",labels={
                     "CustGender": "Gender",
                     "TransactionAmount": "Sum Transaction Amount"
                 },)
    st.plotly_chart(fig,use_container_width=True, height = 200)

with col2:
    st.subheader("Amount of Account Balance per Gender")
    sum2 = df.groupby('CustGender')['CustAccountBalance'].sum()
    df_new1 = sum2.reset_index()
    fig1 = px.bar(df_new1, x = "CustGender", y = "CustAccountBalance", text = ['INR {:,.2f}'.format(x) for x in df_new1["CustAccountBalance"]],
                 template = "seaborn", color= "CustGender",labels={
                     "CustGender": "Gender",
                     "CustAccountBalance": "Account Balance"
                 })
    st.plotly_chart(fig1,use_container_width=True, height = 200)

ca1, ca2 = st.columns((2))
with ca1:
    with st.expander("Transaction per Gender table"):
        st.write(df_new)
        csv = df_new.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Transaction_Gender.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

with ca2:
    with st.expander("Account Balance per Gender table"):
        st.write(df_new1)
        csv = df_new1.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Balance_Gender.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')




#Displaying distribution of age
st.subheader("How's the distribution of age?")
bins = [18, 22, 27, 32, 37, 42]
labels = ['18-22', '23-27', '28-32', '33-37', '38-42']
ages = df.copy()
ages['agegroup'] = pd.cut(ages.Age, bins, labels = labels,include_lowest = True)
now = ages.groupby('agegroup').agg(
    total_customer = ('CustomerID', 'count')
)
now1 = now.reset_index()
fig2 = px.bar(now1, x = "agegroup", y = "total_customer", text = ['{:,}'.format(x) for x in now1["total_customer"]],
                 template = "seaborn", color= "agegroup",labels={
                     "agegroup": "Age",
                     "total_customer": "Total Customer"
                 })
st.plotly_chart(fig2,use_container_width=True, height = 200)

with st.expander("Age group data"):
    st.write(now1)
    csv = now1.to_csv(index = False).encode('utf-8')
    st.download_button("Download Data", data = csv, file_name = "Age_Group.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')

#display top 5 location 
st.subheader("Top 10 Locations for customers")
locations = df.groupby('CustLocation').agg(
    total_customer = ('CustomerID', 'count'),
    total_transaction = ('TransactionAmount', 'sum'),
    total_acc_balance = ('CustAccountBalance', 'sum')
)
locations1 = locations.reset_index()
sorted_df = locations1.sort_values(by='total_customer', ascending= False)
new_location = sorted_df.loc[sorted_df['total_customer'] >= 1158]
new_location = new_location.reset_index(drop=True)
new_location.index = np.arange(1, len(new_location)+1)
st.write(new_location)

csv = new_location.to_csv(index = False).encode('utf-8')
st.download_button("Download Data", data = csv, file_name = "TOP_Location.csv", mime = "text/csv",
                    help = 'Click here to download the data as a CSV file')

#display frequency transaction each month
cl1, cl2 = st.columns((2))
transaction_part = df.copy()
with cl1:
    st.subheader("frequent transaction each month?")
    transaction_part['month'] = pd.to_datetime(transaction_part['TransactionDate']).dt.month
    frequent = transaction_part.groupby('month').agg(
        total_transaction= ('CustomerID','count')
    )
    frequent = frequent.reset_index()
    frequent.index = np.arange(1, len(frequent)+1)
    frequent = frequent.drop('month', axis = 1)
    #st.write(frequent, "Hello")
    fig3 = px.line(frequent, template = "seaborn",labels={
                     "index": "Month"
                 })
    st.plotly_chart(fig3,use_container_width=True, height = 200)

with cl2:
    st.subheader("sum transaction each month")
    jumlah = transaction_part.groupby('month').agg(
        sum_transaction= ('TransactionAmount','sum')
    )
    jumlah = jumlah.reset_index()
    jumlah.index = np.arange(1, len(jumlah)+1)
    jumlah = jumlah.drop('month', axis = 1)
    #st.write(jumlah)
    fig4 = px.line(jumlah, template = "seaborn",labels={
                     "index": "Month"
                 })
    st.plotly_chart(fig4,use_container_width=True, height = 200)

st.write("All events happening in August-September 2016 that leads to high transactions: ")
st.write("1. Teej                               : Women apply henna on their palms and feet, wear traditional clothes for the reunion of Shiva and Parvati. ")
st.write("2. Naag Panchami                      : Celebrated by Hindus across the country and in Nepal on the fifth day of Shraavan. ")
st.write("3. Nehru Trophy Snake Boat Race       : One of the biggest and most awaited boat races in Kerala.")
st.write("4. Independence Day                   : Biggest celebrations are held at the Red Fort in Delhi.")
st.write("5. Jhapan Mela                        : Celebrated in honor of snakes.")
st.write("6. Raksha Bandhan                     : Celebrates the relationship between the brother and his sister.")
st.write("7. Krishna Janmashtami                : Commemorates the birth of Krishna.")
st.write("8. Gogamedi Fair                      : Festival celebrated in India to pay homage to snakes, regionally referred to as Gogaji.")
st.write("9. Feast Of Our Lady Of Good Health   : Millions of people visit the church during the festivities and the feast goes on for 10 days.")
st.write("10. Mim Kut Festival                  : The festival is a colorful affair and a celebration of a successful harvesting season.")