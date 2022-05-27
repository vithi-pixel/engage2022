from itertools import groupby
import pandas
import streamlit as st 
import requests 
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt

make=""
model=""

# reading json file
def get_data():
    f = open('csvjson.json', 'r')
    return json.loads(f.read())

# searching for the model and make in the json file to show matching results
def fun(element):
	if element['Make'] == make and element['Model']== model:
		return True
	else:
		return False

# html styling 
CARS_HTML_TEMPLATE = """
<div style="width:100%;
height:100%;
width:800px;
margin:10px;
padding:20px;
position:relative;
box-shadow:0 0 1px 1px;
color:white;">
<h4 style="color:#18A558">Brand : {} &ensp; Model : {} &ensp;  Variant : {}</h4> 
<h4 style="color:green"> Price : {}</h4>
<h6>Fuel Tank Capacity : {}  &ensp; Fuel Type : {} &ensp;  Body Type : {}</h6> 
<h6>Mileage : {} &ensp; Gears : {} &ensp; Power : {}</h6>
<h6>Seating Capacity : {} &ensp; Type : {} &ensp; Number of Airbags : {}</h6>
</div>
"""

CARS_DES_HTML_TEMPLATE = """
<div style='color:#fff'>
{}
</div>
"""
	
# Making two pages one being the home page and another being the Data analysis page
def main():
    global make,model
    menu = ["Home","Data Analysis"]
    choice = st.sidebar.selectbox("MENU",menu)

    st.title("CAR DHUNDO.COM")

    if choice == "Home":
        st.subheader("Home")
        # creating a search form for getting inputs of make(car brand) and model name and a submit button
        with st.form(key='searchform'):
            nav1,nav2,nav3 = st.columns([3,2,1])

            with nav1:
                make=st.text_input("Search Company")

            with nav2:
                model = st.text_input("Model name")

            with nav3:
                st.text("Search")
                submit_search=st.form_submit_button(label='Search')
            
        #with the help of this the input is diplayed and shows what is being searched
        st.success("Searched for company {} and name {}".format(make,model))

        col1 , col2= st.columns([2,3])

        with col1:
            if submit_search:
                # calling the function where json file is being read to find the results
                data = get_data()
                # defining a variable and storing the values of whose match is found  
                filtered = filter(fun,data)   
                # converting the values for which data is matched to list
                filtered_list = list(filtered)
                # using len function to show how many matching results are found 
                num_of_results = len(filtered_list)  

                st.subheader("Showing {} results".format(num_of_results))
                
                # executinf=g this for loop to display all the features of the car
                for i in filtered_list:
                    Make = i['Make']
                    Model = i['Model']
                    Variant = i['Variant']
                    Price = i['Ex-Showroom_Price']
                    Fuel_Tank_Capacity = i['Fuel_Tank_Capacity']
                    Fuel_Type = i['Fuel_Type']
                    MBody_Type = i['Body_Type']
                    ARAI_Certified_Mileage = i['ARAI_Certified_Mileage']
                    Gears = i['Gears']
                    Power = i['Power']
                    Seating_Capacity = i['Seating_Capacity']
                    Type = i['Type']
                    Number_of_Airbags = i['Number_of_Airbags']
                    st.markdown(CARS_HTML_TEMPLATE.format(Make,Model,Variant,Price,Fuel_Tank_Capacity,Fuel_Type,MBody_Type,ARAI_Certified_Mileage,Gears,Power,Seating_Capacity,Type,Number_of_Airbags),unsafe_allow_html=True)

    # in else loop we enter Data Analysis page        
    else:
        st.subheader("Data Analysis")

        #reading csv file for which i did the cleaning according to what atttributes i wanted to keep
        data = pd.read_csv("cars_engage_2022.csv")

        # finding out the distinct car comapnies in the dataset 
        v = len(pd.unique(data['Make']))
        st.text(f"Data is analysed for {v} car companines")

        # Pie chart - categorizing cars on the basis of Car type(Manual, Automatic etc.)
        p1=pd.unique(data['Type'])  #uniquely indentifying types and counting them
        v1=pd.unique(data['Type'].value_counts(sort=False))
        
        fig1 = go.Figure(
            go.Pie(
            labels = p1,
            values = v1,
            hoverinfo = "label+percent",
            textinfo = "value"
        ))
        st.header("Data analysis on the basis of Car Type")
        st.plotly_chart(fig1)

        # Pie chart - categorizing cars on the basis of Car Fuel type(petrol,diesel etc)
        p2=pd.unique(data['Fuel_Type'])  #uniquely indentifying types and counting them
        v2=pd.unique(data['Fuel_Type'].value_counts(sort=False))
       
        fig2 = go.Figure(
            go.Pie(
            labels = p2,
            values = v2,
            hoverinfo = "label+percent",
            textinfo = "value"
        ))
        st.header("Data analysis on the basis of Fuel Type")
        st.plotly_chart(fig2)

        
        # srush = pd.unique(data['Make']+" "+data['Model'])
        # sbsrush = st.selectbox(label='X axis' , options=srush)
        # print(sbsrush)

        # Scatter plot
        st.title("Scatter Plot")

        # sorting out just the columns with integer values
        numeric_columns = data.select_dtypes(['float64' , 'float32', 'int32', 'int64']).columns
        print(numeric_columns)

        # making drop down boxes
        sb1 = st.selectbox(label='X axis' , options=numeric_columns)
        print(sb1)
        sb2 = st.selectbox(label='Y axis' , options=numeric_columns)
        print(sb2)

        #displaying scatter plot based of selected choices for x and y axis
        sn = sns.relplot(x=sb1, y=sb2, data=data)
        st.pyplot(sn)

        # Pie chart - categorizing cars on the basis of Car Companies
        a = pd.unique(data['Make'])  #uniquely indentifying types and counting them
        c = pd.unique(data['Make'].value_counts(sort=False))
        fig = go.Figure(
            go.Pie(
            labels = a,
            values = c,
            hoverinfo = "label+percent",
            textinfo = "value"
        ))
        st.header("Cars of each company")
        st.plotly_chart(fig)

if __name__ == '__main__':
	main()
