from read_data.get_data import  get_data
from feature_selection.removing_unnecessary_column import  stat,remove_unnecessary_column
from feature_selection.select_feature import feature_selection
from feature_selection.train_test_split import  split

df = get_data(path='../feature_enginerring/data_after_encoding')

#print(df)

data_afer_removing_unnecessary_column = remove_unnecessary_column(df)
data_afer_removing_unnecessary_column.to_csv('data_after_removing_unnecessary_column')
print(data_afer_removing_unnecessary_column)
print(stat(data_afer_removing_unnecessary_column))

o= split(data_afer_removing_unnecessary_column)
x_train = o.X_train()
y_train =o.y_train()
x_test = o.X_test()
y_test=o.y_test()

o2 = feature_selection(x_train,y_train)
print(o2.information_gain())
print(o2.correlation_matrix())
print(o2.plot_information_gain())
print(o2.vif_score())

print(x_test)