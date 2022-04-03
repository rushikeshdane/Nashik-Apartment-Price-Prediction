import streamlit as st
import  get_data
import train_test_split
import find_best_model
try:
    def remove_per_month_emi(data):

        new_data = data.drop(['per_month_emi'], axis=1)
        return new_data

    data_after_removing_unnecessary_column = df = get_data.get_data(path='../feature_selection/data_after_removing_unnecessary_column')
    object_of_train_test_split = train_test_split.split(data_after_removing_unnecessary_column)

    x_train = object_of_train_test_split.X_train()
    y_train = object_of_train_test_split.y_train()
    x_test = object_of_train_test_split.X_test()
    y_test = object_of_train_test_split.y_test()

    new_x_train = remove_per_month_emi(x_train)
    new_x_test = remove_per_month_emi(x_test)

    object_of_best_model= find_best_model.find_best_ml_model(new_x_train,y_train,new_x_test,y_test)

except Exception as e:
    st.write(e)
    pass

def app():
    try:

        st.subheader('Selecting best model by doing model comparison')


        checkbox = st.checkbox('see model comparison')
        @st.cache
        def show_model():
            return object_of_best_model.model_comparision()


        if checkbox :
            st.text('wait for 15 seconds')
            st.write(show_model())

        with st.expander('see observations'):
            st.markdown('gradient boosting regressor and LGBM regressor showing maximum score and minimum root mean squared'
                        ' value ,we can select  any model out of this two . I had selected light gradient boosting framework(LGBM)'
                        '  most of the top performing machine learning model are tree based model and using some sort of boosting techniques ')

        st.header('Hyperparameter tuning')
        st.sidebar.subheader('What is hyperparameter tuning ?')
        with st.sidebar.expander('see explnation'):

            st.write('Hyperparameter tuning is choosing a set of optimal hyperparameters for a learning algorithm.'
                     ' A hyperparameter is a model argument whose value is set before the learning process begins.')

        col1, col2 = st.columns(2)

        with col1:
            st.subheader('Grid search')
            with st.expander('What is grid search cv?'):
                st.write('Grid search is the simplest algorithm for hyperparameter tuning. Basically, we divide the domain'' of the hyperparameters into a discrete grid. Then, we try every combination of values of this'
                         ' grid, calculating some performance metrics using cross-validation. The point of the grid that '
                         'maximizes the average value in cross-validation, is the optimal combination of values for the '
                         'hyperparameters.')

            with st.expander('Best parameter after applying grid search'):
                st.markdown("Best parameters: {'boosting_type': 'dart', 'importance_type ': 'split', 'learning_rate': 0.1, 'n_estimators': 500, 'num_leaves': 10, 'subsample_for_bin ': 100000}")

            with st.expander("RMSE (root mean squared error)"):
                st.write('Lowest RMSE:  8.267841017788236')


        with col2:
            st.subheader('Random search')
            with st.expander('What is random search cv?'):
                st.write('Random search is similar to grid search, but instead of using all the points in the grid, it tests '
                         'only a randomly selected subset of these points. The smaller this subset, the faster but less'
                         ' accurate the optimization. The larger this dataset, the more accurate the optimization but the'
                         ' closer to a grid search.')

            with st.expander('Best parameter after applying random search'):
                st.markdown("Best parameters: {'subsample_for_bin ': 400000, 'num_leaves': 100, 'n_estimators': 300, 'learning_rate': 0.1, 'importance_type ': 'gain', 'boosting_type': 'dart'}")

            with st.expander("RMSE  (root mean squared error)"):
                st.write('Lowest RMSE:  8.480144377661615')
    except  Exception as e:
        st.write(e)
        pass