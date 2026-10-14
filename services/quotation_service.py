from datetime import datetime
from database.connection import get_connection

def save_quotation(
    customer_name,
    customer_phone,
    customer_address,
    system_capacity_kw,
    items,
    discount=0,
    terms=""
):
    if not isinstance(customer_name, str) or not customer_name.strip():
        raise ValueError("A valid customer name is required!")
    
    if not isinstance(items, list):
        raise TypeError("Items must be provided as a list.")
    
    if not items:
        raise ValueError("At least one quotation item is required!")
    
    subtotal = 0

    for item in items:
        quantity = float(item["quantity"])
        unit_price = float(item["unit_price"])

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        if unit_price < 0:
            raise ValueError("Unit price cannot be negative.")

        subtotal += quantity * unit_price

    discount = float(discount)
    if discount < 0 or discount > subtotal:
        raise ValueError("Discount must be between zero and subtotal.")
    
    grand_total = subtotal - discount
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as connection:
        cursor = connection.execute(
            """
     INSERT INTO quotations(
     quotation_number,
     created_at,
     customer_name,
     customer_phone,
     customer_address,
     system_capacity_kw,
     subtotal,
     discount,
     grand_total,
     terms
     )
     VALUES (?,?,?,?,?,?,?,?,?,?)
""",
(
    "TEMP",
    created_at,
    customer_name.strip(),
    customer_phone,
    customer_address,
    system_capacity_kw,
    subtotal,
    discount,
    grand_total,
    terms,
),
        )

        quotation_id = cursor.lastrowid
        quotation_number = f"SQ-{created_at[:4]}-{quotation_id:04d}"

        connection.execute(
            """
UPDATE quotations SET quotation_number = ? WHERE id = ?
""",
(quotation_number, quotation_id)
        )
        for item in items:
              quantity = float(item["quantity"])
              unit_price = float(item["unit_price"])
              line_total = quantity * unit_price
              connection.execute(
                      """
                      INSERT INTO quotation_items (
                          quotation_id,
                          description,
                          quantity,
                          unit_price,
                          line_total
                          )
                      VALUES (?,?,?,?,?)
                          """,
                          (quotation_id,
                           item["description"].strip(),
                           quantity,
                           unit_price,
                          line_total ),
              )
    return quotation_id, quotation_number