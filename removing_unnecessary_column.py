import statsmodels.formula.api as smf

def remove_unnecessary_column(df):

    try:

        df = df.copy()
        df.drop(['address', 'owners','cordinates', 'latitude', 'longitude','location','new_cordinates'],axis = 1,inplace = True)
        return df
    except  Exception as e:
        pass

def stat(data):

    lm = smf.ols(formula='price ~ BHK+total_sqft+ housetype+house_condition+location_mean_encode',data=data).fit()
    return lm.summary()

