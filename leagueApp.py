import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_csv('41binMatches.csv')

st.title('League App')

col1, col2, col3 = st.columns(3)
with col1:
    myChamp = st.text_input('My Champion')

with col2:
    partnerChamp = st.text_input('Partner Champion')


myChamp = myChamp.title()
partnerChamp = partnerChamp.title()


if myChamp != "":
    df = df[df.ChampionID == myChamp & df.PartnerChampionID == partnerChamp]


myChampWins = 0
partnerChampWins = 0

# for row in df:


# st.metric("Winrate On Champion", , delta=None, delta_color="normal")

st.dataframe(df)
