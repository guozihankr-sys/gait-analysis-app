import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="步态分析系统", layout="wide")

# =========================
# 标题区（更像项目）
# =========================
st.title("🚶 智能步态分析系统")
st.markdown("### 数字医疗与运动康复数据分析工具")
st.markdown("---")

# =========================
# 📂 数据加载（支持上传）
# =========================
st.sidebar.header("📂 数据输入")

uploaded_file = st.sidebar.file_uploader("上传CSV文件", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("已加载上传数据")
else:
    DATA_PATH = "gait_joint_angles.csv"
    if not os.path.exists(DATA_PATH):
        st.error("❌ 默认数据缺失，请上传CSV")
        st.stop()
    df = pd.read_csv(DATA_PATH)
    st.sidebar.info("使用默认数据")

# =========================
# 数据检查
# =========================
required_col = "gait_cycle_pct"

if required_col not in df.columns:
    st.error("❌ 数据缺少 gait_cycle_pct 列")
    st.stop()

# =========================
# 参数选择
# =========================
st.sidebar.header("⚙️ 分析设置")

feature_cols = [col for col in df.columns if col != "gait_cycle_pct"]

selected_cols = st.sidebar.multiselect(
    "选择分析关节（可多选）",
    feature_cols,
    default=[feature_cols[0]]
)

# =========================
# 核心指标（多列）
# =========================
st.subheader("📊 核心指标")

for col in selected_cols:
    max_val = df[col].max()
    min_val = df[col].min()
    mean_val = df[col].mean()

    c1, c2, c3 = st.columns(3)
    c1.metric(f"{col} 最大值", f"{max_val:.2f}")
    c2.metric(f"{col} 最小值", f"{min_val:.2f}")
    c3.metric(f"{col} 平均值", f"{mean_val:.2f}")

    st.markdown("---")

# =========================
# 数据预览
# =========================
with st.expander("📄 查看数据"):
    st.dataframe(df)

# =========================
# 📈 步态曲线（多条）
# =========================
st.subheader("📈 步态曲线对比")

fig, ax = plt.subplots()

for col in selected_cols:
    ax.plot(df["gait_cycle_pct"], df[col], label=col)

ax.set_xlabel("Gait Cycle (%)")
ax.set_ylabel("Angle (deg)")
ax.set_title("Gait Curve Comparison")
ax.legend()

st.pyplot(fig)

# =========================
# ⚡ 快速交互图
# =========================
st.subheader("⚡ 快速趋势图")

st.line_chart(df.set_index("gait_cycle_pct")[selected_cols])

# =========================
# 🧠 智能分析（升级版）
# =========================
st.subheader("🧠 智能分析报告")

for col in selected_cols:
    max_val = df[col].max()
    min_val = df[col].min()
    mean_val = df[col].mean()
    range_val = max_val - min_val

    st.markdown(f"### 🔍 {col}")

    if range_val < 30:
        st.warning("活动范围较小，可能存在关节活动受限")
    elif range_val > 100:
        st.warning("活动范围过大，可能存在不稳定风险")
    else:
        st.success("活动范围处于正常区间")

    if abs(mean_val) < 1:
        st.info("运动整体较为对称和平衡")
    else:
        st.info("存在一定偏移，建议进一步评估")

# =========================
# 🎯 项目说明（给老师看的）
# =========================
st.markdown("---")
st.subheader("📌 项目说明")

st.markdown("""
本系统用于对步态周期中的关节角度数据进行可视化与分析，支持：

- 多关节角度对比分析
- 动态数据上传
- 自动计算关键统计指标
- 基于规则的初步医学解释

适用于运动科学、康复医学及生物力学分析场景。
""")
