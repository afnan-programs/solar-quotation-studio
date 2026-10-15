from datetime import datetime
import math
from database.connection import get_connection

class quotation_service:

    @staticmethod
    def calculate_preset_items(
        system_kw,
        panel_brand="Longi 585W",
        panel_price=28000,
        inverter_brand="Inverex Nitrox 10kW",
        inverter_price=350000,
        structure_type="Standard L3",
        structure_price=65000,
        extra_cable_m=0,
        cable_rate=1200,
    ):
        items = []

        #panel math
        panel_wattage = 585
        panel_qty = math.ceil((system_kw * 1000)/panel_wattage)

        #1. Panels
        items.append(
            {
                "description": f"Solar Panels ({panel_brand})",
                "quantity": panel_qty,
                "unit_price": panel_price,
            }
        )
        #2. Inverter
        items.append(
            {
                "description": f"Inverter ({inverter_brand})",
                "quantity": 1,
                "unit_price": inverter_price,
            }
        )

        # 3. Structure
        items.append(
            {
                "description": f"Mounting Structure ({structure_type})",
                "quantity": 1,
                "unit_price": structure_price,
            }
        )

        # 4. Wiring & Protection Box (Base 30m included + Extra)
        base_wiring_cost = 45000
        extra_cable_cost = max(0, extra_cable_m) * cable_rate
        items.append(
            {
                "description": f"Wiring, Breakers & Protection Box (+{extra_cable_m}m Extra Cable)",
                "quantity": 1,
                "unit_price": base_wiring_cost + extra_cable_cost,
            }
        )
        #5. Labor Cost calculation
        labor_cost = system_kw * 4000  # Rs 4,000 per kW
        items.append(
            {
                "description": "Installation, Testing & Commissioning",
                "quantity": 1,
                "unit_price": labor_cost,
            }
        )

        return items

    @staticmethod
    def save_quotation(
        customer_name,
        customer_phone,
        customer_address,
        system_capacity_kw,
        items,
        city="Gujranwala",
        connection_type="Three-Phase",
        system_type="Hybrid",
        discount=0,
        terms="50% Advance, 40% Delivery, 10% Handover",
        company_id=1,
    ):
      if not customer_name or not customer_name.strip():
         raise ValueError("Customer name is required!")
      if not items:
         raise ValueError("At least one quotation item is required!")

      subtotal = 0
      for item in items:
         line_total = float(item["quantity"]) * float(item["unit_price"])
         subtotal += line_total
      grand_total = subtotal - float(discount)
      created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

      with get_connection() as connection:
       cursor = connection.execute(
                """
                INSERT INTO quotations (
                    quotation_number, company_id, created_at, customer_name,
                    customer_phone, customer_address, city, connection_type,
                    system_type, system_capacity_kw, subtotal, discount, grand_total, terms
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "TEMP",
                    company_id,
                    created_at,
                    customer_name.strip(),
                    customer_phone,
                    customer_address,
                    city,
                    connection_type,
                    system_type,
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
                "UPDATE quotations SET quotation_number = ? WHERE id = ?",
                (quotation_number, quotation_id),
            )

       for item in items:
                qty = float(item["quantity"])
                price = float(item["unit_price"])
                connection.execute(
                    """
                    INSERT INTO quotation_items (quotation_id, description, quantity, unit_price, line_total)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (quotation_id, item["description"].strip(), qty, price, qty * price),
                )

      return quotation_id, quotation_number
