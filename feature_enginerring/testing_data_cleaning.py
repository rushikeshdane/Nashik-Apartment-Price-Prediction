from read_data.get_data import  get_data
from feature_enginerring.data_cleaning import  fill_missin_value , outlier_removal
df = get_data(path='../read_data/raw_data.csv')
#print(df)

data_after_removing_null = fill_missin_value(df)
#print(data_after_removing_null.isnull().sum())

data_after_removing_null.to_csv('data_after_removing_null')

o = outlier_removal(data_after_removing_null)
#print(o.print_upper_and_lowerbound())
#print(o.check_outlier_in_BHK())
print(o.remove_outlier())

data_after_removing_outlier = o.remove_outlier()
data_after_removing_outlier.to_csv('data_after_remove_outlier')

