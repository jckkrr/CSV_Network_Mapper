## streamlit run "C:\Users\Jack\Documents\Python_projects\streamlit_apps\csv_network_mapper\streamlit_app.py"

### IMPORTS ################################################

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from pyvis.network import Network
import pyvis

css = 'body, html, p, h1, .st-emotion-cache-1104ytp h1, [class*="css"] {font-family: "Inter", sans-serif;}'
st.markdown( f'<style>{css}</style>' , unsafe_allow_html= True)

    
### FUNCTIONS ################################################

def plotNetwork(df, plot_formatting):
                
    g = pyvis.network.Network(
        directed=False, 
        width = "100%", 
    )
    pyvis.options.Layout(improvedLayout=True)    
    g.force_atlas_2based(spring_length=3)
    
    ### NODES
    ### 1. Collate list of nodes, then prepare them
     
    palette = {
        'primary': 'rgba(102, 99, 236, 1)', 
        'secondary': 'rgba(0, 150, 25, 1)',
        'tertiary': 'rgba(0, 150, 25, 1)',
        'blank_image': 'https://upload.wikimedia.org/wikipedia/commons/a/a7/Blank_image.jpg',
    }
    
    df_nodes = pd.concat([df['node_left'], df['node_right']]).value_counts().to_frame().rename(columns = {0: 'count'})
    
    df_nodes['proportion'] = df_nodes['count'] / df_nodes['count'].max() # Normalise. Scaling happens when node is added
    df_nodes['size'] = df_nodes['proportion'] * plot_formatting['node_scaler']
    
    def styleNode(styling_column, style_high, style_mid, sytle_low): 
        df_nodes[styling_column] = np.where(df_nodes['proportion'] > 0.66, style_high, np.where(df_nodes['proportion'] > 0.33, style_mid, sytle_low))
    
    #styleNode('rgba', palette['primary'], palette['secondary'], palette['tertiary'])
    #styleNode('shape', plot_formatting['node_shape'], plot_formatting['node_shape'], 'circularImage')
    #styleNode('image', '', '', palette['blank_image']) ### This is used for making the small nodes look like empty rings. Works in combination with 'circularImages' shape.
    #df_nodes['font_size'] = 10 + (df_nodes['proportion'] * 15)
    
    st.dataframe(df_nodes, width = 777)
    
    ### 2. Add the nodes to graphic
    
    nodes_unique = list(df_nodes.index)
    for node in nodes_unique:
        
        #st.write(df_nodes.loc[node])
        
        g.add_node(node, 
                   #size = df_nodes.loc[node, 'size'], 
                   #color = df_nodes.loc[node, 'rgba'],
                   #shape = df_nodes.loc[node, 'shape'],
                   #image = df_nodes.loc[node, 'image'],
                   #font = (f'{df_nodes.loc[node, "font_size"]} Manrope black')
                  )
        
    ### EDGES
    for index, row in df.iterrows():
        g.add_edge(row['node_left'], row['node_right'], color = palette['secondary'])
    
    #### DISPLAY REMOVED TEMPORARILY
    
    
    
### MAIN SCRIPT ################################################

required_columns = ['node_left', 'connection', 'node_right']

st.markdown("**Open Investigation Tools** | [constituent.au](%s)" % 'http://www.constituent.au')
    
st.title('CSV Network Mapper')
st.write('A drag and drop network mapper. Makes network mapping easy.')

uploaded_file = st.file_uploader("Upload file here &#x2935;", type={"csv"})
if uploaded_file:
#if uploaded_file is not None:

    file_name = uploaded_file.name
    
    df = pd.read_csv(uploaded_file)
    
    ### Clean up white spaces that will inevitably be in the CSV
    df.columns = [x.strip() for x in df.columns]
    for col in df.columns:
        if col in required_columns:
            df[col] = [x.strip() for x in df[col]]
    
    column_name_search = [x for x in required_columns if x in list(set(df.columns))]
    if len(column_name_search) != 3:    
        st.write('Columns must be "node_left", "connection", "node_right"')
    else:

        df = df[required_columns]
        
        col1, col2 = st.columns(2)

        with col1:
             
            st.write(' ')
            #st.checkbox("Disable formatting", key="disabled")

        with col2:
                    
            node_shape = st.radio(
                "Node shape",
                ["square", "dot", "diamond"],
            )
        
            node_scaler = st.slider("Node scaler", 0, 50, 10)
        
        plot_formatting = {'title': file_name, 'node_scaler': node_scaler, 'node_shape': node_shape}
        plotNetwork(df, plot_formatting)
        
        st.write()
        st.write()
        st.dataframe(df, width = 777)
        
#### END ##########################