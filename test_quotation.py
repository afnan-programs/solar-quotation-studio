
from services.quotation_service import save_quotation

quotation_id, quotation_number = save_quotation(
    customer_name="Ali Solar Solutions",
    customer_phone="03001234567",
    customer_address="Gujranwala",
    system_capacity_kw=10,
    items=[
        {
            "description": "Solar Panels",
            "quantity": 10,
            "unit_price": 18000,
        },
        {
            "description": "Inverter",
            "quantity": 1,
            "unit_price": 150000,
        },
    ],
    discount=5000,
    terms="Quotation valid for 7 days.",
)

print("Saved ID:", quotation_id)
print("Quotation Number:", quotation_number)
