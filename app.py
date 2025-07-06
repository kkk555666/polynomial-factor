import streamlit as st
import sympy as sp

st.set_page_config(page_title="แยกตัวประกอบพหุนาม", layout="centered")
x = sp.symbols('x')

if "poly_input" not in st.session_state:
    st.session_state.poly_input = ""

def add_text(text):
    st.session_state.poly_input += text

def backspace():
    st.session_state.poly_input = st.session_state.poly_input[:-1]

def clear_input():
    st.session_state.poly_input = ""

# CSS ปรับปุ่มให้ชิดกัน
st.markdown("""
<style>
  div.stButton > button {
    margin: 2px 2px !important;
    width: 50px !important;
  }
  div.stColumns > div {
    padding: 0px !important;
  }
</style>
""", unsafe_allow_html=True)

st.title("🧮 แยกตัวประกอบพหุนาม")
st.markdown("ใส่พหุนาม (เช่น `x^2+5*x+6`)")

# ใช้ text_input ให้ผู้ใช้พิมพ์เอง
poly_input = st.text_input("พหุนาม", value=st.session_state.poly_input)

# อัพเดต session_state เมื่อพิมพ์
if poly_input != st.session_state.poly_input:
    st.session_state.poly_input = poly_input

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

cols_list = []
for row in button_rows:
    cols = st.columns(len(row))
    cols_list.append(cols)
    for i, btn in enumerate(row):
        if cols[i].button(btn):
            if btn == '⌫':
                backspace()
            elif btn == 'ล้าง':
                clear_input()
            else:
                actual = symbol_map.get(btn, btn)
                add_text(actual)
            # อัพเดต text_input หลังกดปุ่ม
            st.session_state.poly_input = st.session_state.poly_input

if st.button("✅ คำนวณแยกตัวประกอบ"):
    expr_str = st.session_state.poly_input.replace("^", "**").replace(" ", "")
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
