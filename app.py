import streamlit as st
import sympy as sp

st.set_page_config(page_title="แยกตัวประกอบพหุนาม", layout="centered")
x = sp.symbols('x')

# ค่าพหุนามที่พิมพ์
poly_input = st.text_input("🧮 ใส่พหุนาม (เช่น x^2+5*x+6)", value=st.session_state.get("poly_input", ""))

# บันทึกลง session state
st.session_state.poly_input = poly_input

# ปุ่มคำนวณ
if st.button("✅ คำนวณแยกตัวประกอบ"):
    expr_str = poly_input.replace("^", "**").replace(" ", "")
    try:
        expr = sp.sympify(expr_str, locals={'x': x})
        if expr.free_symbols != {x} and expr.free_symbols != set():
            st.error("❌ ใช้ได้เฉพาะตัวแปร x เท่านั้น")
        else:
            degree = sp.degree(expr, x)
            if degree is None or degree < 2 or degree > 10:
                st.warning("⚠️ รองรับดีกรี 2 ถึง 10 เท่านั้น")
            else:
                result = sp.factor(expr)
                st.success("✅ ผลการแยกตัวประกอบ:")
                st.code(str(result))
    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาด: {e}")
