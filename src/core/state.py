from typing import TypedDict, List


class LoanData(TypedDict):
    industry: str
    revenue_growth: float
    dscr: float
    debt_to_equity: float
    collateral_value: float
    offshore_deposit: float
    director_grey_list: bool
    aml_flag: bool


class WarRoomState(TypedDict):
    loan_data: LoanData
    sales_opinion: str
    risk_opinion: str
    compliance_opinion: str
    flags: List[str]
    veto: bool
    turn_count: int
    final_decision: str
    risk_score: int