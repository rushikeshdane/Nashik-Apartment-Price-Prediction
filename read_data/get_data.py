

import pandas as pd

# create a function to get data
try :

    def get_data(path ='raw_data.csv' ):
        df = pd.read_csv(path,index_col=0)
        df.reset_index(inplace=True,drop=True)
        return df

except Exception as e:
    pass
