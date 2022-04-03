import  pandas as pd

def create_new_location_column(df):
    try:

        location = df['cordinates'].value_counts()
        location_count_lessthan10 = location[location < 10]
        df['new_cordinates'] = df['cordinates'].apply(
            lambda x: 'other' if x in location_count_lessthan10 else x)

        l1 = []
        for cordinate in df['new_cordinates']:
            v = cordinate.split(sep=',')
            l1.append(v[0])

        location = pd.DataFrame(l1, columns=['location'])

        new_data_with_location = pd.concat([df, location], axis=1, verify_integrity=True)

        return new_data_with_location
    except  Exception as e:
        pass


class encoding:

    def __init__(self,data):
        self.data = data


    def label_encoding_husetype_housecondition(self):
        try:
            dff = self.data
            dff['housetype'] = dff['housetype'].map({'Apartment': 1, 'Independent house': 0})
            dff['house_condition'] = dff['house_condition'].map({'new': 1, 'old': 0})
            return dff
        except  Exception as e:
            pass


    def frequecy_encoding_location(self):
        try:
            df = self.label_encoding_husetype_housecondition()
            frequency = df.groupby('location').size() / len(df)
            df['location_frequency_encode'] = df['location'].map(frequency)
            return df
        except  Exception as e:
            pass


    def mean_encode_location(self):
        try:
            df = self.label_encoding_husetype_housecondition()

            mean_encode = df.groupby('location')['price'].mean()
            # print(mean_encode.head(45))
            df['location_mean_encode'] = df['location'].map(mean_encode)
            return df
        except  Exception as e:
            pass
