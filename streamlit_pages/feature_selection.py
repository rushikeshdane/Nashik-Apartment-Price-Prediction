import streamlit as st
import pandas as pd
import  get_data
import select_feature
import train_test_split
import removing_unnecessary_column
try:
    df = get_data.get_data(path='data_after_removing_unnecessary_column')

    #print(df)
    o= train_test_split.split(df)
    x_train = o.X_train()
    y_train =o.y_train()
    x_test = o.X_test()
    y_test=o.y_test()

    o2 = select_feature.feature_selection(x_train,y_train)
except Exception as e:
    pass


def app():
    try:

        st.sidebar.subheader('What is Feature Selection ?')
        with st.sidebar.expander('see explanation '):
            st.markdown('Feature selection is the process of isolating the most consistent, non-redundant, and relevant features to use in model construction. Methodically reducing the size of datasets is important as the size and variety of datasets continue to grow. ')
            st.markdown('The main goal of feature selection is to improve the performance of a predictive model and reduce the computational cost of modeling')


        st.subheader('removing unnecessary column from dataset')
        with st.expander('see explanation'):


            st.write('address , cordinates, new_cordinates ,location  columns representing nearly same thing and I had '
                     'selected location column for encoding so , we cam remove other columns')
            st.write('owners column does not contribute in price prediction for house similarly latitude and longitude is '
                     ' used for plotting the graph so we can remove this column')
            st.markdown('removed columns : address, owners,cordinates, latitude, longitude,location,new_cordinates')

        st.subheader('How statistics of our dataset looks ?')
        with st.expander('see statistics'):
            st.write( removing_unnecessary_column.stat(df))

        st.header('Methods used for feauture selection')
        st.subheader('method1 : pearson correlation')
        st.write(o2.correlation_matrix())
        with st.expander('see observation'):
            st.markdown('1) housetype, house_conditon is having really low correlation with price')
            st.markdown('2) per_moth_emi is highly correlated with price and total_sqft it is causing problem of '
                      ' multicollinearity ,we need to drop this column')
        with st.expander('what is pearson correlation?'):
            st.markdown(' It is a measure of linear correlation between two sets of data. It is the ratio between the covariance'
                        ' of two variables and the product of their standard deviations; thus it is essentially a normalized'
                        ' measurement of the covariance, such that the result always has a value between −1 and 1')

        st.subheader('method 2 : Information gain')
        st.plotly_chart(o2.plot_information_gain(),use_container_width=True)
        with st.expander('see explanation'):
            st.write("check out this [link](https://machinelearningmastery.com/information-gain-and-mutual-information"
                     "/#:~:text=Mutual%20Information%20Related%3F-,What%20Is%20Information%20Gain%3F,samples%2C%20and%"
                     "20hence%20less%20surprise.)")

        st.subheader('method 3: Backward elimination method')
        with st.expander('see explanation'):
            st.markdown('Backward elimination (or backward deletion) is the reverse process. '
                        
                        ' All the independent variables are entered into the equation first and each one is deleted one '
                        'at a time if they do not contribute to the regression equation')
    except Exception as e:
        st.write(e)
        pass
