import streamlit as st
import sympy as sp

st.set_page_config(page_title="แยกตัวประกอบพหุนาม", layout="centered")

x = sp.symbols('x')

# ตั้งชื่อแอป
st.title("📐 เครื่องมือแยกตัวประกอบพหุนาม (มีปุ่มกดช่วยพิมพ์)")

# ใช้ session_state เพื่อเก็บข้อความที่พิมพ์
if "poly_input" not in st.session_state:
    st.session_state.poly_input = ""

st.markdown("### ✍️ ใส่พหุนาม (เช่น `x^2+5*x+6`)")

# แสดงกล่องข้อความแบบจำลอง Entry
st.code(st.session_state.poly_input, language="plaintext")

# ปุ่มกดเหมือนคีย์บอร์ด
buttons = [
    ['7', '8', '9', '+', '-'],
    ['4', '5', '6', '*', '/'],
    ['1', '2', '3', 'x', '^'],
    ['0', '(', ')', '⌫', ' '],
]

for row in buttons:
    cols = st.columns(len(row))
    for i, btn in enumerate(row):
        if cols[i].button(btn):
            if btn == '⌫':
                st.session_state.poly_input = st.session_state.poly_input[:-1]
            else:
                st.session_state.poly_input += btn

# ปุ่มคำนวณ และ ล้างค่า
col1, col2 = st.columns(2)

with col1:
    if st.button("✅ คำนวณแยกตัวประกอบ"):
        try:
            expr_str_fixed = st.session_state.poly_input.replace("^", "**").replace(" ", "")
            expr = sp.sympify(expr_str_fixed, locals={'x': x})

            if expr.free_symbols != {x} and expr.free_symbols != set():
                st.error("❌ กรุณาใช้ตัวแปร x เท่านั้น")
            else:
                degree = sp.degree(expr, x)
                if degree is None or degree < 2 or degree > 10:
                    st.warning("⚠️ รองรับพหุนามดีกรี 2 ถึง 10 เท่านั้น")
                else:
                    factored_expr = sp.factor(expr)

                    st.markdown("### 📝 หมายเหตุ")
                    st.info("ในเวอร์ชันนี้ไม่แสดงรากโดยตรง กรุณาดูผลการแยกตัวประกอบด้านล่าง")

                    st.markdown("### 📌 ผลการแยกตัวประกอบ:")
                    st.latex(sp.latex(factored_expr))
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")

with col2:
    if st.button("🧹 ล้างค่า"):
        st.session_state.poly_input = ""
        st.experimental_rerun()

