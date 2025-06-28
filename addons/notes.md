**Controller example where packaging the data and serving the xml on the server.**

**`odoo-custom/addons/payment/controllers/portal.py`**

**So now when you try to purchase the product, it sends request to route:**
**`/payment/custom/process`**

**Which is in:**
**`payment/payment_custom`**

**With that I need to create this:**

<!--toc:start-->

- [🏭 Custom Manufacturing + Sales Management System (Odoo Project)](#🏭-custom-manufacturing-sales-management-system-odoo-project)
- [🧠 Summary: What You’re Simulating](#🧠-summary-what-youre-simulating)
  - [🔄 What You Actually Need to Build](#🔄-what-you-actually-need-to-build)
    - [✅ 1. Desk Order Lifecycle](#1-desk-order-lifecycle)
    - [✅ 2. Inventory Integration](#2-inventory-integration)
    - [✅ 3. Sales Order & Invoice Generation](#3-sales-order-invoice-generation)
    - [✅ 4. Material Procurement (Optional)](#4-material-procurement-optional)
    - [✅ 5. PDF Report (QWeb)](#5-pdf-report-qweb)
    - [✅ 6. API Endpoint](#6-api-endpoint)
    - [✅ 7. Optional Enhancements](#7-optional-enhancements)
  - [✅ Project Goals](#project-goals)
  - [📁 Suggested Structure](#📁-suggested-structure)
    - [Custom App: `custom_desk_mrp`](#custom-app-customdeskmrp)
  - [🧱 Model Examples](#🧱-model-examples)
    - [DeskOrder model](#deskorder-model)
    - [DeskMaterialLine model](#deskmaterialline-model)
  - [✅ Views](#views)
  - [🧾 Report (QWeb)](#🧾-report-qweb)
  - [🧠 SQL View](#🧠-sql-view)
  - [🌐 API Controller](#🌐-api-controller)
  - [⚙️ Simulated Workflow](#️-simulated-workflow)
  - [🧩 Bonus Ideas](#🧩-bonus-ideas)
  - [📚 Learning Outcome](#📚-learning-outcome)
  <!--toc:end-->

# 🏭 Custom Manufacturing + Sales Management System (Odoo Project)

> Build an Odoo module that helps a company manage **custom office desk production**, from order to delivery. Demonstrates full stack of ERP, CRM, Inventory, and Accounting knowledge.

# 🧠 Summary: What You’re Simulating

Customer places order →

Materials used from inventory →
Desk built →
Sale order created →
Invoice sent →
Purchase raw materials if needed

# What happens after the transaction

1. Customer has placed the order

   - We have to build that order with our desk.order model
   - Load the modules:

     - Inventory
     - Sale:
       - CRM
       - Reports
     - Manufacturing
     - Invoicing (Invoicing & Payments module)
     - Expenses (Do I need this?)

# Convert Web Quotation -> Sales Order

- Automatically confirms the quotation + (allow button if something fails)
- Create Manufacturing Order
- Deduct Inventory
- Generate PDF Reports
- Create Dashboard / SQL View
- Expose API Endpoint JSON view for desk orders by customers

## Default Behaviour

User purchases the product, the quotation is created after the payment.
`We can automate everything or trough buttons create the mrp module`
When user previews all of the quotations,
confirmation can be sent to create sales.order.

So my module should be up and running after, the sales.order creation.
Do I need to setup the webhook that will listen for the changes on the server.
So it can trigger the module, or what should I do to create such a functionality?

I think, I should not change the default behaviour of the lib,
but rather build on top of it?

So what is the next step of the custom_desk_mrp module?

## 🔄 What You Actually Need to Build

### ✅ 1. Desk Order Lifecycle

- Implement the custom model `desk.order` with fields for customer, desk type, materials, and total cost.
- Allow users to create desk orders through form views.
- Use `@api.depends` to compute the total cost dynamically based on selected materials.
- Use `@api.onchange` to improve the user experience when selecting desk types or materials.
- Add a `state` field and support transitions such as: `draft → confirmed → done`.

---

### ✅ 2. Inventory Integration

- Once a desk order is confirmed:
  - Deduct selected raw materials from stock.
  - Use `stock.move` and/or `stock.picking` to simulate or trigger inventory operations.
  - Ensure inventory quantities are updated (requires `stock` module).

---

### ✅ 3. Sales Order & Invoice Generation

- Automatically create a `sale.order` linked to the desk product when the desk order is confirmed.
- Ensure the sale order includes the customer and pricing.
- Use Odoo’s standard workflow to:
  - Trigger delivery from the warehouse.
  - Generate an `account.move` (invoice) from the sale order.
- Optionally, call `create_invoice()` or `action_confirm()` as part of the desk order flow.

---

### ✅ 4. Material Procurement (Optional)

- If material stock is low or below a threshold:
  - Automatically create a `purchase.order` to a predefined vendor.
  - Include all necessary products in `purchase.order.line`.
  - Simulate vendor pricelist logic and procurement rules.

---

### ✅ 5. PDF Report (QWeb)

- Create a printable PDF report of the desk order:
  - Include customer info, selected desk, material breakdown, and total cost.
  - Style it with company branding and a clean layout.
  - Trigger from a "Print" button in the form view.

---

### ✅ 6. API Endpoint

- Implement an endpoint: `/api/customer_orders/<partner_id>`
- It should return a JSON response containing:
  - All desk orders for the given customer.
  - Relevant fields such as order reference, desk type, cost, and state.

---

### ✅ 7. Optional Enhancements

- Add a custom "Mark as Done" button in the form view.
- When clicked, it should:
  - Update inventory.
  - Trigger the creation of a sales order and invoice.
  - Optionally move the order to the `done` state.

---

## ✅ Project Goals

| Feature                         | ERP Skill Covered                             |
| ------------------------------- | --------------------------------------------- |
| Custom model for desk orders    | `models`, fields, `@api.depends`, `@onchange` |
| Relation to product, BoM        | `Many2one`, `One2many`, `Many2many`           |
| Chatter for communication       | `mail.thread`                                 |
| Tree and form views             | XML `form`, `tree`, `search`                  |
| Dynamic computation of cost     | `@api.depends` fields                         |
| PDF report with QWeb            | `report_qweb`                                 |
| Dashboard-like SQL View         | SQL + `window functions`                      |
| Controller for external access  | `http.Controller`, API route                  |
| Partner (customer) selection    | Functional knowledge of `res.partner`         |
| Use product.template/variant    | Functional product knowledge                  |
| Inventory deduction per order   | `stock.move`, `stock.picking`                 |
| Sale Order and Invoice creation | `sale.order`, `account.move` integration      |
| Purchase of raw materials       | `purchase.order`, vendor logic                |

---

## 📁 Suggested Structure

### Custom App: `custom_desk_mrp`

| Folder                         | Contents                               |
| ------------------------------ | -------------------------------------- |
| `models/desk_order.py`         | `DeskOrder`, `DeskMaterialLine` models |
| `views/desk_order_views.xml`   | Tree, Form, Search views               |
| `report/desk_order_report.xml` | QWeb PDF report                        |
| `controllers/api.py`           | JSON API: `/api/desks/customer/123`    |
| `data/`                        | Demo products, partners, BoMs          |
| `security/ir.model.access.csv` | Permissions                            |

---

## 🧱 Model Examples

### DeskOrder model

```python
class DeskOrder(models.Model):
    _name = "desk.order"
    _inherit = ["mail.thread"]
    _description = "Custom Desk Order"

    name = fields.Char(string="Order Reference", required=True, default=lambda self: _('New'))
    customer_id = fields.Many2one("res.partner", string="Customer", required=True)
    desk_product_id = fields.Many2one("product.template", string="Desk Type", required=True)
    material_ids = fields.One2many("desk.material.line", "order_id", string="Materials Used")
    total_cost = fields.Float(compute="_compute_total_cost", store=True)
    state = fields.Selection([...])
```

---

### DeskMaterialLine model

```python
class DeskMaterialLine(models.Model):
    _name = "desk.material.line"
    _description = "Materials for Desk"

    product_id = fields.Many2one("product.product")
    quantity = fields.Float()
    unit_price = fields.Float(related="product_id.standard_price")
    order_id = fields.Many2one("desk.order", ondelete="cascade")
```

---

## ✅ Views

- `tree` view of all desk orders
- `form` view with material line items (O2M)
- `search` view with filters: customer, desk type, state

---

## 🧾 Report (QWeb)

- Print Order PDF: include customer, materials, costs, estimated delivery
- Use company branding

---

## 🧠 SQL View

**Monthly Desk Order Summary**

- PostgreSQL window functions: `ROW_NUMBER()`, `SUM() OVER (...)`
- Output: customer name, desk type, month, total cost, avg quantity

---

## 🌐 API Controller

`/api/customer_orders/<partner_id>`  
Returns JSON list of all desk orders and costs for a specific customer.

---

## ⚙️ Simulated Workflow

1. Admin creates Desk Order
2. Selects customer, desk type, materials
3. System computes total cost
4. PDF report generated
5. Inventory deducted
6. Sale Order created
7. Invoice generated
8. Purchase Order created if needed

---

## 🧩 Bonus Ideas

- Add custom button: "Mark as Done" → triggers delivery + invoice
- Add delivery deadline and late fee
- Add dashboard widget for top customers

---

## 📚 Learning Outcome

| Skill          | You'll Practice                          |
| -------------- | ---------------------------------------- |
| Python/OOP     | Inheritance, computed fields, decorators |
| ORM            | Fields, relations, constraints           |
| Views          | `form`, `tree`, `search`                 |
| QWeb           | Templating, reports                      |
| SQL            | Window functions, analytics              |
| Functional ERP | Sales, MRP, Purchase, CRM                |

---
