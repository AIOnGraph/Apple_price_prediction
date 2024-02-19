import streamlit as st
from datetime import date,timedelta,datetime,time
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import yfinance
import numpy as np
from tensorflow.keras.saving import load_model
st.set_page_config(layout="wide",initial_sidebar_state='collapsed',page_icon='📉')
st.title('**Time Series Forcasting**')
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

prediction_date=st.subheader('**Enter the prediction date in sidebar**',divider=True)
with st.sidebar:
    startdate = st.date_input("**Start Date**",min_value=date.today())
    enddate = st.date_input("**End Date**",min_value=startdate,max_value=startdate+timedelta(days=370),value= None)
    
if startdate and enddate:
    prediction_date.empty()
    indexrange = []
    current_date = startdate
    while current_date <= enddate:
        indexrange += pd.date_range(start=datetime.combine(current_date, time(9, 15)),
                                    end=datetime.combine(current_date, time(15, 29)),
                                    freq='T').tolist()
        current_date += timedelta(days=1)
    if st.sidebar.button('**Start Prediction**'):
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