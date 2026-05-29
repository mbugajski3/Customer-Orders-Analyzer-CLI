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
    unique_customers = []
    revenue_by_country = {}
    revenue_by_category = {}

    
  

    for order in orders:
        revenue = order["quantity"] * order["price"]
        total_revenue += revenue
        customer_name = order["customer_name"]
        customer_id = order["customer_id"]
        country = order["country"]
        category = order["category"]

        if customer_name not in revenue_by_customer:
            revenue_by_customer[customer_name] = 0
        revenue_by_customer[customer_name] += revenue

        if customer_name not in orders_by_customer:
            orders_by_customer[customer_name] = 0
        orders_by_customer[customer_name] += 1
     
        if customer_id not in unique_customers:
            unique_customers.append(customer_id)

        if country not in revenue_by_country:
            revenue_by_country[country] = 0
        revenue_by_country[country] += revenue

        if category not in revenue_by_category:
            revenue_by_category[category] = 0
        revenue_by_category[category] += revenue


    average_order_value = total_revenue / total_orders

    highest_revenue_customer_name = list(revenue_by_customer.keys())[0]
    highest_revenue_customer_value = revenue_by_customer[highest_revenue_customer_name]

    for name in revenue_by_customer:
        if revenue_by_customer[name] > highest_revenue_customer_value:
            highest_revenue_customer_value = revenue_by_customer[name]
            highest_revenue_customer_name = name

    top_orders_customer_name = list(orders_by_customer.keys())[0]
    top_orders_customer_value = orders_by_customer[top_orders_customer_name]

    for name in orders_by_customer:
        if orders_by_customer[name] > top_orders_customer_value:
            top_orders_customer_value = orders_by_customer[name]
            top_orders_customer_name = name

    top_revenue_country_name = list(revenue_by_country.keys())[0]
    top_revenue_country_value = revenue_by_country[top_revenue_country_name]

    for country in revenue_by_country:
        if revenue_by_country[country] > top_revenue_country_value:
            top_revenue_country_value = revenue_by_country[country]
            top_revenue_country_name = country

    top_revenue_category_name = list(revenue_by_category.keys())[0]
    top_revenue_category_value = revenue_by_category[top_revenue_category_name]

    for category in revenue_by_category:
        if revenue_by_category[category] > top_revenue_category_value:
            top_revenue_category_value = revenue_by_category[category]
            top_revenue_category_name = category





print("Revenue by customer: ")
for name in revenue_by_customer:
    print(f"- {name}: {revenue_by_customer[name]} PLN")
print()
print("Orders by customer: ")
for name in orders_by_customer:
    if orders_by_customer[name] == 1:
        print(f"- {name}: {orders_by_customer[name]} order")
    else:
        print(f"- {name}: {orders_by_customer[name]} orders")
print()
print("Revenue by country: ")
for country in revenue_by_country:
    print(f"- {country}: {revenue_by_country[country]} PLN")
print()
print("Revenue by category: ")
for category in revenue_by_category:
    print(f"- {category}: {revenue_by_category[category]} PLN")

print()
print(f"Total revenue: {total_revenue} PLN")
print(f"Total orders: {total_orders}")
print(f"Average order value: {average_order_value} PLN")
print(f"Customer with most orders: {top_orders_customer_name} - {top_orders_customer_value} orders.")
print(f"Customer with highest revenue: {highest_revenue_customer_name} - {highest_revenue_customer_value} PLN")
print(f"Country with highest revenue: {top_revenue_country_name} - {top_revenue_country_value} PLN")
print(f"Category with highest revenue: {top_revenue_category_name} - {top_revenue_category_value} PLN")
print(f"Unique customers: {len(unique_customers)}")

