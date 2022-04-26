from re import M
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("41binMatches.csv")
df.drop(df.iloc[:, :2], inplace=True, axis=1)
meDict = {}
partnerDict = {}

pairings = {}

for index, row in df.iterrows():
    me = row["ChampionID"]
    partner = row["PartnerChampionID"]

    if pairings.get(f"{me}{partner}") == None:
        pairings[f"{me}{partner}"] = [row["Win/Lost"]]
    else:
        pairings[f"{me}{partner}"][0] += row["Win/Lost"]

    if meDict.get(me) == None:
        meDict[me] = row["Win/Lost"]
    else:
        meDict[me] += row["Win/Lost"]

    if partnerDict.get(partner) == None:
        partnerDict[partner] = row["Win/Lost"]
    else:
        partnerDict[partner] += row["Win/Lost"]


st.title("League App")

# f"""
# ### League Stats for 41619 and Yongbin
# """

col1, col2 = st.columns(2)
with col1:
    myChamp = st.text_input("My Champion")

with col2:
    partnerChamp = st.text_input("Partner Champion")


myChamp = myChamp.title()
partnerChamp = partnerChamp.title()


if myChamp != "" and partnerChamp == "":
    df = df[df.ChampionID == myChamp]
elif myChamp == "" and partnerChamp != "":
    df = df[df.PartnerChampionID == partnerChamp]
elif myChamp != "" and partnerChamp != "":
    df = df[(df.ChampionID == myChamp) & (
        df.PartnerChampionID == partnerChamp)]


w = 0
myKDA = 0
themKDA = 0

myVS = 0
themVS = 0

for index, row in df.iterrows():
    if row["Win/Lost"]:
        w += 1

    myKDA += row["KDA"]
    themKDA += row["PartnerKDA"]

    myVS += row["VisionScore"]
    themVS += row["PartnerVisionScore"]


myKDA, themKDA = round(myKDA / df.shape[0], 2), round(themKDA / df.shape[0], 2)
myVS, themVS = round(myVS / df.shape[0], 2), round(themVS / df.shape[0], 2)


wr = round(w / df.shape[0], 4) * 100


newCol1, newCol2, newCol3, newCol4, newCol5 = st.columns(5)
with newCol1:
    st.metric("Winrate", f"{wr}%", delta=None, delta_color="normal")

with newCol2:
    st.metric("My KDA", f"{myKDA}", delta=None, delta_color="normal")
    st.metric("Their KDA", f"{themKDA}", delta=None, delta_color="normal")

with newCol3:
    st.metric("My VS", f"{myVS}", delta=None, delta_color="normal")
    st.metric("Their VS", f"{themVS}", delta=None, delta_color="normal")


with newCol5:
    st.metric("41619 Top Champ", f"{max(meDict, key = meDict.get)}")
    st.metric(
        "Yongbin Top Champ",
        f"{max(partnerDict, key = partnerDict.get)}",
    )
st.dataframe(df)
