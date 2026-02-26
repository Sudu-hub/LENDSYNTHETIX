from typing import TypedDict, List, Dict

class WarRoomState(TypedDict):
    load_data: Dict
    sales_opinion: str
    risk_opinion: str
    compliance_opinion: str
    flags: List[str]
    veto: bool
    turn_count: int
    final_decision: str