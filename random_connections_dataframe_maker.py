import pandas as pd
import numpy as np

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