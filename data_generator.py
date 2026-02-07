"""
Enhanced Data Generator for OmniSight-AI
Now with 6 domains, realistic patterns, and demo scenarios built-in
"""

import random
from datetime import datetime, timedelta

def get_financial_data():
    """Financial transactions with trends and patterns"""
    base_date = datetime.now()
    transactions = []
    
    # Recent revenue decline pattern (for demo)
    for i in range(30):
        date = base_date - timedelta(days=i)
        
        # Revenue declining in recent days (competitive pressure)
        base_amount = 25000
        if i < 7:  # Last week - decline
            base_amount *= 0.85  # 15% drop
        
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
    
    return transactions[:50]  # Return recent 50 transactions


def get_operations_data():
    """Operations with performance degradation pattern"""
    base_date = datetime.now()
    operations = []
    
    for i in range(7):  # Last 7 days
        date = base_date - timedelta(days=i)
        
        # Recent performance degradation (for demo)
        if i < 3:  # Last 3 days
            success_rate = 0.972  # Below 99% SLA
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
            "capacity_utilization": 0.87 if i < 5 else 0.75,  # High capacity
            "status": status
        })
    
    return operations


def get_partner_data():
    """Partners with quality decline in specific region"""
    partners = [
        {
            "partner_id": "P001",
            "partner_name": "XYZ Logistics",
            "partner_type": "Supplier",
            "reliability": "High",
            "region": "North America",
            "quality_score": 0.95,
            "delivery_success": 0.98,
            "cost_efficiency": 0.92,
            "relationship_health": 0.90,
            "monthly_volume": 50000,
            "commission_rate": 0.12
        },
        {
            "partner_id": "P002",
            "partner_name": "MegaRaw Materials",
            "partner_type": "Supplier",
            "reliability": "Medium",
            "region": "APAC",
            "quality_score": 0.72,  # Declined (competitor offered better commission)
            "delivery_success": 0.85,
            "cost_efficiency": 0.88,
            "relationship_health": 0.65,  # At risk!
            "monthly_volume": 35000,
            "commission_rate": 0.12,
            "notes": "Quality declined 12% last week - investigating"
        },
        {
            "partner_id": "P003",
            "partner_name": "Alpha Distributors",
            "partner_type": "Distributor",
            "reliability": "High",
            "region": "EMEA",
            "quality_score": 0.93,
            "delivery_success": 0.96,
            "cost_efficiency": 0.90,
            "relationship_health": 0.88,
            "monthly_volume": 42000,
            "commission_rate": 0.15
        },
        {
            "partner_id": "P004",
            "partner_name": "Pacific Partners",
            "partner_type": "Supplier",
            "reliability": "Medium",
            "region": "APAC",
            "quality_score": 0.68,  # Also declined
            "delivery_success": 0.82,
            "cost_efficiency": 0.85,
            "relationship_health": 0.62,  # At risk!
            "monthly_volume": 28000,
            "commission_rate": 0.12,
            "notes": "Shifted focus to competitor offers"
        }
    ]
    
    return partners


def get_client_data():
    """Clients with acquisition cost and churn risk data"""
    clients = [
        {
            "client_id": "C001",
            "client_name": "ABC Manufacturing",
            "industry": "Manufacturing",
            "contact_person": "Ahmad Zaki",
            "email": "ahmad@abc.com.my",
            "status": "Active",
            "region": "APAC",
            "acquisition_cost": 312,  # Increased from usual $245
            "lifetime_value": 25000,
            "churn_risk": 0.15,
            "engagement_score": 0.85,
            "monthly_revenue": 2500
        },
        {
            "client_id": "C002",
            "client_name": "GreenTech Solution",
            "industry": "Technology",
            "contact_person": "Nur Aina",
            "email": "aina@greentech.com.my",
            "status": "Active",
            "region": "APAC",
            "acquisition_cost": 298,  # Also high
            "lifetime_value": 18500,
            "churn_risk": 0.22,  # Higher risk
            "engagement_score": 0.72,
            "monthly_revenue": 1850
        },
        {
            "client_id": "C003",
            "client_name": "FreshMart Retail",
            "industry": "Retail",
            "contact_person": "Daniel Lee",
            "email": "daniel@freshmart.com.my",
            "status": "At Risk",
            "region": "APAC",
            "acquisition_cost": 325,
            "lifetime_value": 12000,
            "churn_risk": 0.45,  # High risk!
            "engagement_score": 0.58,
            "monthly_revenue": 1200
        },
        {
            "client_id": "C004",
            "client_name": "TechCorp Global",
            "industry": "Technology",
            "contact_person": "Sarah Chen",
            "email": "sarah@techcorp.com",
            "status": "Active",
            "region": "North America",
            "acquisition_cost": 245,  # Normal
            "lifetime_value": 35000,
            "churn_risk": 0.08,
            "engagement_score": 0.92,
            "monthly_revenue": 3500
        },
        {
            "client_id": "C005",
            "client_name": "Euro Solutions",
            "industry": "Consulting",
            "contact_person": "Klaus Mueller",
            "email": "klaus@eurosol.de",
            "status": "Active",
            "region": "EMEA",
            "acquisition_cost": 260,
            "lifetime_value": 28000,
            "churn_risk": 0.12,
            "engagement_score": 0.88,
            "monthly_revenue": 2800
        }
    ]
    
    return clients


def get_competitive_data():
    """NEW: Competitive intelligence data"""
    base_date = datetime.now()
    
    competitive_intel = [
        {
            "competitor_id": "COMP001",
            "competitor_name": "Competitor A",
            "market_share": 0.28,
            "pricing_change": -0.15,  # 15% price drop!
            "pricing_change_date": (base_date - timedelta(days=3)).strftime("%Y-%m-%d"),
            "region": "APAC",
            "our_win_rate": 0.38,  # Down from 0.45
            "notes": "Aggressive pricing campaign launched 3 days ago",
            "threat_level": "High"
        },
        {
            "competitor_id": "COMP002",
            "competitor_name": "Competitor B",
            "market_share": 0.22,
            "pricing_change": 0.0,
            "region": "Global",
            "our_win_rate": 0.52,
            "threat_level": "Medium"
        },
        {
            "competitor_id": "COMP003",
            "competitor_name": "Competitor C",
            "market_share": 0.18,
            "pricing_change": 0.05,
            "region": "EMEA",
            "our_win_rate": 0.61,
            "threat_level": "Low"
        }
    ]
    
    return competitive_intel


def get_compliance_data():
    """NEW: Compliance and risk data"""
    compliance_status = [
        {
            "domain": "Financial",
            "risk_level": "Low",
            "compliance_score": 0.95,
            "last_audit": "2024-01-15",
            "issues": 0
        },
        {
            "domain": "Operations",
            "risk_level": "Medium",
            "compliance_score": 0.87,
            "last_audit": "2024-02-01",
            "issues": 2,
            "notes": "Capacity utilization approaching regulatory limits"
        },
        {
            "domain": "Partner Management",
            "risk_level": "Medium",
            "compliance_score": 0.82,
            "last_audit": "2024-01-20",
            "issues": 1,
            "notes": "Partner concentration risk in APAC region"
        },
        {
            "domain": "Client Data",
            "risk_level": "Low",
            "compliance_score": 0.93,
            "last_audit": "2024-02-05",
            "issues": 0
        }
    ]
    
    return compliance_status


def get_aggregated_metrics():
    """Calculate high-level metrics for dashboard"""
    financial = get_financial_data()
    operations = get_operations_data()
    partners = get_partner_data()
    clients = get_client_data()
    competitive = get_competitive_data()
    
    # Financial metrics
    recent_revenue = sum(t['amount'] for t in financial[:7] if t['type'] == 'Income')
    previous_revenue = sum(t['amount'] for t in financial[7:14] if t['type'] == 'Income')
    revenue_change = ((recent_revenue - previous_revenue) / previous_revenue) * 100 if previous_revenue > 0 else 0
    
    # Client metrics
    avg_cac_apac = sum(c['acquisition_cost'] for c in clients if c['region'] == 'APAC') / len([c for c in clients if c['region'] == 'APAC'])
    high_churn_risk = len([c for c in clients if c['churn_risk'] > 0.25])
    
    # Partner metrics
    apac_partners = [p for p in partners if p['region'] == 'APAC']
    avg_partner_quality_apac = sum(p['quality_score'] for p in apac_partners) / len(apac_partners) if apac_partners else 0
    at_risk_partners = len([p for p in partners if p['relationship_health'] < 0.75])
    
    # Operations metrics
    avg_success_rate = sum(o['success_rate'] for o in operations) / len(operations)
    avg_capacity = sum(o['capacity_utilization'] for o in operations) / len(operations)
    
    return {
        'revenue_change_pct': revenue_change,
        'avg_cac_apac': avg_cac_apac,
        'high_churn_risk_count': high_churn_risk,
        'avg_partner_quality_apac': avg_partner_quality_apac,
        'at_risk_partners': at_risk_partners,
        'avg_success_rate': avg_success_rate,
        'avg_capacity_utilization': avg_capacity,
        'competitive_threats': len([c for c in competitive if c['threat_level'] == 'High'])
    }


# Backward compatibility - keep your original functions working
def get_operations_data_simple():
    """Original simple version for backward compatibility"""
    return [
        {
            "operation_id": "O001",
            "operation_type": "Production",
            "output_per_day": 500,
            "staff_involved": 12,
            "cost": 8000,
            "status": "Active"
        },
        {
            "operation_id": "O002",
            "operation_type": "Packaging",
            "output_per_day": 450,
            "staff_involved": 8,
            "cost": 3500,
            "status": "Active"
        },
        {
            "operation_id": "O003",
            "operation_type": "Maintenance",
            "output_per_day": 0,
            "staff_involved": 4,
            "cost": 2000,
            "status": "Closed"
        }
    ]