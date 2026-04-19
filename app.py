import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Gait Analysis System")

# 读取数据（注意路径！！！）
df = pd.read_csv("03_normal_gait_data.csv")

st.write("数据预览：")
st.write(df.head())

# 画图
fig, ax = plt.subplots()
ax.plot(df.iloc[:,0], df.iloc[:,1])

st.pyplot(fig)
