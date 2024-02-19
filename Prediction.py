import streamlit as st
from datetime import date,timedelta,datetime,time
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import yfinance
import numpy as np
from tensorflow.keras.saving import load_model
from streamlit_option_menu import option_menu
st.set_page_config(layout="wide",initial_sidebar_state='collapsed',page_icon='📉')
st.title('**Time Series Forcasting**')
selected = option_menu(menu_title=None,options= ["Prediction", 'Previous Data'],orientation='horizontal',
                       icons=['None', 'None'], default_index=0,
                       styles={
        "container": {"padding": "0!important", "background-color": "grey"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#35383d"},
    }
)
model = load_model('AAPLE_LSTM.h5')
df2=yfinance.download('AAPL', start='2024-02-16',
                     end=date.today()+timedelta(days=1),
                     interval='1m')
x_input = df2['Open']
x_input = np.array(x_input)
temp_input = list(x_input)
lst_output = []
i = 0
n_steps = 50
n_features=1


if selected=='Prediction':
    st.subheader('**Forecast**')
    if  'startdate' not in st.session_state:
        st.session_state.startdate  = None
    if  'enddate' not in st.session_state:
        st.session_state.enddate  = None
    startdate = st.date_input("**Start Date**",min_value=date.today())
    enddate = st.date_input("**End Date**",min_value=startdate,max_value=startdate+timedelta(days=370),value= None)
    if startdate and enddate:
        st.session_state.startdate  = startdate
        st.session_state.enddate  = enddate
        indexrange = []
        current_date = st.session_state.startdate
        while current_date <= st.session_state.enddate:
            indexrange += pd.date_range(start=datetime.combine(current_date, time(9, 15)),
                                        end=datetime.combine(current_date, time(15, 29)),
                                        freq='T').tolist()
            current_date += timedelta(days=1)
        if st.button('**Start Prediction**'):
            while i < 40:
                print('----------------------------------------------------------------')
                if len(temp_input) >= n_steps:  # Ensure length is sufficient for reshaping
                    x_input = np.array(temp_input[-n_steps:])  # Take the last n_steps elements
                    print("{} day input {}".format(i, x_input))
                    x_input = x_input.reshape((1, n_steps, n_features))
                    yhat = model.predict(x_input, verbose=0)
                    print("{} day output {}".format(i, yhat))
                    temp_input.append(yhat[0][0])
                    lst_output.append(yhat[0][0])
                    i = i + 1
                else:
                    x_input = x_input.reshape((1, n_steps, n_features))
                    yhat = model.predict(x_input, verbose=0)
                    print(yhat[0])
                    temp_input.append(yhat[0][0])
                    lst_output.append(yhat[0][0])
                    i=i+1
            st.subheader('**Predicted Values**',divider=True)
            df = pd.DataFrame(lst_output,index=indexrange[:40],columns=['Open'])
            st.dataframe(data=df,width=700)
            st.subheader("Prediction chart",divider=True)
            plt.figure(figsize=(21,11))
            line=px.line(data_frame=df,x=df.index,y=df.columns,title="Apple Stock Prices")
            line.show()
            st.plotly_chart(line)


if selected=='Previous Data':
    if 'previous_dataframe' not in st.session_state:
        st.session_state.previous_dataframe=None
    previous_dataframe=yfinance.download('AAPL', start=(date.today()-timedelta(days=6)).strftime('%Y-%m-%d'),
                        end=date.today()+timedelta(days=1),
                        interval='1m')
    st.session_state.previous_dataframe=previous_dataframe
    dataframe = st.dataframe(st.session_state.previous_dataframe,width=700)
    if dataframe:
        chkBox = st.checkbox('Click here to see graph')
        if chkBox==True:
            line2 = px.line(data_frame=previous_dataframe,x=previous_dataframe.index,y=previous_dataframe['Open'],title="Previous 7 days")
            line2.show()
            st.plotly_chart(line2)
            
