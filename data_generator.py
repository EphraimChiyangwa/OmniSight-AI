def get_operations_data():
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

def get_partner_data():
    return [
        {
            "partner_id": "P001",
            "partner_name": "XYZ Logistics",
            "partner_type": "Supplier",
            "reliability": "High"
        },
        {
            "partner_id": "P002",
            "partner_name": "MegaRaw Materials",
            "partner_type": "Supplier",
            "reliability": "Medium"
        },
        {
            "partner_id": "P003",
            "partner_name": "Alpha Distributors",
            "partner_type": "Distributor",
            "reliability": "High"
        }
    ]


def get_financial_data():
    return [
        {
            "transaction_id": "F001",
            "client_id": "C001",
            "type": "Income",
            "amount": 25000,
            "status": "Paid"
        },
        {
            "transaction_id": "F002",
            "client_id": "C002",
            "type": "Income",
            "amount": 18500,
            "status": "Unpaid"
        },
        {
            "transaction_id": "F003",
            "client_id": "C003",
            "type": "Expense",
            "amount": 6200,
            "status": "Paid"
        }
    ]

def get_client_data():
    return [
        {
            "client_id": "C001",
            "client_name": "ABC Manufacturing",
            "industry": "Manufacturing",
            "contact_person": "Ahmad Zaki",
            "email": "ahmad@abc.com.my",
            "status": "Active"
        },
        {
            "client_id": "C002",
            "client_name": "GreenTech Solution",
            "industry": "Technology",
            "contact_person": "Nur Aina",
            "email": "aina@greentech.com.my",
            "status": "Active"
        },
        {
            "client_id": "C003",
            "client_name": "FreshMart Retail",
            "industry": "Retail",
            "contact_person": "Daniel Lee",
            "email": "daniel@freshmart.com.my",
            "status": "Inactive"
        }
    ]
