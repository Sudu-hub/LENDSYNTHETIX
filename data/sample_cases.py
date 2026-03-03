from src.core.state import LoanData

input_a = LoanData(
    industry="Tech SaaS",
    revenue_growth=0.40,   # 40%
    dscr=1.1,
    debt_to_equity=2.8,
    collateral_value=0,
    offshore_deposit=0,
    director_grey_list=False,
    aml_flag=False
)

input_b = LoanData(
    industry="Manufacturing",
    revenue_growth=0.08,   # 8%
    dscr=1.4,
    debt_to_equity=1.8,
    collateral_value=10000000,
    offshore_deposit=1000000,
    director_grey_list=True,
    aml_flag=True
)