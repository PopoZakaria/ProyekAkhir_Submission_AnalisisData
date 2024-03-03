import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import traceback


#menyiapkan helper function untuk dataframe
def create_area_df(df):
    area_df = df.groupby("column_station").index_aqi.sum().sort_values(ascending=False).reset_index()
    return area_df

def create_Viklim_mean_df(df):
    Viklim_mean_df= df.groupby(by="quality_air").agg({
        "column_TEMP": ['mean'],
        "column_PRES" : ['mean'],
        "column_DEWP" : ['mean'],
        "column_WSPM" : ['mean']
    })
    Viklim_mean_df = Viklim_mean_df.T
    return Viklim_mean_df

def create_quality_mean_df(df):
    quality_mean_df = df.groupby(by="quality_air").agg({
        "column_SO2" : ['mean'],
        "column_NO2" : ['mean'],
        "column_CO" : ['mean'],
        "column_O3" : ['mean']
    })
    quality_mean_df = quality_mean_df.T
    return quality_mean_df

def create_df_time(df):
    df_time= df
    return df_time

#menyiapkan dataset
df_aqi=pd.read_csv("./dashboard/df_AQI.csv")
df_aqi.sort_values(by="column_datetime")
df_aqi.reset_index(inplace=True)
df_aqi["column_datetime"]=pd.to_datetime(df_aqi["column_datetime"])

#filter data
min_date = df_aqi["column_datetime"].min()
max_date = df_aqi["column_datetime"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("./dashboard/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date = st.date_input("Start date", min_date)
    end_date = st.date_input("End date", max_date)
    

main_df = df_aqi[(df_aqi["column_datetime"] >= str(start_date)) & 
                (df_aqi["column_datetime"] <= str(end_date))]

area_df = create_area_df(main_df)
Viklim_mean_df = create_Viklim_mean_df(main_df)
time_df = create_df_time(main_df)

quality_mean_df = create_quality_mean_df(main_df)


#membuat header dashboard
st.header('Air Quality Index dashboard :lightning:')

st.subheader("Best & Worst Air Quality Index (aqi)")
#membuat subplot grid
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

#membuat template color untuk visualisasi
colors1 = ["#00FF00" , "#D3D3D9", "#D3D3D9", "#D3D3D9", "#D3D3D9"]
colors2 = ["#1E90FF" , "#D3D3D9", "#D3D3D9", "#D3D3D9", "#D3D3D9"]

#membuat barplot dengan inisialisasi ax[0]
sns.barplot(x="index_aqi", y="column_station", data=area_df.head(5), palette=colors1, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Air Quality Index (aqi)", loc="center", fontsize=30)
ax[0].tick_params(axis ='y', labelsize=20)
ax[0].tick_params(axis ='x', labelsize=20)

#membuat barplot dengan inisialisasi ax[1]
sns.barplot(x="index_aqi", y="column_station", data=area_df.sort_values(by="index_aqi", ascending=True).head(5), palette=colors2, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Air Quality Index (aqi)", loc="center", fontsize=30)
ax[1].tick_params(axis='y', labelsize=20)
ax[1].tick_params(axis ='x', labelsize=20)

st.pyplot(fig)

st.subheader("Average variable SO2, NO2, CO, & O3")

col1, col2, col3, col4 = st.columns(4)

with col1:
    mean_so2 = round(quality_mean_df.T.column_SO2.mean(), 2)
    st.metric("average SO2", value=float(mean_so2))
with col2:
    mean_no2 = round(quality_mean_df.T.column_NO2.mean(), 2)
    st.metric("average NO2", value=float(mean_no2))
with col3:
    mean_co = round(quality_mean_df.T.column_CO.mean(), 2)
    st.metric("average CO", value=float(mean_co))
with col4:
    mean_o3 = round(quality_mean_df.T.column_O3.mean(), 2)
    st.metric("average O3", value=float(mean_o3))

species = ("SO2", "NO2", "CO", "O3")

#mengatur posisi, lebar, & jarak setiap bar
x = np.arange(len(species))
width = 0.25
multiplier = 1

fig, ax = plt.subplots(figsize=(12, 9)) #membuat subplot grid

#looping untuk mengisi subplot grid dengan plots
for attribute, measurement in quality_mean_df.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=4, rotation=60)
    multiplier += 1

# Menambah text, title,& label
ax.set_ylabel('Mean')
ax.set_title('Pengaruh SO2, NO2, CO, & O3')
ax.set_xticks(x + width)
ax.set_xticklabels(species)
ax.set_ylim(-2, 3000)
ax.legend(loc='upper right')

st.pyplot(fig)

st.subheader("Average variable temperature, pressure, dew point, & wind speed")

col1, col2, col3, col4= st.columns(4)

with col1:
    mean_temp = round(Viklim_mean_df.T.column_TEMP.mean(), 2)
    st.metric("average TEMP", value=float(mean_temp))

with col2:
    mean_pres = round(Viklim_mean_df.T.column_PRES.mean(), 2)
    st.metric("average PRES", value=float(mean_pres))

with col3:
    mean_dewp = round(Viklim_mean_df.T.column_DEWP.mean(), 2)
    st.metric("average DEWP", value=float(mean_dewp))

with col4:
    mean_wspm = round(Viklim_mean_df.T.column_WSPM.mean(), 2)
    st.metric("average WSPM", value=float(mean_wspm))

species = ("TEMP", "PRES", "DEWP", "WSPM") 

#mengatur posisi, lebar, & jarak setiap bar
x = np.arange(len(species))
width = 0.25
multiplier = 1

fig, ax = plt.subplots(figsize=(12, 9)) #membuat subplot grid

#looping untuk mengisi subplot grid dengan plots
for attribute, measurement in Viklim_mean_df.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=4, rotation=30)
    multiplier += 1

# Menambah text, title,& label
ax.set_ylabel('Mean')
ax.set_title('Pengaruh TEMP, PRES, DEWP, & WSPM')
ax.set_xticks(x + width)
ax.set_xticklabels(species)
ax.set_ylim(-2, 1400)
ax.legend(loc='upper right')

st.pyplot(fig)

st.subheader("Air Quality Index by variable time")

col1, col2, col3, col4= st.columns(4)

with col1:
    mean_year = round(time_df.column_year.mean(), 2)
    st.metric("average year", value=float(mean_year))

with col2:
    mean_month = round(time_df.column_month.mean(), 2)
    st.metric("average month", value=float(mean_month))

with col3:
    mean_day = round(time_df.column_day.mean(), 2)
    st.metric("average day", value=float(mean_day))

with col4:
    mean_hour = round(time_df.column_hour.mean(), 2)
    st.metric("average hour", value=float(mean_hour))

cat_var=["column_year", "column_month", "column_day", "column_hour"] #membuat list untuk label attribute visualisasi

# Membuat subplot grid
fig, ax= plt.subplots(nrows= 2, ncols= int(len(cat_var)/2), figsize= (40,15))

# Looping untuk mengisi subplot grid dengan plots
k= 0
for i in range(2):
    for j in range(int(len(cat_var)/2)):
        sns.barplot(y= time_df.groupby(by= cat_var[k]).index_aqi.sum(),
                    x= time_df.groupby(by= cat_var[k]).mean(numeric_only=True).index, ax= ax[i,j], palette= 'winter')

        ax[i,j].set_title(f'{cat_var[k].upper()}', fontsize= 30)
        ax[i,j].set_ylabel('')
        ax[i,j].set_xlabel('')
        ax[i,j].tick_params(axis='y', labelsize=30)
        ax[i,j].tick_params(axis='x', labelsize=25)
        plt.xticks(rotation=315)
        k+=1

st.pyplot(fig)