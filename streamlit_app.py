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
    
    styleNode('rgba', palette['primary'], palette['secondary'], palette['tertiary'])
    styleNode('shape', plot_formatting['node_shape'], plot_formatting['node_shape'], 'circularImage')
    styleNode('image', '', '', palette['blank_image']) ### This is used for making the small nodes look like empty rings. Works in combination with 'circularImages' shape.
    df_nodes['font_size'] = 10 + (df_nodes['proportion'] * 15)
        
    ### 2. Add the nodes to graphic
    
    nodes_unique = list(df_nodes.index)
    for node in nodes_unique:
        
        #st.write(df_nodes.loc[node])
        
        g.add_node(node, 
                   size = df_nodes.loc[node, 'size'], 
                   color = df_nodes.loc[node, 'rgba'],
                   shape = df_nodes.loc[node, 'shape'],
                   image = df_nodes.loc[node, 'image'],
                   font = (f'{df_nodes.loc[node, "font_size"]} Manrope black')
                  )
        
    ### EDGES
    for index, row in df.iterrows():
        g.add_edge(row['node_left'], row['node_right'], color = palette['secondary'])
    
    ### DISPLAY   
      
    path = '/tmp'
    g.save_graph(f'temp.html')
    HtmlFile = open(f'temp.html', 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(
        source_code, 
        height = int(610), 
        width = int(777)
    )
    
    ### Make some slight improvements to the download graph
    source_code = source_code.replace('height: 600px', 'height: 1000').replace('height: 500px', 'height: 1000')    
    source_code = source_code.replace('border: 1px solid lightgray', 'border: 0px solid lightgray') # removes border that otherwise appears
    source_code = source_code.replace('background-color:rgba(200,200,200,0.8)', 'background: linear-gradient(to bottom right, #33ccff 0%, #ff99cc 100%);')
    source_code = source_code.replace(
        '</style>', 
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;900&display=swap"></style>'
    )
    source_code = source_code.replace(
        '<body>', 
        f'<body><span style="font-family: Manrope; font-size: 24px; font-weight:600">{plot_formatting["title"]}</span><br> \
            <span style="font-family: Inter; font-size: 14px;"><b>Open Investigation Tools</b> | <a href="http://www.constituent.au" style="color:#000000;">constituent.au</a></span>'
    )
    
    st.download_button(
        label = "For easier analysis, download as HTML",
        data = source_code,
        file_name = "downloadable_html.html",
        mime = "application/octet-stream",
    )
    
    
def randomDataframe():
    
    index_length = range(0, np.random.randint(10, 100))

    names = ['Alice', 'Bob', 'Courtney', 'Dehlia', 'Emma', 'Fiona', 'Garry', 'Harry', 'Ian', 'Julia', 'Karen', 'Laurel', 'Michelle'] ## Plus 'Neville'
    connection_type = ['likes', 'loves', 'knows', 'works with']

    df = pd.DataFrame(
        {'node_left': [names[np.random.randint(len(names))] for x in index_length], 
         'connection': [connection_type[np.random.randint(len(connection_type))] for x in index_length], 
         'node_right': [names[np.random.randint(len(names))] for x in index_length]}
    )

    df['node_right'] = np.where(df['node_right'] == df['node_left'], 'Neville', df['node_right'])

    return df

    
    
### MAIN SCRIPT ################################################

required_columns = ['node_left', 'connection', 'node_right']

st.markdown("**Open Investigation Tools** | [constituent.au](%s)" % 'http://www.constituent.au')
    
st.title('CSV Network Mapper')
st.write('A drag and drop network mapper. Makes network mapping easy.')

uploaded_file = st.file_uploader("Upload file here &#x2935;", type={"csv"})

if not uploaded_file:
    
    df_random = randomDataframe() .to_csv(index=False).encode('utf-8')
    st.download_button(
       '... or generate a random CSV test file to use.',
       df_random,
       "random_dataframe.csv",
       "text/csv"
    )



if uploaded_file:

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