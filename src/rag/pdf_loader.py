from pypdf import PdfReader
from src.core.llm import get_llm
from src.core.state import LoanData

import json
import re


def extract_loan_data_from_pdf(pdf_path: str) -> LoanData:

    # -------------------------
    # 1. Read PDF
    # -------------------------
    reader = PdfReader(pdf_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    document_text = "\n\n".join(pages)

    if not document_text.strip():
        raise ValueError("Could not extract text from PDF.")

    # -------------------------
    # 2. Limit context size
    # -------------------------
    # Prevent sending an extremely large PDF to the LLM.
    max_chars = 30000
    document_text = document_text[:max_chars]

    # -------------------------
    # 3. LLM
    # -------------------------
    llm = get_llm()

    # -------------------------
    # 4. Prompt
    # -------------------------
    prompt = f"""
You are a financial document extraction system.

Extract the following financial fields from the loan document.

Return ONLY valid JSON.

Fields:

- industry (string)
- revenue_growth (decimal like 0.40 for 40%)
- dscr (number)
- debt_to_equity (number)
- collateral_value (number)
- offshore_deposit (number)

If a field cannot be found, use a reasonable default:
- industry: "Unknown"
- revenue_growth: 0.1
- dscr: 1.0
- debt_to_equity: 1.5
- collateral_value: 0
- offshore_deposit: 0

Loan Document:

{document_text}
"""

    # -------------------------
    # 5. LLM Extraction
    # -------------------------
    response = llm.invoke(prompt)

    text = response.content

    # -------------------------
    # 6. Extract JSON
    # -------------------------
    json_match = re.search(r"\{.*\}", text, re.DOTALL)

    if not json_match:
        raise ValueError(
            "LLM did not return valid JSON."
        )

    try:
        data = json.loads(json_match.group())
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Could not parse LLM JSON response: {e}"
        )

    # -------------------------
    # 7. Convert to LoanData
    # -------------------------
    loan_data = LoanData(

        industry=str(
            data.get("industry", "Unknown")
        ),

        revenue_growth=float(
            data.get("revenue_growth", 0.1)
        ),

        dscr=float(
            data.get("dscr", 1.0)
        ),

        debt_to_equity=float(
            data.get("debt_to_equity", 1.5)
        ),

        collateral_value=float(
            data.get("collateral_value", 0)
        ),

        offshore_deposit=float(
            data.get("offshore_deposit", 0)
        ),

        director_grey_list=False,

        aml_flag=False,
    )

    return loan_data