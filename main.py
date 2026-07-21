import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="지하철 역사 에스컬레이터 길이 조회", layout="wide")

# ---------------------------
# 데이터 로드
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("escalator_data.csv")
    return df

df = load_data()

st.title("🚇 지하철 역사별 에스컬레이터 운행길이")
st.caption("서울교통공사 지하철 역사 에스컬레이터 설치높이 및 운행길이 정보 (2026.02.11 기준)")

# ---------------------------
# 지역(역명) 선택 + 직접 입력
# ---------------------------
station_list = sorted(df["역명"].dropna().unique())

st.subheader("🔍 역 선택")

col1, col2 = st.columns([1, 1])

with col1:
    selected_station = st.selectbox(
        "목록에서 역 선택",
        options=["(직접 입력 사용)"] + station_list,
        index=0,
    )

with col2:
    typed_station = st.text_input(
        "역명 직접 입력 (예: 청량리, 강남 등 일부만 입력해도 검색됩니다)",
        value="",
        placeholder="역명을 입력하세요",
    )

# 우선순위: 직접 입력이 있으면 입력값으로 검색, 없으면 선택박스 값 사용
if typed_station.strip():
    matched = [s for s in station_list if typed_station.strip() in s]
    if len(matched) == 0:
        st.warning(f"'{typed_station}'와 일치하는 역이 없습니다. 목록에서 선택해주세요.")
        st.stop()
    elif len(matched) == 1:
        target_station = matched[0]
    else:
        target_station = st.selectbox("일치하는 역이 여러 개입니다. 선택해주세요.", matched)
else:
    if selected_station == "(직접 입력 사용)":
        st.info("왼쪽에서 역을 선택하거나, 오른쪽에 역명을 입력해주세요.")
        st.stop()
    target_station = selected_station

# ---------------------------
# 데이터 필터링 및 정렬
# ---------------------------
station_df = df[df["역명"] == target_station].copy()
station_df = station_df.sort_values("운행길이(m)", ascending=False)

# x축 라벨: 승강기번호 + 호기 정보를 함께 표기
station_df["표시라벨"] = station_df["호기"].astype(str) + "호기 (" + station_df["승강기번호"].astype(str) + ")"

st.subheader(f"📊 {target_station} 에스컬레이터 운행길이 (긴 순서)")

if station_df.empty:
    st.warning("해당 역의 에스컬레이터 데이터가 없습니다.")
else:
    fig = px.bar(
        station_df,
        x="표시라벨",
        y="운행길이(m)",
        color="운행방향",
        text="운행길이(m)",
        hover_data={
            "호선": True,
            "운행구간(자체조사)": True,
            "설치높이(m)": True,
            "경사길이(m)": True,
            "표시라벨": False,
        },
        labels={"표시라벨": "승강기 (호기 / 번호)", "운행길이(m)": "운행길이 (m)"},
    )
    fig.update_traces(texttemplate="%{text:.1f}m", textposition="outside")
    fig.update_layout(
        xaxis_tickangle=-30,
        yaxis_title="운행길이 (m)",
        xaxis_title="승강기",
        legend_title="운행방향",
        height=550,
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("원본 데이터 보기"):
        st.dataframe(
            station_df[["호선", "호기", "승강기번호", "운행구간(자체조사)", "운행방향",
                        "설치높이(m)", "경사길이(m)", "운행길이(m)"]],
            use_container_width=True,
        )
