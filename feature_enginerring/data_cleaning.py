import  pandas as pd
from impyute.imputation.cs import mice
import  numpy as np

def fill_missin_value(df):

      imputed = mice(df[['price',
                         'per_month_emi', 'total_sqft']].values)

      new_data = pd.DataFrame(imputed, columns=['price',
                                                'per_month_emi', 'total_sqft'])
      temp_df = df[['address', 'owners', 'housetype', 'house_condition', 'BHK', 'cordinates', 'latitude', 'longitude']]

      frames = [temp_df, new_data]
      clean_data = pd.concat(frames, axis=1)

      clean_data.dropna(inplace=True)

      return clean_data

class  outlier_removal:
    def __init__(self,df):
        self.df = df

    def find_IQR(self,datacolumn):

        Q1, Q3 = np.percentile(datacolumn, [25, 75])
        IQR = Q3 - Q1
        lower_range = Q1 - (1.5 * IQR)
        upper_range = Q3 + (1.5 * IQR)
        return lower_range, upper_range

    def print_upper_and_lowerbound(self):
        list_of_columns = [ 'price',
           'per_month_emi', 'total_sqft']
        for  column in list_of_columns:
            lowerbound,upperbound = self.find_IQR(self.df[column])
            print(column)
            print('upperbound : ',upperbound)
            print('lowerbound : ',lowerbound)
            print('   ')




    def check_outlier_in_BHK(self):
        print("BHK values having  less than 10 count in dataframe :")
        print('   ')
        BHK = self.df['BHK'].value_counts()
        BHK_lessthan10count = BHK[BHK <= 10]
        print(BHK_lessthan10count)

        frames = [self.df[(self.df['BHK'] == 2.5)], self.df[(self.df['BHK'] == 3.5)], self.df[(self.df['BHK'] == 10.0)], self.df[(self.df['BHK'] == 8.0)],
                  self.df[(self.df['BHK'] == 7.0)]]
        filterd = pd.concat(frames)
        print('***' * 40)
        print('Index of outlier in BHK')
        return filterd.index


    def removing_outlier_from_BHK(self):
        filtered_data = self.df.drop(index=[172, 4739, 5485, 4519, 4553, 4864, 5052, 2145, 4767, 5020, 4429,
                                       4784, 4835, 4889, 4908, 4930, 5050, 5166])

        return filtered_data


    def remove_outlier(self):
        df = self.removing_outlier_from_BHK()
        df.drop(df[(df.price > 100.76) | (df.price < 0)].index, inplace=True)
        df.drop(df[(df.per_month_emi > 39.71) | (df.per_month_emi < 0)].index, inplace=True)
        df.drop(df[(df.total_sqft > 1894.24) | (df.total_sqft < 143.45)].index, inplace=True)

        outlier_removed_data = df.copy()
        outlier_removed_data.reset_index(drop=True, inplace=True)

        return outlier_removed_data