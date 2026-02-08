
import random
from datetime import datetime, timedelta

def get_financial_data():
    base_date = datetime.now()
    transactions = []
    for i in range(30):
        date = base_date - timedelta(days=i)
        base_amount = 25000
        if i < 7: base_amount *= 0.85
        
        transactions.extend([
            {
                "transaction_id": f"F{i*3+1:03d}",
                "client_id": f"C{random.randint(1,5):03d}",
                "type": "Income",
                "amount": base_amount * random.uniform(0.9, 1.1),
                "status": "Paid" if random.random() > 0.2 else "Unpaid",
                "region": random.choice(["North America", "EMEA", "APAC", "LATAM"]),
                "date": date.strftime("%Y-%m-%d")
            },
            {
                "transaction_id": f"F{i*3+2:03d}",
                "client_id": f"C{random.randint(1,5):03d}",
                "type": "Income",
                "amount": 18500 * random.uniform(0.9, 1.1),
                "status": "Paid",
                "region": random.choice(["North America", "EMEA", "APAC", "LATAM"]),
                "date": date.strftime("%Y-%m-%d")
            },
            {
                "transaction_id": f"F{i*3+3:03d}",
                "client_id": "OPERATIONAL",
                "type": "Expense",
                "amount": 6200 * random.uniform(0.9, 1.1),
                "status": "Paid",
                "region": "Global",
                "date": date.strftime("%Y-%m-%d")
            }
        ])
    return transactions[:50]

def get_operations_data():
    base_date = datetime.now()
    operations = []
    for i in range(7):
        date = base_date - timedelta(days=i)
        if i < 3:
            success_rate = 0.972
            status = "Degraded"
        else:
            success_rate = 0.995
            status = "Active"
        
        operations.append({
            "operation_id": f"O{i+1:03d}",
            "date": date.strftime("%Y-%m-%d"),
            "operation_type": "Production",
            "output_per_day": int(500 * success_rate),
            "staff_involved": 12,
            "cost": 8000,
            "success_rate": success_rate,
            "error_count": int((1 - success_rate) * 100),
            "capacity_utilization": 0.87 if i < 5 else 0.75,
            "status": status
        })
    return operations

def get_partner_data():
    return [
        {"partner_id": "P001", "partner_name": "XYZ Logistics", "partner_type": "Supplier", "reliability": "High", "region": "North America", "quality_score": 0.95, "delivery_success": 0.98, "cost_efficiency": 0.92, "relationship_health": 0.90, "monthly_volume": 50000, "commission_rate": 0.12},
        {"partner_id": "P002", "partner_name": "MegaRaw Materials", "partner_type": "Supplier", "reliability": "Medium", "region": "APAC", "quality_score": 0.72, "delivery_success": 0.85, "cost_efficiency": 0.88, "relationship_health": 0.65, "monthly_volume": 35000, "commission_rate": 0.12, "notes": "Quality declined 12% last week"},
        {"partner_id": "P003", "partner_name": "Alpha Distributors", "partner_type": "Distributor", "reliability": "High", "region": "EMEA", "quality_score": 0.93, "delivery_success": 0.96, "cost_efficiency": 0.90, "relationship_health": 0.88, "monthly_volume": 42000, "commission_rate": 0.15},
        {"partner_id": "P004", "partner_name": "Pacific Partners", "partner_type": "Supplier", "reliability": "Medium", "region": "APAC", "quality_score": 0.68, "delivery_success": 0.82, "cost_efficiency": 0.85, "relationship_health": 0.62, "monthly_volume": 28000, "commission_rate": 0.12, "notes": "Shifted focus to competitor offers"}
    ]

def get_client_data():
    return [
        {"client_id": "C001", "client_name": "ABC Manufacturing", "industry": "Manufacturing", "status": "Active", "region": "APAC", "acquisition_cost": 312, "lifetime_value": 25000, "churn_risk": 0.15},
        {"client_id": "C002", "client_name": "GreenTech Solution", "industry": "Technology", "status": "Active", "region": "APAC", "acquisition_cost": 298, "lifetime_value": 18500, "churn_risk": 0.22},
        {"client_id": "C003", "client_name": "FreshMart Retail", "industry": "Retail", "status": "At Risk", "region": "APAC", "acquisition_cost": 325, "lifetime_value": 12000, "churn_risk": 0.45},
        {"client_id": "C004", "client_name": "TechCorp Global", "industry": "Technology", "status": "Active", "region": "North America", "acquisition_cost": 245, "lifetime_value": 35000, "churn_risk": 0.08},
        {"client_id": "C005", "client_name": "Euro Solutions", "industry": "Consulting", "status": "Active", "region": "EMEA", "acquisition_cost": 260, "lifetime_value": 28000, "churn_risk": 0.12}
    ]

def get_competitive_data():
    base_date = datetime.now()
    return [
        {"competitor_id": "COMP001", "competitor_name": "Competitor A", "market_share": 0.28, "pricing_change": -0.15, "pricing_change_date": (base_date - timedelta(days=3)).strftime("%Y-%m-%d"), "region": "APAC", "our_win_rate": 0.38, "notes": "Aggressive pricing campaign", "threat_level": "High"},
        {"competitor_id": "COMP002", "competitor_name": "Competitor B", "market_share": 0.22, "pricing_change": 0.0, "region": "Global", "our_win_rate": 0.52, "threat_level": "Medium"},
        {"competitor_id": "COMP003", "competitor_name": "Competitor C", "market_share": 0.18, "pricing_change": 0.05, "region": "EMEA", "our_win_rate": 0.61, "threat_level": "Low"}
    ]

def get_compliance_data():
    return [
        {"domain": "Financial", "risk_level": "Low", "compliance_score": 0.95, "issues": 0},
        {"domain": "Operations", "risk_level": "Medium", "compliance_score": 0.87, "issues": 2, "notes": "Capacity limits"},
        {"domain": "Partner Management", "risk_level": "Medium", "compliance_score": 0.82, "issues": 1, "notes": "Partner concentration risk"},
        {"domain": "Client Data", "risk_level": "Low", "compliance_score": 0.93, "issues": 0}
    ]
def generate_full_dataset():
    """
    Returns the full OmniSight dataset in a single dict.
    This is the contract the UI + AI engine expects.
    """
    return {
        "finance": get_financial_data(),
        "operations": get_operations_data(),
        "partners": get_partner_data(),
        "clients": get_client_data(),
        "competitive": get_competitive_data(),
        "compliance": get_compliance_data(),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

generate_data = generate_full_dataset
