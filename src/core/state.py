# src/core/state.py

from typing import TypedDict, List, Optional, Literal
from pydantic import BaseModel, Field


# ---------------------------
# Loan Input Model
# ---------------------------

class LoanData(BaseModel):
    industry: str

    revenue_growth: float = Field(
        ..., ge=0, le=1,
        description="YoY revenue growth as decimal (0.40 = 40%)"
    )

    dscr: float = Field(
        ..., gt=0,
        description="Debt Service Coverage Ratio"
    )

    debt_to_equity: float = Field(
        ..., ge=0,
        description="Debt-to-equity ratio"
    )

    collateral_value: Optional[float] = Field(
        default=None,
        ge=0,
        description="Collateral value in INR; None means unsecured loan"
    )

    offshore_deposit: float = Field(
        default=0.0,
        ge=0,
        description="Offshore deposits in INR (0 if none)"
    )

    director_grey_list: bool = Field(
        default=False,
        description="Director appears on grey watchlist"
    )

    aml_flag: bool = Field(
        default=False,
        description="AML red flag detected"
    )


# ---------------------------
# War Room State
# ---------------------------

class WarRoomState(TypedDict):
    loan_data: LoanData

    sales_opinion: Optional[str]
    risk_opinion: Optional[str]
    compliance_opinion: Optional[str]

    flags: List[str]
    veto: bool
    turn_count: int

    risk_score: Optional[int]
    final_decision: Optional[Literal["approve", "reject", "review"]]
    decision_summary: Optional[str]

    debate_round: int
    max_rounds: int
    consensus_reached: bool