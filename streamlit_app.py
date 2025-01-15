## streamlit run "C:\Users\Jack\Documents\Python_projects\streamlit_apps\csv_network_mapper\streamlit_app.py"

### IMPORTS ################################################

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from pyvis.network import Network
import pyvis


### FUNCTIONS ################################################

def plotNetwork(df, node_scaler, node_shape):
                
    g = pyvis.network.Network(
        directed=False, 
        width = "100%", 
        height = "100%", 
    )
    
    ###
    
    df_nodes = pd.concat([df['node_left'], df['node_right']]).value_counts().to_frame().rename(columns = {0: 'count'})
    df_nodes['count'] = df_nodes['count'] / df_nodes['count'].max() # Normalise. Scaling happens when node is added
    df_nodes['rgba'] = df_nodes["count"].apply(lambda x:  f'rgba(100, 100, {x * 255}, 1') #     f'0,0,{ * 255},1'
    nodes_unique = list(df_nodes.index)
    
    ### Add nodes
    for node in nodes_unique:
        g.add_node(node, 
                   size = int(df_nodes.loc[node, 'count'] * node_scaler), 
                   color = df_nodes.loc[node, 'rgba'],
                   shape = node_shape
                  )
        
    ### Add edges
    for index, row in df.iterrows():
        g.add_edge(row['node_left'], row['node_right'], color = 'lightblue')
        
    ### Display   
    path = '/tmp'
    g.save_graph(f'temp.html')
    HtmlFile = open(f'temp.html', 'r', encoding='utf-8')
    
    components.html(
        HtmlFile.read(), 
        height = 500, 
        width = 777
    )
    
    st.write('   ')

    
### MAIN SCRIPT ################################################

required_columns = ['node_left', 'connection', 'node_right']

st.markdown("**Open Investigation Tools** | [constituent.au](%s)" % 'http://www.constituent.au')
    
st.title('CSV Network Mapper')
st.write('A drag and drop network mapper. Makes network mapping easy.')

uploaded_file = st.file_uploader("Upload file here &#x2935;", type={"csv"}) 
if uploaded_file is not None:
    
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
                ["dot", "square", "diamond"],
                #isabled=st.session_state.disabled,
            )
        
            node_scaler = st.slider("Node scaler", 0, 50, 10)
        
        plotNetwork(df, node_scaler, node_shape)
        
        st.write()
        st.write()
        st.dataframe(df, width = 777)
        
        
                
                


