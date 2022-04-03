import  pandas as pd
from read_data.get_data import  get_data
from feature_enginerring.feature_encoding import create_new_location_column, encoding

desired_width=320
pd.set_option('display.width', desired_width)
#np.set_printoption(linewidth=desired_width)
pd.set_option('display.max_columns',10)


df = get_data(path= 'data_after_remove_outlier')
#print(df)

data_after_adding_location = create_new_location_column(df)
print(data_after_adding_location)
data_after_adding_location.to_csv('data_after_adding_location_column')

o = encoding(data_after_adding_location)
#print(o.frequecy_encoding_location())
#print(o.mean_encode_location())

data_after_encoding = o.mean_encode_location()
print(data_after_encoding)


data_after_encoding.to_csv('data_after_encoding')
