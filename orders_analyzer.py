import csv

with open("orders.csv") as file:
    reader = csv.DictReader(file)

    orders = []

    for row in reader:
        order_id = int(row["order_id"])
        date = row["date"]
        customer_id = row["customer_id"]
        customer_name = row["customer_name"]
        product = row["product"]
        category = row["category"]
        quantity = int(row["quantity"])
        price = float(row["price"])
        country = row["country"]

        order = {
            "order_id": order_id,
            "date": date,
            "customer_id": customer_id,
            "customer_name": customer_name,
            "product": product,
            "category": category,
            "quantity": quantity,
            "price": price,
            "country": country
        }

        orders.append(order)

    total_revenue = 0
    total_orders = len(orders)
    revenue_by_customer = {}
    orders_by_customer = {}
    
  

    for order in orders:
        revenue = order["quantity"] * order["price"]
        total_revenue += revenue
        customer_name = order["customer_name"]
        if customer_name not in revenue_by_customer:
            revenue_by_customer[customer_name] = 0
        revenue_by_customer[customer_name] += revenue

        if customer_name not in orders_by_customer:
            orders_by_customer[customer_name] = 0
        orders_by_customer[customer_name] +=1

    average_order_value = total_revenue / total_orders

    highest_revenue_customer_name = list(revenue_by_customer.keys())[0]
    highest_revenue_customer_value = revenue_by_customer[highest_revenue_customer_name]

    for name in revenue_by_customer:
        if revenue_by_customer[name] > highest_revenue_customer_value:
            highest_revenue_customer_value = revenue_by_customer[name]
            highest_revenue_customer_name = name




print(f"Total revenue: {total_revenue} PLN")
print(f"Total orders: {total_orders}")
print(f"Average order value: {average_order_value} PLN")
print("Revenue by customer: ")
for name in revenue_by_customer:
    print(f"- {name} {revenue_by_customer[name]} PLN")
print(f"Customer with highest revenue: {highest_revenue_customer_name} - {highest_revenue_customer_value} PLN")
for name in orders_by_customer:
    if orders_by_customer[name] <= 1:
        print(f"- {name} {orders_by_customer[name]} order")
    else:
        print(f"- {name} {orders_by_customer[name]} orders")


