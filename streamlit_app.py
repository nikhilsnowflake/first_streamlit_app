import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title("My Parents new Healthy Diner")
streamlit.header("Breakfast Favourites")
streamlit.text(":bowl_with_spoon: Omega 3 & Blueberry Oatmeal")
streamlit.text(":green_salad: Kale, Spinach & Rocket Smoothie")
streamlit.text(":chicken: Hard-Boiled Free-Range Egg")
streamlit.text(":avocado::bread: Avocado Toast")
streamlit.header(':banana::mango: Build Your Own Fruit Smoothie :kiwifruit::grapes:')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")
fruits_selected = streamlit.multiselect("Pick some fruits: ", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
#diplay the table on the page
streamlit.dataframe(fruits_to_show)
#created a function for api call
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
#New section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input("Which fruit would you like information about?")
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
streamlit.header("View our fruit list - Add your favourites")
#Snowflake related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    my_cnx.close()
    return my_cur.fetchall()
#Add a button to load the fruit
if streamlit.button("Get fruit load list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)
#Allowing the user to add fruit
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute(f"insert into fruit_load_list values ('{new_fruit}')")
    my_cnx.close()
    return "thanks for adding " + new_fruit
add_my_fruit = streamlit.text_input("Which fruit would you like to add?")
if streamlit.button("Add fruit to list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)

