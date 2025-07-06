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
                
                # 1. แยกแบบจำนวนจริง (Real)
                real_factor = sp.factor(expr, extension=False)
                st.markdown("**➤ แยกตัวประกอบในโดเมนจำนวนจริง (Real):**")
                st.code(str(real_factor))

                # 2. แยกแบบจำนวนเชิงซ้อน (Complex)
                complex_factor = sp.factor(expr, extension=sp.I)
                st.markdown("**➤ แยกตัวประกอบในโดเมนจำนวนเชิงซ้อน (Complex):**")
                st.code(str(complex_factor))

                # 3. แสดงรากแบบ Quadratic (เมื่อ factor ไม่ได้เพิ่ม)
                roots = sp.solve(expr, x)
                if len(roots) > 0:
                    quadratic_form = 1
                    for r in roots:
                        quadratic_form *= (x - r)
                    st.markdown("**➤ แยกตัวประกอบโดยแสดงราก (อาจเป็น Quadratic Complex Form):**")
                    st.code(str(sp.simplify(quadratic_form)))
    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาด: {e}")
