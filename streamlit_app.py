# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests



# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
   """Choose the fruits you want in your custom smoothie!"""
)


name_on_order = st.text_input("Name of Smoothie:")
st.write("The name on your Smoothie will be:",name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('Fruit_Name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list=st.multiselect (
    'Choose up to 5 ingredients:',
    my_dataframe
)

if ingredient_list:
     
     ingredient_string=''
     for fruit_chosen in ingredient_list:
         ingredient_string+=fruit_chosen+' '
         st.subheader(fruit_chosen + 'Nutrition Information')
         smoothiefroot_response=requests.get("https://my.smoothiefroot.com/api/fruit/"+ fruit_chosen)
         sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
     #st.write(ingredient_string)

     my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredient_string + """')"""

     #st.write(my_insert_stmt)
     time_to_insert=st.button('Submit Order')
     if time_to_insert:
        session.sql(my_insert_stmt).collect()
     if ingredient_string:
         session.sql(my_insert_stmt).collect()
         st.success('Your Smoothie is ordered!', icon="✅")

         

