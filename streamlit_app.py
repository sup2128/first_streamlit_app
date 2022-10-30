import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My Parents New Healthy Dinner')

def get_fruityvice_data(fruit_choice):
  fruityvice_response=requests.get("https://www.fruityvice.com/api/fruit/"+fruit_choice)
  streamlit.header("FruityVice Advice")
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from pc_rivery_db.public.fruit_load_list " )
    my_data_row = my_cur.fetchall()
    return my_data_row

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.

streamlit.dataframe(fruits_to_show)
try:
  fruit_choice=streamlit.text_input('which fruit you want?')
  if not fruit_choice:
    streamlit.error('Please select fruit')
  else:
    fruityvice_normalized = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_normalized)
finally:
  streamlit.text('done')

if streamlit.button('Get Fruit Load List'):
  
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_data_row = get_fruit_load_list()

streamlit.text("Fruitload list contains")

streamlit.dataframe(my_data_row)
#my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('streamlit')")


