from fpdf import FPDF
import os

# Crée un dossier de stockage si nécessaire
storage_dir = "storage/NEW-1107"
os.makedirs(storage_dir, exist_ok=True)

# ---------- BANK_STATEMENT.pdf ----------
bank_pdf = FPDF()
bank_pdf.add_page()
bank_pdf.set_font("Arial", size=12)
bank_pdf.cell(0, 10, "Bank Statement", ln=True, align="C")
bank_pdf.ln(10)
bank_pdf.multi_cell(0, 10, "Salary: 3000\nExpenses: 1500\nOther transactions: ...")
bank_path = os.path.join(storage_dir, "BANK_STATEMENT.pdf")
bank_pdf.output(bank_path)
print(f"Generated {bank_path}")

bank_pdf = FPDF()
bank_pdf.add_page()
bank_pdf.set_font("Arial", size=12)
bank_pdf.cell(0, 10, "Bank Statement1", ln=True, align="C")
bank_pdf.ln(10)
bank_pdf.multi_cell(0, 10, "Salary: 5000\nExpenses: 2500\nOther transactions: ...")
bank_path = os.path.join(storage_dir, "BANK_STATEMENT1.pdf")
bank_pdf.output(bank_path)
print(f"Generated {bank_path}")


# ---------- CONTRACT.pdf ----------
contract_pdf = FPDF()
contract_pdf.add_page()
contract_pdf.set_font("Arial", size=12)
contract_pdf.cell(0, 10, "Loan Contract", ln=True, align="C")
contract_pdf.ln(10)
contract_pdf.multi_cell(0, 10, "Borrower agrees to repay the loan over 36 months.\nTerms and conditions apply.")
contract_path = os.path.join(storage_dir, "CONTRACT.pdf")
contract_pdf.output(contract_path)
print(f"Generated {contract_path}")

contract_pdf = FPDF()
contract_pdf.add_page()
contract_pdf.set_font("Arial", size=12)
contract_pdf.cell(0, 10, "Loan Contract", ln=True, align="C")
contract_pdf.ln(10)
contract_pdf.multi_cell(0, 10, "Borrower agrees to repay the loan over 24 months.\nTerms and conditions apply.")
contract_path = os.path.join(storage_dir, "CONTRACT1.pdf")
contract_pdf.output(contract_path)
print(f"Generated {contract_path}")