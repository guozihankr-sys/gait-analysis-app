import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 页面设置
st.set_page_config(page_title="步态分析系统", layout="wide")

# 标题
st.title("步态分析系统")
st.markdown("基于关节角度数据的步态可视化分析")

# 读取数据
@st.cache_data
def load_data():
    return pd.read_csv("gait_joint_angles.csv")

df = load_data()

# ======================
# 侧边栏
# ======================
st.sidebar.header("参数选择")

columns = [col for col in df.columns if col != "gait_cycle_pct"]
selected_col = st.sidebar.selectbox("选择分析关节", columns)

# ======================
# 核心指标
# ======================
st.subheader("📊 核心指标")

col1, col2, col3 = st.columns(3)

max_val = df[selected_col].max()
min_val = df[selected_col].min()
mean_val = df[selected_col].mean()

col1.metric("最大值", f"{max_val:.2f}")
col2.metric("最小值", f"{min_val:.2f}")
col3.metric("平均值", f"{mean_val:.2f}")

# ======================
# 数据预览
# ======================
with st.expander("📋 查看原始数据"):
    st.dataframe(df)

# ======================
# 步态曲线
# ======================
st.subheader("📈 步态曲线")

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(df["gait_cycle_pct"], df[selected_col])
ax.set_xlabel("Gait Cycle (%)")
ax.set_ylabel(selected_col)
ax.set_title(f"{selected_col} Curve")
ax.grid(True)

st.pyplot(fig)

# ======================
# 快速图（去掉标题更简洁）
# ======================
st.subheader("⚡ 快速图")

fig2, ax2 = plt.subplots()
ax2.plot(df[selected_col])
ax2.grid(True)

st.pyplot(fig2)

# ======================
# 简单分析
# ======================
st.subheader("🧠 简单分析")

range_val = max_val - min_val

if range_val < 30:
    st.warning("关节活动幅度偏低，可能存在活动受限")
elif range_val > 80:
    st.warning("关节活动幅度较大，可能存在异常")
else:
    st.success("关节活动范围正常")

# 平均值分析
if abs(mean_val) < 1:
    st.info("整体运动较为对称")
