import streamlit
import requests
import pandas
import snowflake.connector
from urllib.error import URLError

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

# Let's put a pick list here so they can pick the fruit they want to include and pre-populate the list to set an example for the customer. 
# We'll ask our app to put the list of selected fruits into a variable called fruits_selected. 
# Then, we'll ask our app to use the fruits in our fruits_selected list to pull rows from the full data set (and assign that data to a variable called fruits_to_show). 
# Finally, we'll ask the app to use the data in fruits_to_show in the dataframe it displays on the page. 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)     
      # take the json version of the response and normalize it
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      # output it as a table
        streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error()

      
      
#streamlit.write('The user entered ', fruit_choice)



# streamlit.text(fruityvice_response.json()) #writes the data to the screen

streamlit.stop()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
#streamlit.text(my_data_rows)
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit')
streamlit.write('The user entered ', add_my_fruit)

# After pulling the data into a pandas dataframe called my_fruit_list, we will ask the streamlit library to display it on the page by typing:

streamlit.dataframe(fruits_to_show)

my_cur.execute("insert into fruit_load_list values ('from streamlit')");

