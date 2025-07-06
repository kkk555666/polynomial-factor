import streamlit as st
import sympy as sp

st.set_page_config(page_title="แยกตัวประกอบพหุนาม", layout="centered")
x = sp.symbols('x')

# ใส่ CSS ให้ปุ่มอยู่ชิดกันในมือถือ
st.markdown("""
<style>
  div.stButton > button {
    margin: 2px !important;
    min-width: 50px !important;
  }
  div[data-testid="column"] {
    padding: 2px !important;
  }
</style>
""", unsafe_allow_html=True)

# เก็บ input ไว้ใน session_state
if "poly_input" not in st.session_state:
    st.session_state.poly_input = ""

def update_input(new_text):
    st.session_state.poly_input = new_text

def add_text(t):
    st.session_state.poly_input += t

def backspace():
    st.session_state.poly_input = st.session_state.poly_input[:-1]

def clear_input():
    st.session_state.poly_input = ""

st.title("🧮 แยกตัวประกอบพหุนาม")
st.markdown("ใส่พหุนาม (เช่น `x^2+5*x+6`)")

# กล่อง input ผูกกับ session_state โดยตรง
st.text_input("พหุนาม", key="poly_input", label_visibility="collapsed")

# ปุ่มกด
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

for row in button_rows:
    cols = st.columns(len(row))
    for i, btn in enumerate(row):
        if cols[i].button(btn, key=f"{btn}_{i}"):
            if btn == '⌫':
                backspace()
            elif btn == 'ล้าง':
                clear_input()
            else:
                actual = symbol_map.get(btn, btn)
                add_text(actual)

# ปุ่มคำนวณ
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
