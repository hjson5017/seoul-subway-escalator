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
    # main.py(또는 app.py)가 있는 폴더를 기준으로 CSV 경로를 만들어서
    # 실행 위치가 달라져도 항상 같은 폴더의 CSV를 찾도록 함
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "escalator_data.csv")
    df = pd.read_csv(csv_path)
    return df

df = load_data()
