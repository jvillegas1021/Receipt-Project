import tkinter as tk
import pandas as pd
from tkinter import messagebox
from tkinter import filedialog
import xlsxwriter
import xlsxwriter.utility
from datetime import datetime
from PIL import Image, ImageTk


def submit():
    global current_question

    answer = entry.get()
    if current_question >= 2:
        try:
            value = float(answer)
            feedback_label.config(text="")
        except ValueError:
            feedback_label.config(text="Invalid input. Please enter a number.")
            return

    answers.append(answer)
    entry.delete(0, tk.END)

    current_question += 1

    if current_question == 6:
        answers.append('')
        current_question += 1

    if current_question < len(questions):
        label.config(text=questions[current_question])
    else:
        while len(answers) < len(df.columns):
            answers.append("")
        df.loc[len(df)] = answers

        again = messagebox.askyesno("New Entry", "Would you like to enter another receipt?")

        if again:
            answers.clear()
            current_question = 0
            label.config(text=questions[current_question])
            entry.delete(0, tk.END)
        else:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=f"Receipts_{datetime.now().strftime('%Y-%m-%d')}.xlsx",
                title="Save your receipt file as..."
            )
            if file_path:  # <- Only export if the user didn't cancel
                export_to_excel(file_path, df)
            root.destroy()


def end_receipt():
    while len(answers) < len(df.columns):
        answers.append("")
    df.loc[len(df)] = answers

    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        initialfile=f"Receipts_{datetime.now().strftime('%Y-%m-%d')}.xlsx",
        title="Save your receipt file as..."
    )
    if file_path:
        export_to_excel(file_path, df)
    root.destroy()

def close_exit():
    root.destroy()


def export_to_excel(file_path, df):
    # Convert data types
    numeric_columns = [
        "Subtotal (orig, pre-tax, pre-tip)",
        "Tax Amount (orig, stated)",
        "Tip Amount (orig, stated, optional)",
        "Other Charges (orig, not subject to tax)",
        "Total (orig, stated, optional)",
        "Personal / Non-Reimbursable (from subtotal, orig)",
        "Exchange Rate (target per 1 original)",
        "Eligible Subtotal",
        "Observed Tax Rate",
        "Observed Tip Rate",
        "Allowed Tax",
        "Allowed Tip (target, auto, <=20%)",
        "Other Charges",
        "Reimbursable Total",
        "Disallowed Tax",
        "Disallowed Tip"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df["Date"] = df["Date"].astype('string')
    df["Vendor"] = df["Vendor"].astype('string')

    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Receipts', index=False, startrow=0, header=True)

        workbook = writer.book
        worksheet = writer.sheets['Receipts']

        # Insert formulas row by row
        for i in range(30):
            excel_row = i + 2  # Excel rows start at 1, add 1 for header

            C = f'C{excel_row}'
            D = f'D{excel_row}'
            E = f'E{excel_row}'
            F = f'F{excel_row}'
            H = f'H{excel_row}'
            I = f'I{excel_row}'

            worksheet.write_formula(f'G{excel_row}', f'=SUM({C},{D},{E},{F})')
            worksheet.write_formula(f'J{excel_row}', f'=ROUND(MAX({C}-{H}, 0) * {I}, 2)')
            worksheet.write_formula(f'K{excel_row}', f'=IF({C}>0, {D}/{C}, 0)')
            worksheet.write_formula(f'L{excel_row}', f'=IF({C}>0, {E}/{C}, 0)')
            worksheet.write_formula(f'M{excel_row}', f'=ROUND(MIN({D}*{I}, J{excel_row}*K{excel_row}), 2)')
            worksheet.write_formula(f'N{excel_row}',
                                    f'=ROUND(MIN({E}*{I}, MIN(J{excel_row}*L{excel_row}, 0.2*J{excel_row})), 2)')
            worksheet.write_formula(f'O{excel_row}', f'=ROUND({F}*{I}, 2)')
            worksheet.write_formula(f'P{excel_row}',
                                    f'=ROUND(J{excel_row} + M{excel_row} + N{excel_row} + O{excel_row}, 2)')
            worksheet.write_formula(f'Q{excel_row}', f'=MAX({D}*{I}-M{excel_row}, 0)')
            worksheet.write_formula(f'R{excel_row}', f'=MAX({E}*{I}-N{excel_row}, 0)')

        num_rows, num_cols = df.shape

        currency_format = workbook.add_format({'num_format': '$#,##0.00', 'align': 'right'})
        percent_format = workbook.add_format({'num_format': '0.00%', 'align': 'right'})
        wrap_header_format = workbook.add_format({
            'bg_color': '#FCE4D6',
            'font_name': 'Calibri',
            'font_size': 12,
            'font_color': 'black',
            'text_wrap': True,
            'bold': True,
            'align': 'center',
            'valign': 'top'
        })

        for col_num, header in enumerate(df.columns):
            worksheet.write(0, col_num, header, wrap_header_format)

        worksheet.set_column('A:B', 20)
        worksheet.set_column('C:H', 30, currency_format)
        worksheet.set_column('I:I', 30)
        worksheet.set_column('J:J', 30, currency_format)
        worksheet.set_column('M:R', 30, currency_format)
        worksheet.set_column('K:L', 30, percent_format)
        worksheet.autofilter(0, 0, num_rows, num_cols - 1)
        worksheet.freeze_panes(1, 0)


# Initial setup
df = pd.DataFrame(columns=["Date",
                           "Vendor",
                           "Subtotal (orig, pre-tax, pre-tip)",
                           "Tax Amount (orig, stated)",
                           "Tip Amount (orig, stated, optional)",
                           "Other Charges (orig, not subject to tax)",
                           "Total (orig, stated, optional)",
                           "Personal / Non-Reimbursable (from subtotal, orig)",
                           "Exchange Rate (target per 1 original)",
                           "Eligible Subtotal",
                           "Observed Tax Rate", "Observed Tip Rate",
                           "Allowed Tax",
                           "Allowed Tip (target, auto, <=20%)",
                           "Other Charges",
                           "Reimbursable Total",
                           "Disallowed Tax",
                           "Disallowed Tip"])

answers = []  # To store user input step-by-step
questions = ["Enter Date", "Enter Vendor", "Enter the Subtotal (orig, pre-tax, pre-tip)?", "Enter the Tax Amount (orig, stated)",
             "Enter the Tip Amount (orig, stated, optional)",
             "Enter the Other Charges (orig, not subject to tax)", "",
             "Enter the Personal / Non-Reimbursable (from subtotal, orig)", " Enter Exchange Rate (target per 1 original)"]
current_question = 0

# MAIN BLOCK

root = tk.Tk()
root.title("Receipt Entry")
root.geometry("800x700")
root.configure(bg="white")

top_frame = tk.Frame(root, bg="white", width=800, height=200)
top_frame.pack(side="top", fill="x")

image = Image.open(r"C:\Users\14088\Desktop\channels4_profile.jpg").resize((200, 200))
photo = ImageTk.PhotoImage(image)
left_label = tk.Label(top_frame, image=photo, bd=0, bg="white")
left_label.pack(side="left")

image_receipt = Image.open(r"C:\Users\14088\Desktop\ply-transaction-receipt-clipart_251822-474.avif").resize((200, 200))
photo_receipt = ImageTk.PhotoImage(image_receipt)
right_label = tk.Label(top_frame, image=photo_receipt,  bd=0, bg="white")
right_label.pack(side="right")

label = tk.Label(root, text=questions[current_question], bg="white", font='Arial 20')
label.pack(pady=10)

feedback_label = tk.Label(root, text="", bg="white", fg="red")
feedback_label.pack(pady=(0, 10))

entry = tk.Entry(root, width=30, bd=1, relief="solid")
entry.pack(pady=10)
entry.bind('<Return>', lambda event: submit())

submit_button = tk.Button(root, height=2, width=20, text="Submit (Save)", command=submit)
submit_button.pack(pady=10, padx=5)

submit_button = tk.Button(root, height= 2, width=20, text="End Receipt (Save)", command=end_receipt)
submit_button.pack(pady=10, padx=5)

submit_button = tk.Button(root, height= 2, width=20, text="Close & Exit (Don't Save)", command=end_receipt)
submit_button.pack(pady=10, padx=5)


root.mainloop()