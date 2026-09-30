```python
import streamlit as st
import pandas as pd


# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="wide"
)


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def money(value):
    return f"{value:,.0f} VNĐ"


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.title("💰 TÍNH LÃI GỬI TIẾT KIỆM")

st.markdown(
    """
    Ứng dụng tính tiền lãi tiền gửi theo **lãi đơn** hoặc **lãi kép**.
    
    Bạn có thể lựa chọn:
    - 📅 Lãnh lãi theo tháng
    - 📅 Lãnh lãi theo quý
    - 🏦 Lãnh lãi cuối kỳ
    """
)

st.divider()


# =========================================================
# NHẬP THÔNG TIN
# =========================================================

st.subheader("📋 Thông tin khoản gửi")

col1, col2 = st.columns(2)

with col1:

    so_tien = st.number_input(
        "💵 Số tiền gửi (VNĐ)",
        min_value=1000.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    ky_han = st.number_input(
        "⏱️ Kỳ hạn",
        min_value=1,
        value=12,
        step=1
    )

    don_vi_ky_han = st.selectbox(
        "Đơn vị kỳ hạn",
        ["Tháng", "Năm"]
    )


with col2:

    lai_suat = st.number_input(
        "📈 Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1,
        format="%.2f"
    )

    loai_lai = st.selectbox(
        "🔢 Phương pháp tính lãi",
        ["Lãi đơn", "Lãi kép"]
    )

    hinh_thuc = st.selectbox(
        "💳 Hình thức nhận lãi",
        [
            "Lãnh lãi theo tháng",
            "Lãnh lãi theo quý",
            "Lãnh lãi cuối kỳ"
        ]
    )


# =========================================================
# QUY ĐỔI KỲ HẠN
# =========================================================

if don_vi_ky_han == "Năm":
    so_thang = ky_han * 12
else:
    so_thang = ky_han


# =========================================================
# NÚT TÍNH
# =========================================================

st.divider()

tinh = st.button(
    "🧮 TÍNH TIỀN LÃI",
    type="primary",
    use_container_width=True
)


if tinh:

    # -----------------------------------------------------
    # LÃI SUẤT
    # -----------------------------------------------------

    lai_nam = lai_suat / 100
    lai_thang = lai_nam / 12


    # -----------------------------------------------------
    # BIẾN KẾT QUẢ
    # -----------------------------------------------------

    tong_lai = 0
    tong_tien = so_tien
    lai_dinh_ky = 0

    chi_tiet = []


    # =====================================================
    # LÃI ĐƠN
    # =====================================================

    if loai_lai == "Lãi đơn":

        # -------------------------------------------------
        # LÃNH LÃI THEO THÁNG
        # -------------------------------------------------

        if hinh_thuc == "Lãnh lãi theo tháng":

            lai_dinh_ky = so_tien * lai_thang

            for thang in range(1, so_thang + 1):

                tong_lai += lai_dinh_ky

                chi_tiet.append({
                    "Kỳ": thang,
                    "Thời gian": f"Tháng {thang}",
                    "Tiền gốc": money(so_tien),
                    "Tiền lãi": money(lai_dinh_ky)
                })

            tong_tien = so_tien + tong_lai


        # -------------------------------------------------
        # LÃNH LÃI THEO QUÝ
        # -------------------------------------------------

        elif hinh_thuc == "Lãnh lãi theo quý":

            so_quy = so_thang // 3
            thang_le = so_thang % 3

            lai_moi_quy = so_tien * lai_nam / 4

            lai_dinh_ky = lai_moi_quy

            for quy in range(1, so_quy + 1):

                tong_lai += lai_moi_quy

                chi_tiet.append({
                    "Kỳ": quy,
                    "Thời gian": f"Quý {quy}",
                    "Tiền gốc": money(so_tien),
                    "Tiền lãi": money(lai_moi_quy)
                })

            # Xử lý số tháng còn lại
            if thang_le > 0:

                lai_le = so_tien * lai_thang * thang_le

                tong_lai += lai_le

                chi_tiet.append({
                    "Kỳ": so_quy + 1,
                    "Thời gian": f"{thang_le} tháng còn lại",
                    "Tiền gốc": money(so_tien),
                    "Tiền lãi": money(lai_le)
                })

            tong_tien = so_tien + tong_lai


        # -------------------------------------------------
        # LÃNH LÃI CUỐI KỲ
        # -------------------------------------------------

        else:

            tong_lai = (
                so_tien
                * lai_nam
                * so_thang
                / 12
            )

            lai_dinh_ky = tong_lai
            tong_tien = so_tien + tong_lai

            chi_tiet.append({
                "Kỳ": 1,
                "Thời gian": f"Cuối kỳ ({so_thang} tháng)",
                "Tiền gốc": money(so_tien),
                "Tiền lãi": money(tong_lai)
            })


    # =====================================================
    # LÃI KÉP
    # =====================================================

    else:

        von = so_tien


        # -------------------------------------------------
        # LÃNH LÃI THEO THÁNG
        # -------------------------------------------------

        if hinh_thuc == "Lãnh lãi theo tháng":

            for thang in range(1, so_thang + 1):

                von_dau_ky = von

                lai_ky = von * lai_thang

                von += lai_ky

                tong_lai += lai_ky

                lai_dinh_ky = lai_ky

                chi_tiet.append({
                    "Kỳ": thang,
                    "Thời gian": f"Tháng {thang}",
                    "Tiền đầu kỳ": money(von_dau_ky),
                    "Tiền lãi": money(lai_ky),
                    "Tiền cuối kỳ": money(von)
                })

            tong_tien = von


        # -------------------------------------------------
        # LÃNH LÃI THEO QUÝ
        # -------------------------------------------------

        elif hinh_thuc == "Lãnh lãi theo quý":

            so_quy = so_thang // 3
            thang_le = so_thang % 3

            lai_quy = lai_nam / 4

            for quy in range(1, so_quy + 1):

                von_dau_ky = von

                lai_ky = von * lai_quy

                von += lai_ky

                tong_lai += lai_ky

                lai_dinh_ky = lai_ky

                chi_tiet.append({
                    "Kỳ": quy,
                    "Thời gian": f"Quý {quy}",
                    "Tiền đầu kỳ": money(von_dau_ky),
                    "Tiền lãi": money(lai_ky),
                    "Tiền cuối kỳ": money(von)
                })


            # Xử lý tháng lẻ
            if thang_le > 0:

                von_dau_ky = von

                lai_le = von * lai_thang * thang_le

                von += lai_le

                tong_lai += lai_le

                lai_dinh_ky = lai_le

                chi_tiet.append({
                    "Kỳ": so_quy + 1,
                    "Thời gian": f"{thang_le} tháng còn lại",
                    "Tiền đầu kỳ": money(von_dau_ky),
                    "Tiền lãi": money(lai_le),
                    "Tiền cuối kỳ": money(von)
                })


            tong_tien = von


        # -------------------------------------------------
        # LÃNH LÃI CUỐI KỲ
        # -------------------------------------------------

        else:

            # Lãi kép theo tháng
            tong_tien = (
                so_tien
                * (1 + lai_thang) ** so_thang
            )

            tong_lai = tong_tien - so_tien

            lai_dinh_ky = tong_lai

            chi_tiet.append({
                "Kỳ": 1,
                "Thời gian": f"Cuối kỳ ({so_thang} tháng)",
                "Tiền gốc": money(so_tien),
                "Tiền lãi": money(tong_lai),
                "Tổng tiền": money(tong_tien)
            })


    # =====================================================
    # HIỂN THỊ KẾT QUẢ
    # =====================================================

    st.success("✅ Đã tính toán
```
