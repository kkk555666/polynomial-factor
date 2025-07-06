import streamlit as st
import sympy as sp

# ตั้งค่าหน้า
st.set_page_config(page_title="แยกตัวประกอบพหุนาม", layout="centered")
x = sp.symbols('x')

# เก็บค่าการพิมพ์
if "poly_input" not in st.session_state:
    st.session_state.poly_input = ""

input_str = st.session_state.poly_input

st.title("🧮 แยกตัวประกอบพหุนาม")
st.markdown("ใส่พหุนาม เช่น `x^2+5*x+6`")

# ปุ่มคีย์บอร์ด
button_rows = [
    ['7', '8', '9', 'บวก', 'ลบ'],
    ['4', '5', '6', 'คูณ', 'หาร'],
    ['1', '2', '3', 'x', '^'],
    ['0', '(', ')', '⌫', 'ล้าง']
]

symbol_map = {
    'บวก': '+',
    'ลบ': '-',
    'คูณ': '*',
    'หาร': '/',
}

cols = st.columns(5)
for i, btn in enumerate(sum(button_rows, [])):
    if cols[i % 5].button(btn, key=f"btn_{btn}_{i}"):
        if btn == '⌫':
            input_str = input_str[:-1]
        elif btn == 'ล้าง':
            input_str = ""
        else:
            input_str += symbol_map.get(btn, btn)

st.session_state.poly_input = input_str

# แสดง input
st.code(input_str, language="plaintext")

# ปุ่มคำนวณ
if st.button("✅ คำนวณแยกตัวประกอบ"):
    expr_str = input_str.replace("^", "**").replace(" ", "")
    try:
        expr = sp.sympify(expr_str, locals={'x': x})
        if expr.free_symbols != {x} and expr.free_symbols != set():
            st.error("❌ ใช้ได้เฉพาะตัวแปร x เท่านั้น")
        else:
            degree = sp.degree(expr, x)
            if degree is None or degree < 2 or degree > 10:
                st.warning("⚠️ รองรับดีกรี 2 ถึง 10 เท่านั้น")
            else:
                st.success("✅ ผลการแยกตัวประกอบ:")

                # ✅ 1. แยกในจำนวนจริง (ไม่ต้องใส่ extension)
                real_factor = sp.factor(expr)
                st.markdown("**➤ แยกตัวประกอบในโดเมนจำนวนจริง (Real):**")
                st.code(str(real_factor))

                # ✅ 2. แยกในจำนวนเชิงซ้อน (Complex)
                complex_factor = sp.factor(expr, extension=[sp.I])
                st.markdown("**➤ แยกตัวประกอบในโดเมนจำนวนเชิงซ้อน (Complex):**")
                st.code(str(complex_factor))

                # ✅ 3. Quadratic form โดยใช้ราก
                roots = sp.solve(expr, x)
                if len(roots) > 0:
                    quadratic_form = 1
                    for r in roots:
                        quadratic_form *= (x - r)
                    st.markdown("**➤ แยกโดยใช้ราก (Quadratic/Complex Form):**")
                    st.code(str(sp.simplify(quadratic_form)))

    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาด: {e}")
