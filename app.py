import streamlit as st
import sympy as sp

st.set_page_config(page_title="แยกตัวประกอบพหุนาม & หาร", layout="centered")
x = sp.symbols('x')

if "poly_input" not in st.session_state:
    st.session_state.poly_input = ""

input_str = st.session_state.poly_input

st.title("🧮 แยกตัวประกอบพหุนาม & หาร")
st.markdown("ใส่พหุนาม (เช่น `x^3+5*x^2+6*x+1`) และเลือกฟังก์ชัน")

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
            input_str = input_str[:-1] if input_str else ""
        elif btn == 'ล้าง':
            input_str = ""
        else:
            input_str += symbol_map.get(btn, btn)

st.session_state.poly_input = input_str
st.code(input_str, language="plaintext")

st.markdown("---")

# เลือกฟังก์ชัน
operation = st.radio("เลือกการทำงาน", ("แยกตัวประกอบ", "หารพหุนาม"))

expr_str = input_str.replace("^", "**").replace(" ", "")

try:
    expr = sp.sympify(expr_str, locals={'x': x})
    if expr.free_symbols != {x} and expr.free_symbols != set():
        st.error("❌ ใช้ได้เฉพาะตัวแปร x เท่านั้น")
    else:
        degree = sp.degree(expr, x)
        if degree is None or degree < 1 or degree > 10:
            st.warning("⚠️ รองรับดีกรี 1 ถึง 10 เท่านั้น")
        else:
            if operation == "แยกตัวประกอบ":
                result = sp.factor(expr)
                st.success("✅ ผลการแยกตัวประกอบ:")
                st.code(str(result))
            else:
                st.markdown("**กรุณาใส่พหุนามตัวตั้ง (Dividend) และตัวหาร (Divisor)**")
                
                dividend_str = st.text_input("พหุนามตัวตั้ง (Dividend)", value=expr_str, key="dividend")
                divisor_str = st.text_input("พหุนามตัวหาร (Divisor)", value="x+1", key="divisor")
                
                try:
                    dividend = sp.sympify(dividend_str.replace("^", "**"), locals={'x': x})
                    divisor = sp.sympify(divisor_str.replace("^", "**"), locals={'x': x})

                    # ตรวจสอบตัวแปร
                    if (dividend.free_symbols - {x}) or (divisor.free_symbols - {x}):
                        st.error("❌ ตัวแปรที่ใช้ได้ต้องเป็น x เท่านั้น")
                    else:
                        q, r = sp.div(dividend, divisor, domain='QQ')
                        st.success("✅ ผลหารพหุนาม:")
                        st.write(f"ตัวตั้ง: {dividend}")
                        st.write(f"ตัวหาร: {divisor}")
                        st.write(f"ผลหาร (Quotient): {q}")
                        st.write(f"เศษ (Remainder): {r}")

                        # แสดงในรูปเศษส่วน (Quotient + Remainder/Divisor)
                        if r != 0:
                            fraction_expr = q + r / divisor
                            fraction_simplified = sp.simplify(fraction_expr)
                            st.info("ผลลัพธ์ในรูปเศษส่วน:")
                            st.latex(sp.latex(fraction_simplified))
                        else:
                            st.info("หารลงตัว ไม่มีเศษเหลือ")
                except Exception as e:
                    st.error(f"❌ เกิดข้อผิดพลาดในการประมวลผล: {e}")

except Exception as e:
    st.error(f"❌ เกิดข้อผิดพลาด: {e}")
