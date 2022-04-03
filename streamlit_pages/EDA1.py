import streamlit as st
import pandas as pd
import seaborn as sns
import get_data
import matplotlib.pyplot as plt
import plotly.express as px


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
        st.sidebar.subheader('What  is  EDA     (exploratory data analysis) ?')
        with st.sidebar.expander('see explanation'):
            st.write("Exploratory Data Analysis refers to the critical "
                     "process of performing initial investigations on data so as to discover"
                     " patterns,to spot anomalies,to test hypothesis and to check assumptions"
                     " with the help of summary statistics and graphical representations.")
            st.write('                  ')

            st.write( "It is a good practice to understand the data first and try to gather as many insights from it. "
                      "EDA is all about making sense of data in hand,before getting them dirty with it")

        house = get_data.get_data(path='../read_data/raw_data.csv')
        st.subheader('How our dataset looks ?')
        st.dataframe(house)
        downnload_button(house, 'nashik.csv')

        st.subheader('which are the columns with missing values?')
        col1, col2 = st.columns([2, 3])
        with col1:
            st.write(house.isnull().sum())
        with col2:
            plt.figure(figsize=(10, 6))
            st.pyplot(sns.displot(
                data=house.isna().melt(value_name="missing"),
                 y="variable",
                hue="missing",
                multiple="fill",
                aspect=1.25
            ))

        st.subheader('Outlier Detection 🔍')
        nashik = house.copy()
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('boxplot of price')

            with st.expander("See observation on price"):
                st.write("""<p style="background-color:powderblue;">
                        There are only 65 values above 2cr rupee, these are expensive properties 
                          we can treat this values as an outlier</p>
                    """,unsafe_allow_html=True)
            st.plotly_chart(px.box(data_frame=nashik, y=nashik.price, width=300, color_discrete_sequence=['grey'], orientation='v',hover_data=['owners', 'house_condition', 'BHK', 'price', 'per_month_emi', 'total_sqft']))


        with col2:
            st.markdown('boxplot of per_month_emi')

            with st.expander("observation per_month_emi"):
                st.write("""<p style="background-color:powderblue;">
                    There are only 3 values of above 1cr rupee for expensive propertise emi are very high
                    ,we can treat this as an outlier</p>
                """,unsafe_allow_html=True)

            st.plotly_chart(px.box(data_frame=nashik,y=nashik.per_month_emi, width=300,hover_data=['owners', 'house_condition', 'BHK', 'price', 'per_month_emi', 'total_sqft']
                                       , color_discrete_sequence=['grey'], orientation='v'))
        with col3:
            st.markdown('boxplot of total_sqft')

            with st.expander("See observation on total_sqft"):
                st.write("""<p style="background-color:powderblue;">
                         There are only 5 value above 5000 sqare foot so we can treat this value as outlier and use value below 5000 sqft</p>
                    """,unsafe_allow_html=True)
            st.plotly_chart(px.box(data_frame=nashik,y= nashik.total_sqft ,width = 300,hover_data=['owners', 'house_condition', 'BHK', 'price', 'per_month_emi', 'total_sqft']
               ,color_discrete_sequence=['grey'],orientation='v'))

        df= get_data.get_data('../feature_enginerring/data_after_removing_null')
        st.subheader('How categorical variable distributed ?')
        category_distribution = st.selectbox('select category',['housetype','house_condition','BHK','housetype and housecondition'])

        if category_distribution=='housetype':
            fig = px.bar(x=df.housetype, color_discrete_sequence=['brown', 'yellow'], template='simple_white',
                         color=df.housetype)
            fig.update_traces(marker_line_width=0,
                              selector=dict(type="bar"))

            fig.update_layout(xaxis_title=' House Type')
            st.plotly_chart(fig, use_container_width=True)


        elif category_distribution == 'house_condition':
            fig = px.bar(x=df.house_condition, color_discrete_sequence=['indigo', 'green'], template='simple_white',
                         color=df.house_condition)
            fig.update_traces(marker_line_width=0,
                              selector=dict(type="bar"))

            fig.update_layout(xaxis_title=' House condition')
            st.plotly_chart(fig, use_container_width=True)

        elif category_distribution == 'BHK':
            BHK_count = df.groupby('BHK')['BHK'].count()
            df1 = pd.DataFrame(data=BHK_count.index, columns=['BHK'])
            df2 = pd.DataFrame(data=BHK_count.values, columns=['count'])
            BHK_data = pd.merge(df1, df2, left_index=True, right_index=True)

            fig = px.bar(data_frame=BHK_data,x='BHK',y='count',color_discrete_sequence=['indigo'], template='simple_white')
            fig.update_traces(marker_line_width=0,
                              selector=dict(type="bar"))

            st.plotly_chart(fig, use_container_width=True)

        elif category_distribution=='housetype and housecondition':
            fig = px.bar(x=df.housetype, color_discrete_sequence=['brown', 'yellow'], template='simple_white',
                         color=df.house_condition)
            fig.update_traces(marker_line_width=0,
                              selector=dict(type="bar"))

            fig.update_layout(xaxis_title=' House Type')
            st.plotly_chart(fig, use_container_width=True)

        st.subheader('How dataset distributed for continuous variable?')
        data_distribution = st.selectbox('select feature', ['price', 'per_month_emi', 'total_sqft'])

        if data_distribution == 'price':
            with st.expander('see observation'):
                st.text('''
             1) most of the values lies between 21 lakhs to 47 lakshs 
             2)32 lakhs is median and we can use this value to fill na values in price column
             3) there are some properties which are really costly above 1 cr 
        
            ''')
            fig1 = px.histogram(data_frame=nashik[nashik.price < 200.0], x=nashik.price[nashik.price < 200.0],
                                color_discrete_sequence=['grey'], template='gridon',
                                marginal="box",
                                hover_data=['owners', 'house_condition', 'BHK', 'price', 'housetype', 'total_sqft'])
            fig1.update_layout(xaxis_title="Price in lakhs")
            st.plotly_chart(fig1, use_container_width=True)

        # 2) above 50 thsouand per month emi is really big amount this are an outlier we need to deal with it latter')


        if data_distribution == 'total_sqft':
            with st.expander('see observation'):
                st.write('''<p style="background-color:powderblue;">
            1) most of the values lies between 734 sqft and 1290 sqft 
        2)971 is median value ,we can fill missing value in total_sqft with this value
        3) There are so many outliers after 2150 sq_ft or
         we can say some independent houses in our data has really huge sq_ft area</p>
            ''',unsafe_allow_html=True)
            fig1 = px.histogram(data_frame=nashik[nashik.total_sqft < 5000.0], x=nashik.total_sqft[nashik.total_sqft < 5000.0],
                                color_discrete_sequence=['grey'], marginal='box', template='gridon',
                                hover_data=['owners', 'house_condition', 'BHK', 'price', 'housetype', 'total_sqft'])
            fig1.update_layout(xaxis_title='total square foot of house')
            st.plotly_chart(fig1, use_container_width=True)



        if data_distribution == 'per_month_emi':
            with st.expander('see observation'):
                st.text('''
                         1) most of the values lies between 11 thousand rs to  26 thousand rs
                2)18 thusand rs is median we can use this  value to fill missing value
                3)above 50 thsouand per month emi is really big amount this are an outlier
                 we need to deal with it latter
                ''')

            fig1 = px.histogram(data_frame=nashik[nashik.per_month_emi < 100.0],x=nashik.per_month_emi[nashik.per_month_emi < 100.0], color_discrete_sequence=['grey'],template='gridon'
                ,marginal='box',hover_data=['owners', 'house_condition', 'BHK', 'price', 'housetype', 'total_sqft'])
            fig1.update_layout(xaxis_title= 'per month emi in thousand')
            st.plotly_chart(fig1,use_container_width=True)

        st.text('(note : I had ignored extreme outliers while plotting above graph)')

    except Exception as e:
        st.write(e)
        pass


#if data_distribution == 'total_sqft':

#if data_distribution == 'per_month_emi'

