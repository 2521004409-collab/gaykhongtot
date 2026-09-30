```python
import streamlit as st
import pandas as pd


# ============================================================
# CẤU HÌNH ỨNG DỤNG
# ============================================================

st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="wide"
)


# ============================================================
# HÀM ĐỊNH DẠNG TIỀN
# ============================================================

def format_money(number):
    return f"{number:,.0f} VNĐ"


# ============================================================
# TIÊU ĐỀ
# ============================================================

st.title("💰 TÍNH LÃI GỬI TIẾT KIỆM")

st.write(
    "Ứng dụng tính tiền lãi theo **lãi đơn** hoặc **lãi kép** "
    "với các hình thức nhận lãi theo tháng, theo quý hoặc cuối kỳ."
)

st.divider()


# ============================================================
# NHẬP DỮ LIỆU
# ============================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("📌 Thông tin tiền gửi")

    tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=1_000_000,
        value=100_000_000,
        step=1_000_000,
        format="%.0f"
    )

    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        max_value=600,
        value=12,
        step=1
    )


with col2:

    st.subheader("⚙️ Thông tin lãi suất")

    lai_suat = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1
    )

    loai_lai = st.selectbox(
        "Phương pháp tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

    hinh_thuc = st.selectbox(
        "Hình thức nhận lãi",
```
