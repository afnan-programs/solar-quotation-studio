from flask import Flask, jsonify, render_template, request
from services.quotation_service import quotation_service

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("wizard.html")

@app.route("/api/calculate-preset", methods=["POST"])
def calculate_preset():
    data = request.json
    items = quotation_service.calculate_preset_items(
        system_kw = float(data.get("system_kw",10)),
        panel_brand = float(data.get("panel_brand","Longi 585W")),
        structure_type = float(data.get("structure_type","Standard L3")),
        extra_cable_m=int(data.get("extra_cable_m", 0)),
    )
    subtotal = 0
    for i in items:
        subtotal += i["quantity"] * i["unit_price"]
    return jsonify({"items": items, "subtotal":subtotal})

@app.route("/api/save-quotation", methods=["POST"])
def save_quotation():
    try:
       data = request.json
       q_id, q_num = quotation_service.save_quotation(
           customer_name=data["customer_name"],
           customer_phone=data["customer_phone"],
           system_capacity_kw=float(data["system_kw"]),
           items=data["items"],
           customer_address=data.get("customer_address", ""),
           city=data.get("city", "Local"),
           connection_type=data.get("connection_type", "Three-Phase"),
           system_type=data.get("system_type", "Hybrid"),
           discount=float(data.get("discount", 0)),
       )
       return jsonify(
            {
                "success": True,
                "quotation_id": q_id,
                "quotation_number": q_num,
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)

   