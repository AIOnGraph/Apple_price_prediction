import streamlit as st
import yfinance
import pandas as pd
from datetime import date ,timedelta
import  plotly.express as px


st.title("**Previous 7 days data**")
st.divider()
previous_dataframe=yfinance.download('AAPL', start=(date.today()-timedelta(days=6)).strftime('%Y-%m-%d'),
                     end=date.today()+timedelta(days=1),
                     interval='1m')
st.dataframe(previous_dataframe,width=700)
line2 = px.line(data_frame=previous_dataframe,x=previous_dataframe.index,y=previous_dataframe['Open'],title="Previous 7 days")
line2.show()
st.plotly_chart(line2)