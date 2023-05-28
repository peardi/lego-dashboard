import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.express.colors import sample_colorscale
from datetime import datetime, timedelta
from PIL import Image

def do_stuff_on_page_load():
    st.set_page_config(layout="wide")

do_stuff_on_page_load()

st.header('Theme Explorer', anchor=None)

#Set Sidebar Elements
with st.sidebar:
    st.header('Filters', anchor=None)
    values = st.slider(
        'Select the Start and End Years',
        1950, 2017, (1950, 2017))
    st.write('Date Range: '+str(values[0])+'-01-01 to '+str(values[1])+'-01-01')

#Import Data
df = st.session_state['df']
df_filtered = df[(df.year >= values[0]) & (df.year <= values[1])]
df_sets_to_theme = df_filtered[['year','parent_theme_name','theme_name','set_name','num_parts']].drop_duplicates()


#Get Top N Themes
#👇 Paste the code to create a slider input widget with possible values between 1 and 20. Set default value to 10 and save the output to a new variable called filt_n_themes
#👇 You can find the documentation here - https://docs.streamlit.io/library/api-reference/widgets/st.slider
filt_n_themes = st.slider("Number of Top themes", 1, 20, 10) 


#Explore the Themes to Sets relationship
#👇 Create an expander container widget with title "Theme Explorer Sunburst". Remember that everything contained on the container must be idented
with st.expander(f"Theme Explorer Sunburst",expanded=True):

    #👇 Create spinner that displays "Loading..." while running. Remember that everything contained on the spinner must be idented
    with st.spinner(text="Loading..."): #Replace the ... by the spinner method
        #👇 Paste the code created in activity 3.1 to produce a list of parent themes
        list_parent_themes = df_sets_to_theme.groupby('parent_theme_name').nunique('set_name').sort_values('set_name',ascending=False).reset_index()
        list_parent_themes = list_parent_themes.parent_theme_name.tolist()[:filt_n_themes]
        
        #👇 Create a select box widget to gather from the user what Parent Theme is to be output. Pass the following label 'What theme do you want to explore?' as well as the list_parent_themes
        # Save the user selected option to a chosen_theme variable
        #https://docs.streamlit.io/library/api-reference/widgets/st.selectbox
        option = st.selectbox('What theme do you want to explore?',list_parent_themes)
        st.write('You selected:', option)

        #👇 Paste the code created in activity 3.1 to produce the df_sunburst DataFrame
        df_sunburst = df_filtered[['parent_theme_name','theme_name','set_name']].drop_duplicates()
        df_sunburst['nbr'] = 1
        df_sunburst = df_sunburst.loc[df_sunburst.parent_theme_name.isin([option])].dropna()
        #👇 Paste the code created in activity 3.1 to create the visualization of the df_sunburst DataFrame
        fig = px.sunburst(
          df_sunburst,
          path=['parent_theme_name','theme_name','set_name'],
          values ='nbr',
          height=900,
          color_discrete_sequence=px.colors.qualitative.Plotly
        )

        #👇 Use a plotly widget from Streamlit to visualize the fig_sunburst plot. Pass the parameter use_container_width =True to ensure the visualization expands to the container width.
        st.plotly_chart(fig,use_container_width=True)


#Table Explorer
#👇 Create an expander container widget with title "Theme Explorer Table". Remember that everything contained on the container must be idented
with st.expander(f"Theme Explorer Table",expanded=True):

    #👇 Create spinner that displays "Loading..." while running.  Remember that everything contained on the spinner must be idented
    with st.spinner(text="Loading..."):

        #👇 Paste the code created in activity 3.2 to produce a DataFrame with details 'parent_theme_name','theme_name',
        #                                                                              'year','set_num',
        #                                                                              'set_name','num_parts',
        #                                                                              'part_num','part_name',
        #                                                                              'part_category_name','quantity',
        #                                                                              'color_name','is_trans'

        df_table_sets = df_filtered[['parent_theme_name','theme_name','year','set_num','set_name','num_parts','part_num','part_name','part_category_name','quantity','color_name','is_trans']].drop_duplicates()
        df_table_sets = df_table_sets[df_table_sets.parent_theme_name.isin([option])]


        #👇 Use a plotly widget from Streamlit to output an interactive table with df_table_sets. Pass the parameter use_container_width =True to ensure the visualization expands to the container width.
        st.dataframe(data=df_table_sets, use_container_width =True)
