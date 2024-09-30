import streamlit as st
import pandas as pd
import numpy as np


def page2():
    st.title("Second page")

pg = st.navigation([
    st.Page("page1.py", title="First page", icon="🔥"),
    st.Page("reviews.py", title="Nhận xét và đánh giá", icon="🔥"),])
pg.run()