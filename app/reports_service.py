from fastapi import Response
from typing import Dict, Any

def get_report_bytes(report_type: str) -> tuple[bytes, str, str]:
    """
    Returns CSV/Excel bytes, media type, and suggested filename for statutory banking reports.
    """
    headers = "Report_ID,Customer_ID,Account_No,Amount_INR,Status,Risk_Score,Date,Branch\n"
    sample_row = "REP001,CUST8921,AC9928172,1500000,FLAGGED,92,2026-11-20,MUMBAI-MAIN\n"
    content = (headers + sample_row * 10).encode("utf-8")
    
    mapping = {
        "master_excel": ("MASTER_CONSOLIDATED_BANKING_EXECUTIVE.csv", "text/csv"),
        "aml_fiu_ind": ("AML_FIU_IND_STATUTORY_REPORTS.csv", "text/csv"),
        "credit_card_risk": ("CREDIT_CARD_RISK_PORTFOLIO.csv", "text/csv"),
        "alm_liquidity": ("ALM_LIQUIDITY_BASEL3.csv", "text/csv"),
        "loans_microfinance": ("LOANS_MICROFINANCE_JLG.csv", "text/csv")
    }
    
    filename, media_type = mapping.get(report_type, (f"{report_type.upper()}_REPORT.csv", "text/csv"))
    return content, media_type, filename
