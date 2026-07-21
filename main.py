import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="지하철 역사 에스컬레이터 길이 조회", layout="wide")

# ---------------------------
# 데이터 로드
# ---------------------------
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    xlsx_path = os.path.join(base_dir, "서울교통공사_지하철_역사_엘리베이터_및_에스컬레이터_길이_높이_정보_20260211.xlsx")
    
    df = pd.read_excel(xlsx_path, sheet_name="ES 설치높이 및 운행길이", header=1)
    df.columns = [c.replace("\n", "") for c in df.columns]
    
    # 콤마를 소수점으로 정제 (원본 데이터에 오류값 2건 존재)
    df["운행길이(m)"] = df["운행길이(m)"].astype(str).str.replace(",", ".", regex=False)
    df["운행길이(m)"] = pd.to_numeric(df["운행길이(m)"], errors="coerce")
    df["설치높이(m)"] = pd.to_numeric(df["설치높이(m)"], errors="coerce")
    df["경사길이(m)"] = pd.to_numeric(df["경사길이(m)"], errors="coerce")
    
    cols = ["호선", "역명", "호기", "승강기번호", "운행구간(자체조사)", "운행방향",
            "설치높이(m)", "경사길이(m)", "운행길이(m)"]
    df = df[cols].dropna(subset=["역명", "운행길이(m)"])
    return df

df = load_data()
