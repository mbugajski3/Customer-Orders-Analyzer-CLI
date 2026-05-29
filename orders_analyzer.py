import csv
import sys

def find_top_item(data):
    highest_data_name = list(data.keys())[0]
    highest_data_value = data[highest_data_name]
    for name in data:
        if data[name] > highest_data_value:
            highest_data_value = data[name]
            highest_data_name = name
    return highest_data_name, highest_data_value


def load_orders(filename):
    with open(filename) as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            print("Error: CSV file is empty.")
            exit()
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
        return orders


def format_money(value):
    return f"{value:,.2f}".replace(",", " ")


def calculate_metrics(orders):
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

    return total_revenue, total_orders, average_order_value, revenue_by_customer, orders_by_customer, unique_customers, revenue_by_country, revenue_by_category


def print_report(total_revenue,
                total_orders,
                average_order_value,
                revenue_by_customer,
                orders_by_customer,
                unique_customers,
                revenue_by_country,
                revenue_by_category,
                highest_revenue_customer_name,
                highest_revenue_customer_value,
                top_orders_customer_name,
                top_orders_customer_value,
                top_revenue_country_name,
                top_revenue_country_value,
                top_revenue_category_name, 
                top_revenue_category_value
    ):

    print("Revenue by customer: ")
    for name in revenue_by_customer:
        print(f"- {name}: {format_money(revenue_by_customer[name])} PLN")
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
        print(f"- {country}: {format_money(revenue_by_country[country])} PLN")
    print()
    print("Revenue by category: ")
    for category in revenue_by_category:
        print(f"- {category}: {format_money(revenue_by_category[category])} PLN")

    print()
    print(f"Total revenue: {format_money(total_revenue)} PLN")
    print(f"Total orders: {total_orders}")
    print(f"Average order value: {format_money(average_order_value)} PLN")
    print(f"Customer with most orders: {top_orders_customer_name} - {top_orders_customer_value} orders.")
    print(f"Customer with highest revenue: {highest_revenue_customer_name} - {format_money(highest_revenue_customer_value)} PLN")
    print(f"Country with highest revenue: {top_revenue_country_name} - {format_money(top_revenue_country_value)} PLN")
    print(f"Category with highest revenue: {top_revenue_category_name} - {format_money(top_revenue_category_value)} PLN")
    print(f"Unique customers: {len(unique_customers)}")

def main():

    if len(sys.argv) < 2:
        print("Usage: orders_analyzer.py filename.csv.")
        exit()

    filename = sys.argv[1]

    if not filename.endswith(".csv"):
        print("Error: input file must be a .csv file.")
        exit()

    try:
        orders = load_orders(filename)
    except FileNotFoundError:
        print("Error: File not found.")
        exit()
    except ValueError:
        print("Error: invalid numeric value in CSV file.")
        exit()

    if not orders:
        print("Error: CSV file contains no order data.")
        exit()

    total_revenue, total_orders, average_order_value, revenue_by_customer, orders_by_customer, unique_customers, revenue_by_country, revenue_by_category = calculate_metrics(orders)

    highest_revenue_customer_name, highest_revenue_customer_value = find_top_item(revenue_by_customer)

    top_orders_customer_name, top_orders_customer_value = find_top_item(orders_by_customer)

    top_revenue_country_name, top_revenue_country_value = find_top_item(revenue_by_country)

    top_revenue_category_name, top_revenue_category_value = find_top_item(revenue_by_category)

    print_report(total_revenue,
                    total_orders,
                    average_order_value,
                    revenue_by_customer,
                    orders_by_customer,
                    unique_customers,
                    revenue_by_country,
                    revenue_by_category,
                    highest_revenue_customer_name,
                    highest_revenue_customer_value,
                    top_orders_customer_name,
                    top_orders_customer_value,
                    top_revenue_country_name,
                    top_revenue_country_value,
                    top_revenue_category_name, 
                    top_revenue_category_value
    )

    
if __name__ == "__main__":
    main()



