import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("步态分析系统")

# ✅ 改这里：用你已有的文件
df = pd.read_csv("gait_joint_angles.csv")

st.write("数据预览：")
st.write(df.head())

# 简单画图（前两列）
fig, ax = plt.subplots()
ax.plot(df.iloc[:, 0], df.iloc[:, 1])
st.pyplot(fig)
