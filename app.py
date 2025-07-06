import streamlit as st
import sympy as sp

st.set_page_config(page_title="แยกตัวประกอบพหุนาม", layout="centered")
x = sp.symbols('x')

# เริ่มต้นค่า input ใน session state
if "poly_input" not in st.session_state:
    st.session_state.poly_input = ""

# ฟังก์ชันแก้ไข input รับค่าปัจจุบันแล้วคืนค่าใหม่
def backspace(s):
    return s[:-1]

def clear_input(s):
    return ""

def add_text(s, t):
    return s + t

st.title("🧮 แยกตัวประกอบพหุนาม")
st.markdown("ใส่พหุนาม (เช่น `x^2+5*x+6`)")

# ตัวแปรกลางเก็บค่า input ชั่วคราว
input_str = st.session_state.poly_input

# แสดงช่อง input (text_input) พร้อม value จาก input_str
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

# สร้างปุ่มและตรวจสอบการกด
for row in button_rows:
    cols = st.columns(len(row))
    for i, btn in enumerate(row):
        if cols[i].button(btn, key=f"{btn}_{i}"):
            if btn == '⌫':
                input_str = backspace(input_str)
            elif btn == 'ล้าง':
                input_str = clear_input(input_str)
            else:
                actual = symbol_map.get(btn, btn)
                input_str = add_text(input_str, actual)

# อัปเดต session_state ด้วยค่า input_str ที่แก้ไขแล้ว
st.session_state.poly_input = input_str

# แสดงข้อความ input ปัจจุบัน
st.code(st.session_state.poly_input, language="plaintext")

# ปุ่มคำนวณแยกตัวประกอบ
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

