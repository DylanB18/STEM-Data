import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Config
stem_source = 'prod_data.csv'
DOE_source = 'DOE.csv'

#Math Functions
def calcFreeLunch(row):
	fLunch = row['Free Lunch Eligible'] / row['Total Students']
	return fLunch * 100

def calcPercentBlack(row):
	pBlack = row['Black Students'] / row['Total Students']
	return pBlack * 100

def calcSexRatio(row, data):
	males = ((data['School'] == row['School Name']) & (data['Sex'] == "M")).sum()
	females = ((data['School'] == row['School Name']) & (data['Sex'] == "F")).sum()

	sRatio = round(males/females, 1)

	return sRatio

#Return Number of Title I Schools
def countTitleOne(g_data):
	return len(g_data.loc[g_data['School-wide Title I'] == "Yes"].index)

#Calculate the sRatio average for Title I schools
def calcTitleOneRatio(g_data):
	TitleOneSchools = g_data.loc[g_data['School-wide Title I'] == "Yes"]
	mean = TitleOneSchools['sRatio'].mean()
	return mean


def TitleOne(g_data):
	return "The " + str(countTitleOne(g_data)) + " Title I schools have a mean sexRatio of " + str(round(calcTitleOneRatio(g_data), 2))

#Return Number of Title I Schools
def countMagnet(g_data):
	return len(g_data.loc[g_data['Magnet School'] == "Yes"].index)

#Calculate the sRatio average for Title I schools
def calcMagnetRatio(g_data):
	TitleOneSchools = g_data.loc[g_data['Magnet School'] == "Yes"]
	mean = TitleOneSchools['sRatio'].mean()
	return mean


def Magnet(g_data):
	return "The " + str(countMagnet(g_data)) + " magnet schools have a mean sexRatio of " + str(round(calcMagnetRatio(g_data), 2))

def AllSchools(g_data):
	return "All schools have a mean sexRatio of " + str(round(g_data['sRatio'].mean(), 2))

#Loading Functions
@st.cache
def loadSTEMData():
	data = pd.read_csv(stem_source)
	return data

@st.cache
def loadDOEData():
	data = pd.read_csv(DOE_source)
	return data

@st.cache
def loadGraphData(main, DOE):
	#Start with DOE data
	g_data = DOE.copy()

	#Calculate percents
	g_data['% Free Lunch'] = g_data.apply(lambda row: calcFreeLunch(row), axis=1)
	g_data['% Black'] = g_data.apply(lambda row: calcPercentBlack(row), axis=1)

	#Calculate Sex Ratio
	g_data['sRatio'] = g_data.apply(lambda row: calcSexRatio(row, main), axis=1)

	sexTotal = main.groupby(["School"])["Sex"].count().reset_index()

	#Discard unneeded data for organization purposes
	g_data.drop('Total Students', axis=1, inplace=True)
	g_data.drop('Free Lunch Eligible', axis=1, inplace=True)
	g_data.drop('Hispanic Students', axis=1, inplace=True)
	g_data.drop('Black Students', axis=1, inplace=True)
	g_data.drop('White Students', axis=1, inplace=True)
	g_data.drop('Two or More Races Students', axis=1, inplace=True)

	return g_data
