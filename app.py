import streamlit as st
import pandas as pd
import os

# =========================
# CẤU HÌNH APP
# =========================
st.set_page_config(
    page_title="Quản lý khách hàng",
    page_icon="📋",
    layout="wide"
)

FILE_NAME = "customers.csv"

# =========================
# HÀM ĐỌC DỮ LIỆU
# =========================
def load_data():
    if os.path.exists(FILE_NAME):
        try:
            return pd.read_csv(FILE_NAME, dtype=str)
        except:
            pass

    return pd.DataFrame(
        columns=[
            "Số điện thoại",
            "Tên khách hàng",
            "Khu vực",
            "Ghi chú"
        ]
    )


# =========================
# HÀM LƯU DỮ LIỆU
# =========================
def save_data(df):
    df.to_csv(
        FILE_NAME,
        index=False,
        encoding="utf-8-sig"
    )


# =========================
# TIÊU ĐỀ
# =========================
st.title("📋 QUẢN LÝ THÔNG TIN KHÁCH HÀNG")
st.write("Nhập và quản lý thông tin khách hàng")

st.divider()

# =========================
# FORM NHẬP KHÁCH HÀNG
# =========================
st.subheader("➕ Thêm khách hàng")

with st.form("customer_form", clear_on_submit=True):

    col1, col2 = st.columns(2)

    with col1:
        phone = st.text_input(
            "📱 Số điện thoại *",
            placeholder="Nhập số điện thoại"
        )

        name = st.text_input(
            "👤 Tên khách hàng *",
            placeholder="Nhập tên khách hàng"
        )

    with col2:
        area = st.selectbox(
            "📍 Khu vực",
            [
                "Hà Nội",
                "TP. Hồ Chí Minh",
                "Đà Lạt",
                "Đà Nẵng",
                "Hải Phòng",
                "Cần Thơ",
                "Khác"
            ]
        )

        note = st.text_area(
            "📝 Ghi chú",
            placeholder="Nhập ghi chú về khách hàng..."
        )

    submitted = st.form_submit_button(
        "💾 Lưu khách hàng",
        use_container_width=True
    )

# =========================
# XỬ LÝ LƯU
# =========================
if submitted:

    if not phone.strip():
        st.error("⚠️ Vui lòng nhập số điện thoại.")

    elif not name.strip():
        st.error("⚠️ Vui lòng nhập tên khách hàng.")

    else:
        df = load_data()

        # Kiểm tra số điện thoại trùng
        if not df.empty and phone.strip() in df["Số điện thoại"].astype(str).values:
            st.warning(
                "⚠️ Số điện thoại này đã tồn tại trong danh sách."
            )

        else:
            new_customer = pd.DataFrame({
                "Số điện thoại": [phone.strip()],
                "Tên khách hàng": [name.strip()],
                "Khu vực": [area],
                "Ghi chú": [note.strip()]
            })

            df = pd.concat(
                [df, new_customer],
                ignore_index=True
            )

            save_data(df)

            st.success(
                f"✅ Đã lưu khách hàng: {name}"
            )


st.divider()

# =========================
# DANH SÁCH KHÁCH HÀNG
# =========================
st.subheader("👥 Danh sách khách hàng")

df = load_data()

if df.empty:
    st.info("Chưa có khách hàng nào.")

else:

    # =========================
    # THỐNG KÊ
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Tổng số khách hàng",
            len(df)
        )

    with col2:
        st.metric(
            "Số khu vực",
            df["Khu vực"].nunique()
        )

    st.write("")

    # =========================
    # TÌM KIẾM
    # =========================
    search = st.text_input(
        "🔎 Tìm kiếm khách hàng",
        placeholder="Nhập tên hoặc số điện thoại..."
    )

    filtered_df = df.copy()

    if search.strip():

        search = search.strip().lower()

        filtered_df = df[
            df["Tên khách hàng"]
            .str.lower()
            .str.contains(search, na=False)
            |
            df["Số điện thoại"]
            .str.lower()
            .str.contains(search, na=False)
        ]

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    # =========================
    # XÓA KHÁCH HÀNG
    # =========================
    st.subheader("🗑️ Xóa khách hàng")

    customer_list = (
        df["Số điện thoại"]
        + " - "
        + df["Tên khách hàng"]
    ).tolist()

    selected_customer = st.selectbox(
        "Chọn khách hàng muốn xóa",
        customer_list
    )

    if st.button(
        "🗑️ Xóa khách hàng",
        type="secondary"
    ):

        selected_phone = selected_customer.split(" - ")[0]

        df = df[
            df["Số điện thoại"] != selected_phone
        ]

        save_data(df)

        st.success("✅ Đã xóa khách hàng.")

        st.rerun()


st.divider()

# =========================
# TẢI DỮ LIỆU
# =========================
if not df.empty:

    st.subheader("📥 Xuất dữ liệu")

    csv_data = df.to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    st.download_button(
        label="⬇️ Tải danh sách khách hàng (.csv)",
        data=csv_data,
        file_name="danh_sach_khach_hang.csv",
        mime="text/csv",
        use_container_width=True
    )
