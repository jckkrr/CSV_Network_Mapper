## streamlit run "C:\Users\Jack\Documents\Python_projects\streamlit_apps\csv_network_mapper\streamlit_app.py"

### IMPORTS ################################################

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from pyvis.network import Network
import pyvis

st.write('hello_world')

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
        
        
        #col1, col2 = st.columns(2)

        #with col1:
        #    st.checkbox("Disable formatting", key="disabled")

        #with col2:
        #    node_shape = st.radio(
        #        "Node shape",
        #        ["dot", "square", "diamond"],
        #        disabled=st.session_state.disabled,
        #    )
        
         #   node_scaler = st.slider("Node scaler", 0, 50, 10, disabled=st.session_state.disabled,)
        
        # plotNetwork(df, node_scaler, node_shape)
        
        st.dataframe(df)  
        
        
                
                


