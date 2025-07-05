import sympy as sp
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("เครื่องมือแยกตัวประกอบพหุนาม (มีปุ่มกดช่วยพิมพ์)")
factoring-app
/
app.py
in
main


root.geometry("700x600")

x = sp.symbols('x')

def insert_text(text):
    entry.insert(tk.END, text)

def analyze_polynomial():
    expr_str = entry.get()

    try:
        expr_str_fixed = expr_str.replace("^", "**").replace(" ", "")
        expr = sp.sympify(expr_str_fixed, locals={'x': x})

        if expr.free_symbols != {x} and expr.free_symbols != set():
            messagebox.showerror("ข้อผิดพลาด", "กรุณาใช้ตัวแปร x เท่านั้น")
            return

        degree = sp.degree(expr, x)
        if degree is None or degree < 2 or degree > 10:
            messagebox.showinfo("ข้อจำกัด", "รองรับพหุนามดีกรี 2 ถึง 10 เท่านั้น")
            return

        factored_expr = sp.factor(expr)

        output_roots.delete('1.0', tk.END)
        output_roots.insert(tk.END, "ในเวอร์ชันนี้ไม่แสดงรากโดยตรง กรุณาดูผลการแยกตัวประกอบด้านล่าง\n")

        output_factors.delete('1.0', tk.END)
        output_factors.insert(tk.END, f"ผลการแยกตัวประกอบ:\n{factored_expr}")

    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {e}")

def clear_all():
    entry.delete(0, tk.END)
    output_roots.delete('1.0', tk.END)
    output_factors.delete('1.0', tk.END)

label = tk.Label(root, text="ใส่พหุนาม (เช่น x^2+5*x+6):")
label.pack(pady=10)

entry = tk.Entry(root, width=70, font=("Consolas", 14))
entry.pack(pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

buttons = [
    '7', '8', '9', '+', '-',
    '4', '5', '6', '*', '/',
    '1', '2', '3', 'x', '^',
    '0', '(', ')', ' ', '⌫'  # ปุ่มลบทีละตัว
]

def on_button_click(btn_text):
    if btn_text == '⌫':
        current_text = entry.get()
        if current_text:
            entry.delete(len(current_text)-1, tk.END)
    else:
        insert_text(btn_text)

for i, btn_text in enumerate(buttons):
    btn = tk.Button(button_frame, text=btn_text, width=5, height=2, font=("Arial", 12),
                    command=lambda bt=btn_text: on_button_click(bt))
    btn.grid(row=i//5, column=i%5, padx=3, pady=3)

frame_btn = tk.Frame(root)
frame_btn.pack(pady=10)

btn_calc = tk.Button(frame_btn, text="คำนวณแยกตัวประกอบ", command=analyze_polynomial, width=20)
btn_calc.pack(side=tk.LEFT, padx=10)

btn_clear = tk.Button(frame_btn, text="ล้างค่า", command=clear_all, width=10)
btn_clear.pack(side=tk.LEFT, padx=10)

label_root = tk.Label(root, text="หมายเหตุ:")
label_root.pack()
output_roots = tk.Text(root, height=4, width=85)
output_roots.pack(pady=5)

label_factor = tk.Label(root, text="ผลการแยกตัวประกอบ:")
label_factor.pack()
output_factors = tk.Text(root, height=8, width=85)
output_factors.pack(pady=5)

root.mainloop()
