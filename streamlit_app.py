import streamlit as st
import pandas as pd

# 텍스트
st.title("📊 일일 식비 지출 분석 대시보드")
st.caption("10강 실습 과제: CSV 기반 식비 데이터 분석 및 예산 모니터링")

st.markdown("""
매일 업데이트되는 일일 식비 기록 CSV(`expenses.csv`)를 불러와 분석합니다.
조회 기간 및 목표 일일 예산을 조절하여 지출 흐름을 파악해요.
""")

# CSV 불러오기
@st.cache_data
def load_data():
    return pd.read_csv("expenses.csv")

df = load_data()


st.sidebar.header("⚙️ 분석 설정")

# 위젯 1: 최근 며칠 치를 볼 것인지 선택 
view_days = st.sidebar.slider(
    "조회할 최근 일수 선택", 
    min_value=3, 
    max_value=len(df), 
    value=len(df)
)

# 위젯 2: 하루 목표 식비 기준선 
daily_budget = st.sidebar.slider(
    "하루 권장 식비 예산 설정 (원)", 
    min_value=5000, 
    max_value=30000, 
    value=15000, 
    step=1000
)

recent_df = df.tail(view_days).copy()


st.header(f"📌 최근 {view_days}일간 지출 요약")

total_spent = recent_df["식비"].sum()
avg_spent = int(recent_df["식비"].mean())
over_budget_days = int((recent_df["식비"] > daily_budget).sum())

# 데이터: 요약 정보 metric
col1, col2, col3 = st.columns(3)
col1.metric("총 지출액", f"{total_spent:,}원")
col2.metric("일평균 식비", f"**{avg_spent:,}원**", delta=f"{avg_spent - daily_budget:,}원 (목표 대비)", delta_color="inverse")
col3.metric("예산 초과 일수", f"**{over_budget_days}일** / {view_days}일")

st.divider()


st.header("📈 일자별 식비 지출 추이")

# 일일 목표 예산 기준선 차트
recent_df["목표 예산"] = daily_budget

# 설정 날짜범위 차트용 데이터 설정
chart_data = recent_df.set_index("날짜")[["식비", "목표 예산"]]

# 차트 출력 (위젯-화면 연동)
st.line_chart(chart_data)

st.divider()

# 데이터
st.header("📋 세부 기록 내역")
st.dataframe(
    recent_df[["날짜", "식비"]].sort_values(by="날짜", ascending=False), 
    use_container_width=True
)
