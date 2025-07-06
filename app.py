
import streamlit as st
import sympy as sp

st.set_page_config(page_title="แยกตัวประกอบพหุนาม", layout="centered")
x = sp.symbols('x')

if "poly_input" not in st.session_state:
    st.session_state.poly_input = ""

# เก็บค่าชั่วคราวเพื่อแก้ไข input
input_str = st.session_state.poly_input

def backspace():
    nonlocal input_str  # ถ้าอยู่ในฟังก์ชัน แต่ถ้าไม่ใช้ ให้ประกาศเป็น global หรืออื่น ๆ
    return input_str[:-1]

def clear_input():
    return ""

def add_text(t, s):
    return s + t

st.title("🧮 แยกตัวประกอบพหุนาม")
st.markdown("ใส่พหุนาม (เช่น `x^2+5*x+6`)")

# แสดงช่อง input และรับค่าจากผู้ใช้
input_str = st.text_input("พหุนาม", value=input_str, key="text_display")

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

cols = None
for row in button_rows:
    cols = st.columns(len(row))
    for i, btn in enumerate(row):
        if cols[i].button(btn):
            if btn == '⌫':
                input_str = input_str[:-1]
            elif btn == 'ล้าง':
                input_str = ""
            else:
                actual = symbol_map.get(btn, btn)
                input_str += actual

# อัปเดตค่า session_state จาก input_str หลังจากแก้ไขปุ่มแล้ว
st.session_state.poly_input = input_str

# แสดงข้อความ input อัปเดต
st.code(st.session_state.poly_input, language="plaintext")

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

