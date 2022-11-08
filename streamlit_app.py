import streamlit
import pandas

streamlit.title('My Parents New Healthy Diner')

streamlit.header('🧑‍🚀 Breakfast Menu')
streamlit.text('🐲 Omega 3 & Blueberry Oatmeal')
streamlit.text('🌸 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥯 Hard-Boiled Free Range Eggs')

streamlit.header('🧆🧆 Build Your Own Fruit Smoothie 🍠🍠')

# We're going to use a CSV file from that bucket in our app. The file is here: https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt
# We want pandas to read our CSV file from the S3 bucket so we use a pandas function called read_csv  to pull the data into a dataframe we'll call my_fruit_list. 

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# Choose the Fruit Name Column as the Index
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# Display the table on the page.

# After pulling the data into a pandas dataframe called my_fruit_list, we will ask the streamlit library to display it on the page by typing:

streamlit.dataframe(my_fruit_list)

