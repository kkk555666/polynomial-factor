import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="แยกตัวประกอบพหุนาม", layout="centered")
x = sp.symbols('x')

if "poly_input" not in st.session_state:
    st.session_state.poly_input = ""

input_str = st.session_state.poly_input

st.title("🧮 แยกตัวประกอบพหุนาม")
st.markdown("ใส่พหุนาม (เช่น x^2+5*x+6)")

# ปุ่มกดตัวเลข
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

if st.button("✅ คำนวณแยกตัวประกอบ"):
    expr_str = input_str.replace("^", "**").replace(" ", "")
    try:
        expr = sp.sympify(expr_str, locals={'x': x})

        # ตรวจสอบว่าใช้แค่ x
        if expr.free_symbols != {x} and expr.free_symbols != set():
            st.error("❌ ใช้ได้เฉพาะตัวแปร x เท่านั้น")
        else:
            degree = sp.degree(expr, x)
            if degree is None or degree < 2 or degree > 4:
                st.warning("⚠️ รองรับดีกรี 2 ถึง 4 เท่านั้น")
            else:
                # factor
                result = sp.factor(expr)
                if result != expr:
                    st.success("✅ ผลการแยกตัวประกอบ:")
                    st.code(str(result))
                else:
                    st.warning("⚠️ ไม่สามารถแยกตัวประกอบเชิงสัญลักษณ์ได้ (จะแสดงรากแทน)")

                # หา root (real + complex)
                roots = sp.nroots(expr)  # คำนวณเชิงตัวเลข
                if roots:
                    roots_str = []
                    for r in roots:
                        if abs(r.as_real_imag()[1]) < 1e-8:  # ถ้าเป็น real
                            roots_str.append(f"{float(r):.6f}")
                        else:
                            roots_str.append(str(r))
                    st.info("📌 รากของสมการ: " + ", ".join(roots_str))
                else:
                    st.warning("⚠ ไม่มีราก")

                # === กราฟ f(x) ===
                st.subheader("📈 กราฟของ f(x)")
                X = np.linspace(-10, 10, 400)
                f_lambd = sp.lambdify(x, expr, 'numpy')
                Y = f_lambd(X)

                fig, ax = plt.subplots()
                ax.axhline(0, color='black', linewidth=1)
                ax.axvline(0, color='black', linewidth=1)
                ax.plot(X, Y, label=f"f(x) = {expr}", color='blue')

                # จุดรากจริง
                real_roots = [float(r.evalf()) for r in roots if abs(sp.im(r)) < 1e-8]
                ax.scatter(real_roots, [0]*len(real_roots), color='red', zorder=5, label="รากจริง")

                ax.legend()
                ax.grid(True)
                st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาด: {e}")

