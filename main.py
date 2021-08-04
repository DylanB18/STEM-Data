import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from functions import calcFreeLunch, loadSTEMData, loadDOEData, loadGraphData, TitleOne, Magnet, AllSchools

# Title
st.title('Broward STEM Data')
st.text("All students in BCPS taking STEM Classes 2014-2021")

# Load Data
data_load_state = st.text('Loading data...')
data = loadSTEMData()
DOE_data = loadDOEData()
graph_data = loadGraphData(data, DOE_data)
data_load_state.text('Loading data...done!')

graph_data

# Show Raw Data
st.subheader('Raw Data')
if(st.checkbox("Show Data")):
	st.write(data)

#Group to browse sex data by school
sex_data = data.groupby(["School"])["Sex"].value_counts()

st.subheader('School and Gender Breakdown')
if(st.checkbox("Show Breakdown")):
	sex_data


st.subheader("School Search")
selected_school = st.selectbox("Select School", data["School"].unique())
selected_row = DOE_data[DOE_data['School Name'].str.contains(selected_school)]

selected_row = selected_row.to_numpy()

st.text("Magnet: " + selected_row[0][2])
st.text("Title I: " + selected_row[0][3] + " (School Wide)")
st.text("White: " + str(round((selected_row[0][8] / selected_row[0][4])* 100, 2)) + "%")
st.text("Hispanic: " + str(round((selected_row[0][6] / selected_row[0][4])* 100, 2)) + "%")
st.text("Black: " + str(round((selected_row[0][7] / selected_row[0][4])* 100, 2)) + "%")
st.text("Free Lunch Eligible: " + str(round((selected_row[0][5] / selected_row[0][4])* 100, 2)) + "%")

#Sex Data Extraction

#TODO: FIX ATLANTIC TECH SEX RATIO BY USING graph data

sex_data_arr = np.array(sex_data)

index = DOE_data[DOE_data["School Name"] == selected_school].index.values

male = sex_data_arr[index*2][0]
female = sex_data_arr[index*2 + 1][0]

st.text("Males per Female Student: " + str(round(male/female, 2)))


st.subheader("Graphs")
st.text("Free Lunch vs. sRatio")
lunchSexGraph = alt.Chart(graph_data).mark_circle().encode(
	x='% Free Lunch',
	y='sRatio',
	tooltip=['School Name', '% Free Lunch', 'sRatio'])

lunchSexGraph + lunchSexGraph.transform_regression('% Free Lunch', 'sRatio', method="poly").mark_line()

st.text("% Black vs. sRatio")
raceSexGraph = alt.Chart(graph_data).mark_circle().encode(
	x='% Black',
	y='sRatio',
	tooltip=['School Name', '% Black', 'sRatio'])

raceSexGraph + raceSexGraph.transform_regression('% Black', 'sRatio', method="poly").mark_line()

st.subheader("Correlations")
correlations = graph_data.corr(method="pearson")
correlations

st.subheader("School Type Analysis")
st.text(TitleOne(graph_data))
st.text(Magnet(graph_data))
st.text(AllSchools(graph_data))
