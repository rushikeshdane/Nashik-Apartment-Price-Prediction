import streamlit as st
import plotly.express as px
import get_data
from st_aggrid import AgGrid
import pandas as pd


def downnload_button(df, name: str):
    try:
        @st.cache
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(df)
        return st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=name)
    except  Exception as e:
        pass
def app():

    try:
        st.sidebar.subheader('What is Feature Engineering ?')
        with st.sidebar.expander('see explanation'):
            st.markdown('Feature engineering is the process of selecting, manipulating, and transforming raw data into features that can be used in supervised learning. In order to make machine learning work well on new tasks, it might be necessary to design and train better features. As you may know, a “feature” is any measurable input that can be used in a predictive model — it could be the color of an object or the sound of someone’s voice.')
            st.markdown(' Feature engineering, in simple terms, is the act of converting raw observations into desired features using statistical or machine learning approaches')
        st.subheader('How missing values in data are filled ?')
        with st.expander('see explanation'):
            st.subheader('Filling missing values with mice library')


            st.write('MICE, or Multivariate Imputation by Chained Equation (what a memorable term), is an imputation '
                    'method which works by filling the missing data multiple times. Chained Equation approach also has '
                    'the benefit of being able to handle different data types efficiently — such as continuous and binary')

            st.write('The basic idea is to treat each variable with missing values as the dependent variable in a regression, '
                    'with some or all of the remaining variables as its predictors. The MICE procedure cycles through these'
                    ' models, fitting each in turn, then uses a procedure called “predictive mean matching” (PMM) to '
                    'generate random draws from the predictive distributions determined by the fitted models. '
                    'These random draws become the imputed values for one imputed data set')

        with st.expander('Data after filling missing value '):


            st.dataframe(get_data.get_data(path='feature_enginerring/data_after_removing_null'))
            df=get_data.get_data(path='feature_enginerring/data_after_removing_null')


            downnload_button(df,'data_after_removing_null.csv')

        st.subheader('Which method is used for outlier removal ?')
        with st.expander('see explanation'):
            st.subheader('Inter quartile range (IQR) method')

            st.write('1) Find the first quartile, Q1.')
            st.write('2) Find the third quartile, Q3.')
            st.write('3) Calculate the IQR. IQR= Q3-Q1.')
            st.write('4) Define the normal data range with lower limit as Q1–1.5*IQR and upper limit as Q3+1.5*IQR')
            st.write('5) Any data point outside this range is considered as outlier and should be removed for '
                     'further analysis.')

        with st.expander('data after removing outlier'):
            st.dataframe(get_data.get_data(path='feature_enginerring/data_after_remove_outlier'))
            df = get_data.get_data(path='feature_enginerring/data_after_remove_outlier')

            downnload_button(df,name='data_after_removing_outlier.csv')

        st.subheader('creating new column called location')
        with st.expander('see explanation'):
            st.write(' I had created new column name location from existion column address ,in address column we have full '
                     'address of each house which creates more than thousand unique values ,if we distribute houses according '
                     'to their common area(secondary address ) we will reduce category to less than 40  which will be more easy '
                     'for categorical encoding ')

        st.subheader(' Which methods are used for categrical encoding ?')
        with st.expander('see explanation'):
            st.subheader(' columns for encoding house : housetype,house_condition , location')

            st.subheader('method 1 : Label encoding')
            st.write(' In this method we replace labels of categorical column with numerical value '
                     'I had applied this method on housetype and house_condition column as this are '
                     'binary column replacing their labels with 0 and 1 works fine. ')

            st.subheader('method 2 : Mean encoding')
            st.write(' Mean encoding is similar to label encoding, except here labels are correlated directly'
                     ' with the target. ''For example, in mean target encoding for each category in the feature '
                     'label is decided with the mean value of the target variable on training data. This encoding'
                      'method brings out the relation between similar categories, but the connections are bounded within'
                    'the categories and target itself. The advantages of the mean target encoding are that it does not '
                     'affect the volume of the data and helps in faster learning.')

            st.write('steps :')
            st.write('1. Select a categorical variable you would like to transform')
            st.write(' 2. Group by the categorical variable and obtain aggregated sum over the “Target” variable. ')
            st.write('(total number of 1’s for each category in ‘price’)')
            st.write(' 3. Group by the categorical variable and obtain aggregated count over “Target” variable')
            st.write('4. Divide the step 2 / step 3 results and join it back with the train.')

            st.write('I had applied this method on location column ')
        with st.expander('data after Feature encoding'):
            st.dataframe(get_data.get_data(path='feature_enginerring/data_after_encoding'))
            df = get_data.get_data(path='feature_enginerring/data_after_encoding')

            downnload_button(df,name='data_after_feature_encoding.csv')

        def histogram(data, columname:str,xaxis_title:str) :
            fig1 = px.histogram(data_frame=data,x=data[columname], color_discrete_sequence=['grey'],template='gridon'
                    ,marginal='box',hover_data=['owners', 'house_condition', 'BHK', 'price', 'housetype', 'total_sqft'])
            fig1.update_layout(xaxis_title= xaxis_title)
            return fig1

        st.subheader('how continuous variable distributed after removing outlier ?')
        data_distribution = st.selectbox('select feature',['price','per_month_emi','total_sqft'])
        data_after_removing_outlier=get_data.get_data('feature_enginerring/data_after_remove_outlier')
        if data_distribution =='price':
            st.plotly_chart(histogram(data_after_removing_outlier,columname='price',xaxis_title='price in lakhs'), use_container_width=True)
        if data_distribution== 'total_sqft':
            st.plotly_chart(histogram(data_after_removing_outlier,columname='total_sqft',xaxis_title='total square foot area')
                            , use_container_width=True)

        if data_distribution == 'per_month_emi':
            st.plotly_chart(histogram(data_after_removing_outlier,columname='per_month_emi',xaxis_title='per_month_emi in thousand rs')
                            , use_container_width=True)


        st.subheader('How continous variable correlated with price column ?')

        def feauture_vs_price(data,feature:str):
            fig = px.scatter(data,x = feature,y= 'price',trendline='ols', trendline_color_override='black'
                             ,color_discrete_sequence=['grey'])
            return fig

        scatter_distribution = st.selectbox('select feature', ['per_month_emi', 'total_sqft'])
        if scatter_distribution == 'total_sqft':
            st.plotly_chart(feauture_vs_price(data_after_removing_outlier,'total_sqft'), use_container_width=True)

        if scatter_distribution =='per_month_emi':
            st.plotly_chart(feauture_vs_price(data_after_removing_outlier, 'per_month_emi'), use_container_width=True)

        st.subheader('How categorical variable distributied after removing outliers ?')
        category_distribution = st.selectbox('select category',['housetype','house_condition','BHK'])

        if category_distribution=='housetype':
            fig = px.bar(x=data_after_removing_outlier.housetype, color_discrete_sequence=['brown', 'yellow'], template='simple_white',
                         color=data_after_removing_outlier.housetype)
            fig.update_traces(marker_line_width=0,
                              selector=dict(type="bar"))

            fig.update_layout(xaxis_title=' House Type')
            st.plotly_chart(fig, use_container_width=True)


        elif category_distribution == 'house_condition':
            fig = px.bar(x=data_after_removing_outlier.house_condition, color_discrete_sequence=['indigo', 'green'], template='simple_white',
                         color=data_after_removing_outlier.house_condition)
            fig.update_traces(marker_line_width=0,
                              selector=dict(type="bar"))

            fig.update_layout(xaxis_title=' House condition')
            st.plotly_chart(fig, use_container_width=True)

        elif category_distribution == 'BHK':
            BHK_count = data_after_removing_outlier.groupby('BHK')['BHK'].count()
            df1 = pd.DataFrame(data=BHK_count.index, columns=['BHK'])
            df2 = pd.DataFrame(data=BHK_count.values, columns=['count'])
            BHK_data = pd.merge(df1, df2, left_index=True, right_index=True)

            fig = px.bar(data_frame=BHK_data,x='BHK',y='count',color_discrete_sequence=['indigo'], template='simple_white')
            fig.update_traces(marker_line_width=0,
                              selector=dict(type="bar"))

            st.plotly_chart(fig, use_container_width=True)

    except  Exception as e:
        st.write(e)
        pass

