import streamlit as st
import re
import json
import os
from datetime import date

# ============================================================
# CẤU HÌNH TRANG
# ============================================================

st.set_page_config(
    page_title="Đăng ký vay vốn ngân hàng",
    page_icon="🏦",
    layout="wide"
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f4f7fb;
}

.header {
    background: white;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 25px;
    border: 1px solid #e5e9f0;
}

.title {
    color: #0b4ea2;
    font-size: 32px;
    font-weight: bold;
}

.subtitle {
    color: #687386;
    font-size: 15px;
}

.section {
    background: white;
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.05);
}

.section-title {
    color: #0b4ea2;
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 5px;
}

.section-description {
    color: #687386;
    font-size: 14px;
    margin-bottom: 20px;
}

.success-box {
    background: #e7f7ed;
    padding: 25px;
    border-radius: 12px;
    border: 1px solid #b9e6c8;
    text-align: center;
}

.loan-code {
    background: #edf5ff;
    padding: 12px;
    border-radius: 8px;
    color: #0b4ea2;
    font-weight: bold;
}

.summary-box {
    background: #f8fafc;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.required {
    color: red;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# KHỞI TẠO SESSION STATE
# ============================================================

if "step" not in st.session_state:
    st.session_state.step = 1

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "form_data" not in st.session_state:
    st.session_state.form_data = {}


# ============================================================
# HÀM FORMAT TIỀN
# ============================================================

def format_money(value):

    try:
        return f"{float(value):,.0f}".replace(",", ".")
    except:
        return "0"


# ============================================================
# VALIDATE
# ============================================================

def validate_cccd(cccd):

    return bool(
        re.fullmatch(r"\d{9}|\d{12}", cccd)
    )


def validate_phone(phone):

    return bool(
        re.fullmatch(r"0\d{9}", phone)
    )


def validate_email(email):

    pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"

    return bool(
        re.fullmatch(pattern, email)
    )


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="header">

<div class="title">
🏦 ĐĂNG KÝ VAY VỐN NGÂN HÀNG
</div>

<div class="subtitle">
Vui lòng cung cấp đầy đủ thông tin để ngân hàng
tiếp nhận và xử lý hồ sơ vay vốn.
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# TRANG XÁC NHẬN SAU KHI SUBMIT
# ============================================================

if st.session_state.submitted:

    st.markdown("""
    <div class="success-box">

    <h1>✅ Đăng ký thành công!</h1>

    <p>
    Hồ sơ vay vốn của Quý khách đã được ghi nhận.
    </p>

    </div>
    """, unsafe_allow_html=True)

    loan_code = (
        "HV"
        + str(date.today().year)
        + str(abs(hash(str(st.session_state.form_data))))[-6:]
    )

    st.markdown(
        f"""
        <div class="loan-code">
        Mã hồ sơ: {loan_code}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    data = st.session_state.form_data

    # ========================================================
    # TÓM TẮT HỒ SƠ
    # ========================================================

    st.subheader("📋 Tóm tắt hồ sơ")

    # --------------------------------------------------------
    # THÔNG TIN CÁ NHÂN
    # --------------------------------------------------------

    with st.expander("👤 Thông tin cá nhân", expanded=True):

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Họ và tên:** {data.get('full_name', '')}"
            )

            st.write(
                f"**CMND/CCCD:** {data.get('cccd', '')}"
            )

            st.write(
                f"**Ngày cấp:** {data.get('issue_date', '')}"
            )

            st.write(
                f"**Nơi cấp:** {data.get('issue_place', '')}"
            )

            st.write(
                f"**Ngày sinh:** {data.get('birth_date', '')}"
            )

        with col2:

            st.write(
                f"**Giới tính:** {data.get('gender', '')}"
            )

            st.write(
                f"**Điện thoại:** {data.get('phone', '')}"
            )

            st.write(
                f"**Email:** {data.get('email', '')}"
            )

            st.write(
                f"**Địa chỉ thường trú:** "
                f"{data.get('permanent_address', '')}"
            )

            st.write(
                f"**Địa chỉ hiện tại:** "
                f"{data.get('current_address', '')}"
            )

    # --------------------------------------------------------
    # KHOẢN VAY
    # --------------------------------------------------------

    with st.expander("💰 Thông tin khoản vay", expanded=True):

        st.write(
            f"**Mục đích vay:** "
            f"{data.get('loan_purpose', '')}"
        )

        st.write(
            f"**Số tiền vay:** "
            f"{format_money(data.get('loan_amount', 0))} VNĐ"
        )

        st.write(
            f"**Thời hạn:** "
            f"{data.get('loan_term', '')} "
            f"{data.get('loan_unit', '')}"
        )

        st.write(
            f"**Hình thức trả nợ:** "
            f"{data.get('repayment_method', '')}"
        )

    # --------------------------------------------------------
    # TÀI CHÍNH
    # --------------------------------------------------------

    with st.expander("📊 Thông tin tài chính"):

        st.write(
            f"**Nghề nghiệp:** "
            f"{data.get('occupation', '')}"
        )

        st.write(
            f"**Nơi công tác:** "
            f"{data.get('workplace', '')}"
        )

        st.write(
            f"**Thu nhập hàng tháng:** "
            f"{format_money(data.get('income', 0))} VNĐ"
        )

        st.write(
            f"**Nguồn trả nợ:** "
            f"{data.get('repayment_source', '')}"
        )

    # --------------------------------------------------------
    # TÀI SẢN
    # --------------------------------------------------------

    with st.expander("🏠 Tài sản đảm bảo"):

        st.write(
            f"**Có tài sản đảm bảo:** "
            f"{data.get('collateral', '')}"
        )

        if data.get("collateral") == "Có":

            st.write(
                f"**Loại tài sản:** "
                f"{data.get('collateral_type', '')}"
            )

            st.write(
                f"**Giá trị ước tính:** "
                f"{format_money(data.get('collateral_value', 0))} VNĐ"
            )

        st.write(
            f"**Số lượng hồ sơ đính kèm:** "
            f"{data.get('file_count', 0)} file"
        )

    st.write("")

    if st.button(
        "📝 Đăng ký hồ sơ mới",
        use_container_width=True
    ):

        st.session_state.step = 1
        st.session_state.submitted = False
        st.session_state.form_data = {}

        st.rerun()

    st.stop()


# ============================================================
# THANH TIẾN TRÌNH
# ============================================================

steps = [
    "Thông tin cá nhân",
    "Thông tin khoản vay",
    "Tài chính",
    "Tài sản đảm bảo",
    "Xác nhận"
]

current_step = st.session_state.step

progress = (current_step - 1) / 4

st.progress(progress)

cols = st.columns(5)

for i, step_name in enumerate(steps):

    with cols[i]:

        if i + 1 < current_step:

            st.success(
                f"✓ {step_name}"
            )

        elif i + 1 == current_step:

            st.info(
                f"**{i + 1}. {step_name}**"
            )

        else:

            st.caption(
                f"{i + 1}. {step_name}"
            )


st.write("")


# ============================================================
# BƯỚC 1
# ============================================================

if current_step == 1:

    st.markdown(
        '<div class="section">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">👤 Thông tin cá nhân</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Thông tin định danh và thông tin liên hệ của khách hàng'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        full_name = st.text_input(
            "Họ và tên *",
            placeholder="Nguyễn Văn A"
        )

        cccd = st.text_input(
            "Số CMND/CCCD *",
            placeholder="012345678901"
        )

        issue_date = st.date_input(
            "Ngày cấp *",
            value=None
        )

        issue_place = st.text_input(
            "Nơi cấp *",
            placeholder="Cục Cảnh sát QLHC về TTXH"
        )

        birth_date = st.date_input(
            "Ngày sinh *",
            value=None
        )

    with col2:

        gender = st.selectbox(
            "Giới tính *",
            [
                "-- Chọn giới tính --",
                "Nam",
                "Nữ",
                "Khác"
            ]
        )

        phone = st.text_input(
            "Số điện thoại *",
            placeholder="09xxxxxxxx"
        )

        email = st.text_input(
            "Email *",
            placeholder="example@email.com"
        )

        permanent_address = st.text_area(
            "Địa chỉ thường trú *",
            placeholder="Số nhà, đường, phường/xã..."
        )

        current_address = st.text_area(
            "Địa chỉ hiện tại *",
            placeholder="Địa chỉ nơi đang sinh sống..."
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    if st.button(
        "Tiếp tục →",
        type="primary",
        use_container_width=True
    ):

        errors = []

        if not full_name.strip():
            errors.append("Vui lòng nhập họ và tên.")

        if not validate_cccd(cccd):
            errors.append(
                "CMND/CCCD phải gồm 9 hoặc 12 chữ số."
            )

        if issue_date is None:
            errors.append("Vui lòng nhập ngày cấp.")

        if not issue_place.strip():
            errors.append("Vui lòng nhập nơi cấp.")

        if birth_date is None:
            errors.append("Vui lòng nhập ngày sinh.")

        if gender == "-- Chọn giới tính --":
            errors.append("Vui lòng chọn giới tính.")

        if not validate_phone(phone):
            errors.append(
                "Số điện thoại phải gồm 10 chữ số và bắt đầu bằng 0."
            )

        if not validate_email(email):
            errors.append("Email không hợp lệ.")

        if not permanent_address.strip():
            errors.append(
                "Vui lòng nhập địa chỉ thường trú."
            )

        if not current_address.strip():
            errors.append(
                "Vui lòng nhập địa chỉ hiện tại."
            )

        if errors:

            for error in errors:
                st.error(error)

        else:

            st.session_state.form_data.update({

                "full_name": full_name,
                "cccd": cccd,
                "issue_date": str(issue_date),
                "issue_place": issue_place,
                "birth_date": str(birth_date),
                "gender": gender,
                "phone": phone,
                "email": email,
                "permanent_address": permanent_address,
                "current_address": current_address

            })

            st.session_state.step = 2

            st.rerun()


# ============================================================
# BƯỚC 2
# ============================================================

elif current_step == 2:

    st.markdown(
        '<div class="section">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">💰 Thông tin khoản vay</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Thông tin về nhu cầu vay vốn của khách hàng'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        loan_purpose = st.selectbox(
            "Mục đích vay *",
            [
                "-- Chọn mục đích --",
                "Mua nhà",
                "Mua xe",
                "Kinh doanh",
                "Tiêu dùng",
                "Học tập",
                "Sửa chữa nhà",
                "Khác"
            ]
        )

        loan_amount = st.number_input(
            "Số tiền vay mong muốn (VNĐ) *",
            min_value=0,
            step=10_000_000,
            value=0
        )

    with col2:

        loan_term = st.number_input(
            "Thời hạn vay *",
            min_value=1,
            step=1,
            value=60
        )

        loan_unit = st.selectbox(
            "Đơn vị thời hạn",
            ["Tháng", "Năm"]
        )

        repayment_method = st.selectbox(
            "Hình thức trả nợ *",
            [
                "-- Chọn hình thức --",
                "Gốc đều – lãi giảm dần",
                "Trả đều gốc và lãi",
                "Gốc cuối kỳ"
            ]
        )

    st.info(
        "💡 Hình thức trả nợ cuối cùng sẽ được ngân hàng "
        "tư vấn và xác định căn cứ vào hồ sơ tín dụng."
    )

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Quay lại",
            use_container_width=True
        ):

            st.session_state.step = 1
            st.rerun()

    with col2:

        if st.button(
            "Tiếp tục →",
            type="primary",
            use_container_width=True
        ):

            errors = []

            if loan_purpose == "-- Chọn mục đích --":

                errors.append(
                    "Vui lòng chọn mục đích vay."
                )

            if loan_amount <= 0:

                errors.append(
                    "Số tiền vay phải lớn hơn 0."
                )

            if loan_term <= 0:

                errors.append(
                    "Thời hạn vay phải lớn hơn 0."
                )

            if repayment_method == "-- Chọn hình thức --":

                errors.append(
                    "Vui lòng chọn hình thức trả nợ."
                )

            if errors:

                for error in errors:
                    st.error(error)

            else:

                st.session_state.form_data.update({

                    "loan_purpose": loan_purpose,
                    "loan_amount": loan_amount,
                    "loan_term": loan_term,
                    "loan_unit": loan_unit,
                    "repayment_method": repayment_method

                })

                st.session_state.step = 3

                st.rerun()


# ============================================================
# BƯỚC 3
# ============================================================

elif current_step == 3:

    st.markdown(
        '<div class="section">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">📊 Thông tin tài chính / Thu nhập</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Thông tin giúp ngân hàng đánh giá khả năng trả nợ'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        occupation = st.text_input(
            "Nghề nghiệp *",
            placeholder="Nhân viên văn phòng"
        )

        workplace = st.text_input(
            "Nơi công tác *",
            placeholder="Tên công ty / tổ chức"
        )

    with col2:

        income = st.number_input(
            "Thu nhập hàng tháng (VNĐ) *",
            min_value=0,
            step=1_000_000,
            value=0
        )

        repayment_source = st.selectbox(
            "Nguồn trả nợ *",
            [
                "-- Chọn nguồn trả nợ --",
                "Tiền lương",
                "Thu nhập kinh doanh",
                "Cho thuê tài sản",
                "Thu nhập đầu tư",
                "Nguồn khác"
            ]
        )

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Quay lại",
            use_container_width=True
        ):

            st.session_state.step = 2
            st.rerun()

    with col2:

        if st.button(
            "Tiếp tục →",
            type="primary",
            use_container_width=True
        ):

            errors = []

            if not occupation.strip():

                errors.append(
                    "Vui lòng nhập nghề nghiệp."
                )

            if not workplace.strip():

                errors.append(
                    "Vui lòng nhập nơi công tác."
                )

            if income <= 0:

                errors.append(
                    "Thu nhập phải lớn hơn 0."
                )

            if repayment_source == "-- Chọn nguồn trả nợ --":

                errors.append(
                    "Vui lòng chọn nguồn trả nợ."
                )

            if errors:

                for error in errors:
                    st.error(error)

            else:

                st.session_state.form_data.update({

                    "occupation": occupation,
                    "workplace": workplace,
                    "income": income,
                    "repayment_source": repayment_source

                })

                st.session_state.step = 4

                st.rerun()


# ============================================================
# BƯỚC 4
# ============================================================

elif current_step == 4:

    st.markdown(
        '<div class="section">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">🏠 Tài sản đảm bảo</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Thông tin tài sản dùng để đảm bảo khoản vay'
        '</div>',
        unsafe_allow_html=True
    )

    collateral = st.radio(
        "Có tài sản đảm bảo không?",
        ["Có", "Không"],
        horizontal=True
    )

    collateral_type = ""
    collateral_value = 0

    if collateral == "Có":

        col1, col2 = st.columns(2)

        with col1:

            collateral_type = st.selectbox(
                "Loại tài sản *",
                [
                    "-- Chọn loại tài sản --",
                    "Bất động sản",
                    "Ô tô",
                    "Xe máy",
                    "Tài sản khác"
                ]
            )

        with col2:

            collateral_value = st.number_input(
                "Giá trị ước tính (VNĐ) *",
                min_value=0,
                step=10_000_000,
                value=0
            )

    st.subheader("📎 Hồ sơ đính kèm")

    st.caption(
        "Có thể tải lên CMND/CCCD, giấy tờ tài sản, "
        "sao kê lương... "
    )

    uploaded_files = st.file_uploader(
        "Chọn file",
        type=[
            "pdf",
            "jpg",
            "jpeg",
            "png",
            "doc",
            "docx"
        ],
        accept_multiple_files=True
    )

    if uploaded_files:

        st.write("### File đã chọn")

        for file in uploaded_files:

            size_mb = file.size / (
                1024 * 1024
            )

            st.write(
                f"📄 {file.name} "
                f"({size_mb:.2f} MB)"
            )

            if file.size > 5 * 1024 * 1024:

                st.error(
                    f"File {file.name} vượt quá 5MB."
                )

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Quay lại",
            use_container_width=True
        ):

            st.session_state.step = 3
            st.rerun()

    with col2:

        if st.button(
            "Tiếp tục →",
            type="primary",
            use_container_width=True
        ):

            errors = []

            if collateral == "Có":

                if collateral_type == "-- Chọn loại tài sản --":

                    errors.append(
                        "Vui lòng chọn loại tài sản."
                    )

                if collateral_value <= 0:

                    errors.append(
                        "Giá trị tài sản phải lớn hơn 0."
                    )

            if uploaded_files:

                for file in uploaded_files:

                    if file.size > 5 * 1024 * 1024:

                        errors.append(
                            f"File {file.name} vượt quá 5MB."
                        )

            if errors:

                for error in errors:
                    st.error(error)

            else:

                st.session_state.form_data.update({

                    "collateral": collateral,
                    "collateral_type": collateral_type,
                    "collateral_value": collateral_value,
                    "file_count": len(uploaded_files)

                })

                st.session_state.step = 5

                st.rerun()


# ============================================================
# BƯỚC 5
# ============================================================

elif current_step == 5:

    data = st.session_state.form_data

    st.markdown(
        '<div class="section">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">✅ Xác nhận hồ sơ</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Vui lòng kiểm tra lại toàn bộ thông tin trước khi gửi'
        '</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # CÁ NHÂN
    # ========================================================

    st.subheader("👤 Thông tin cá nhân")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Họ và tên:** {data['full_name']}"
        )

        st.write(
            f"**CMND/CCCD:** {data['cccd']}"
        )

        st.write(
            f"**Ngày cấp:** {data['issue_date']}"
        )

        st.write(
            f"**Nơi cấp:** {data['issue_place']}"
        )

        st.write(
            f"**Ngày sinh:** {data['birth_date']}"
        )

    with col2:

        st.write(
            f"**Giới tính:** {data['gender']}"
        )

        st.write(
            f"**Điện thoại:** {data['phone']}"
        )

        st.write(
            f"**Email:** {data['email']}"
        )

        st.write(
            f"**Địa chỉ thường trú:** "
            f"{data['permanent_address']}"
        )

        st.write(
            f"**Địa chỉ hiện tại:** "
            f"{data['current_address']}"
        )

    st.divider()

    # ========================================================
    # KHOẢN VAY
    # ========================================================

    st.subheader("💰 Thông tin khoản vay")

    st.write(
        f"**Mục đích vay:** "
        f"{data['loan_purpose']}"
    )

    st.write(
        f"**Số tiền vay:** "
        f"{format_money(data['loan_amount'])} VNĐ"
    )

    st.write(
        f"**Thời hạn:** "
        f"{data['loan_term']} {data['loan_unit']}"
    )

    st.write(
        f"**Hình thức trả nợ:** "
        f"{data['repayment_method']}"
    )

    st.divider()

    # ========================================================
    # TÀI CHÍNH
    # ========================================================

    st.subheader("📊 Thông tin tài chính")

    st.write(
        f"**Nghề nghiệp:** "
        f"{data['occupation']}"
    )

    st.write(
        f"**Nơi công tác:** "
        f"{data['workplace']}"
    )

    st.write(
        f"**Thu nhập:** "
        f"{format_money(data['income'])} VNĐ/tháng"
    )

    st.write(
        f"**Nguồn trả nợ:** "
        f"{data['repayment_source']}"
    )

    st.divider()

    # ========================================================
    # TÀI SẢN
    # ========================================================

    st.subheader("🏠 Tài sản đảm bảo")

    st.write(
        f"**Tài sản đảm bảo:** "
        f"{data['collateral']}"
    )

    if data["collateral"] == "Có":

        st.write(
            f"**Loại tài sản:** "
            f"{data['collateral_type']}"
        )

        st.write(
            f"**Giá trị:** "
            f"{format_money(data['collateral_value'])} VNĐ"
        )

    st.write(
        f"**Hồ sơ đính kèm:** "
        f"{data['file_count']} file"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.warning(
        "⚠️ Vui lòng kiểm tra kỹ thông tin. "
        "Sau khi gửi, hồ sơ sẽ được chuyển sang bước "
        "tiếp nhận và thẩm định."
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Chỉnh sửa",
            use_container_width=True
        ):

            st.session_state.step = 4
            st.rerun()

    with col2:

        if st.button(
            "🚀 GỬI HỒ SƠ",
            type="primary",
            use_container_width=True
        ):

            st.session_state.submitted = True

            st.rerun()
