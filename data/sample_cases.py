from src.core.state import LoanData

# Input A – High growth tech startup (Sales vs Risk test)
input_a = LoanData(
    industry="Tech SaaS",
    revenue_growth=40,
    dscr=1.1,
    debt_to_equity=2.8,
    collateral_value=0,
    offshore_deposit=0,
    director_grey_list=False,
    aml_flag=False
)

# Input B – Manufacturing firm with compliance issue (Compliance veto test)
input_b = LoanData(
    industry="Manufacturing",
    revenue_growth=8,
    dscr=1.4,
    debt_to_equity=1.8,
    collateral_value=10000000,
    offshore_deposit=1000000,
    director_grey_list=True,
    aml_flag=True
)