from pypdf import PdfReader
import re
from src.core.state import LoanData


def extract_loan_data_from_pdf(pdf_path: str) -> LoanData:

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    # -----------------------
    # Simple regex extraction
    # -----------------------

    industry = re.search(r"Industry:\s*(.*)", text)
    revenue = re.search(r"Revenue Growth.*?(\d+)", text)
    dscr = re.search(r"DSCR.*?([\d.]+)", text)
    debt = re.search(r"Debt to Equity.*?([\d.]+)", text)
    collateral = re.search(r"Collateral Value.*?([\d,]+)", text)
    offshore = re.search(r"Offshore Deposits.*?([\d,]+)", text)

    loan = LoanData(

        industry=industry.group(1) if industry else "Unknown",

        revenue_growth=float(revenue.group(1)) / 100 if revenue else 0.1,

        dscr=float(dscr.group(1)) if dscr else 1.0,

        debt_to_equity=float(debt.group(1)) if debt else 1.5,

        collateral_value=float(collateral.group(1).replace(",", "")) if collateral else None,

        offshore_deposit=float(offshore.group(1).replace(",", "")) if offshore else 0,

        director_grey_list=False,

        aml_flag=False,
    )

    return loan