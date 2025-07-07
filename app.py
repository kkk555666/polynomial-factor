import streamlit as st
import sympy as sp

st.set_page_config(page_title="แยกตัวประกอบพหุนาม", layout="centered")
x = sp.symbols('x')

if "poly_input" not in st.session_state:
    st.session_state.poly_input = ""

input_str = st.session_state.poly_input

st.title("🧮 แยกตัวประกอบพหุนาม")
st.markdown("ใส่พหุนาม เช่น `x^2 + 5*x + 6` หรือ `x^2 - 2` หรือ `2*x^2+2*x+23`")

# ปุ่มพิมพ์ลัด
button_rows = [
    ['7', '8', '9', 'บวก', 'ลบ'],
    ['4', '5', '6', 'คูณ', 'หาร'],
    ['1', '2', '3', 'x', '^'],
    ['0', '(', ')', '⌫', 'ล้าง']
]
symbol_map = {'บวก': '+', 'ลบ': '-', 'คูณ': '*', 'หาร': '/'}

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
st.code(input_str, language="plaintext")

if st.button("✅ คำนวณแยกตัวประกอบ"):
    expr_str = input_str.replace("^", "**").replace(" ", "")
    try:
        expr = sp.sympify(expr_str, locals={'x': x})
        if expr.free_symbols and expr.free_symbols != {x}:
            st.error("❌ ใช้ได้เฉพาะตัวแปร x เท่านั้น")
        else:
            degree = sp.degree(expr, x)
            if degree is None or degree < 2 or degree > 10:
                st.warning("⚠️ รองรับดีกรี 2 ถึง 10 เท่านั้น")
            else:
                factored = sp.factor(expr)
                if factored == expr:
                    # หากแยกไม่ได้แบบสมบูรณ์ ใช้รากแทน (รวม complex)
                    roots = sp.roots(expr, x, multiple=True)
                    if roots:
                        factors = []
                        for r in roots:
                            factor_str = f"(x - ({sp.simplify(r)}))"
                            factors.append(factor_str)
                        result_str = " * ".join(factors)
                        st.info("แยกตัวประกอบโดยใช้ราก (รวมรากเชิงซ้อน):")
                        st.code(result_str)
                    else:
                        st.warning("ไม่สามารถแยกตัวประกอบได้")
                else:
                    st.success("✅ ผลการแยกตัวประกอบ:")
                    st.code(str(factored))
    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาด: {e}")
