import csv
import sys

def find_top_item(data):
    top_item_name = list(data.keys())[0]
    top_item_value = data[top_item_name]
    for name in data:
        if data[name] > top_item_value:
            top_item_value = data[name]
            top_item_name = name
    return top_item_name, top_item_value


def load_orders(filename):
    with open(filename) as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("CSV file is empty.")

        required_columns = ["order_id",
                            "date",
                            "customer_id",
                            "customer_name",
                            "product",
                            "category",
                            "quantity",
                            "price",
                            "country"
        ]

        missing_columns = []

        for column in required_columns:
            if column not in reader.fieldnames:
                missing_columns.append(column)

        if len(missing_columns) != 0:
            raise ValueError(f"missing columns - {missing_columns}")

        orders = []

        for row in reader:
            for column in required_columns:
                if row[column].strip() == "":
                    raise ValueError(f"Missing value in {column}")
            
               
            order_id = int(row["order_id"])
            date = row["date"]
            customer_id = row["customer_id"]
            customer_name = row["customer_name"]
            product = row["product"]
            category = row["category"]
            quantity = int(row["quantity"])
            price = float(row["price"])
            country = row["country"]

            if quantity <= 0:
                raise ValueError("Quantity cannot be negative or zero.")                

            if price < 0:
                raise ValueError("Price cannot be negative.")
                
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

    metrics = {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "average_order_value": average_order_value,
        "revenue_by_customer": revenue_by_customer,
        "orders_by_customer": orders_by_customer,
        "unique_customers": unique_customers,
        "revenue_by_country": revenue_by_country,
        "revenue_by_category": revenue_by_category
    }

    return metrics

def calculate_top_results(metrics):
    top_results = {}

    highest_revenue_customer_name, highest_revenue_customer_value = find_top_item(metrics["revenue_by_customer"])
    top_results["revenue_by_customer"] = {
        "name": highest_revenue_customer_name,
        "value": highest_revenue_customer_value
    }

    top_orders_customer_name, top_orders_customer_value = find_top_item(metrics["orders_by_customer"])   
    top_results["orders_by_customer"] = {
        "name": top_orders_customer_name,
        "value": top_orders_customer_value
    }

    top_revenue_country_name, top_revenue_country_value = find_top_item(metrics["revenue_by_country"])
    top_results["revenue_by_country"] = {
        "name": top_revenue_country_name,
        "value": top_revenue_country_value
    }

    top_revenue_category_name, top_revenue_category_value = find_top_item(metrics["revenue_by_category"])
    top_results["revenue_by_category"] = {
        "name": top_revenue_category_name,
        "value": top_revenue_category_value
    }

    return top_results


def print_report(metrics, top_results):

    print("Revenue by customer: ")
    for name in metrics["revenue_by_customer"]:
        print(f"- {name}: {format_money(metrics['revenue_by_customer'][name])} PLN")
    print()
    print("Orders by customer: ")
    for name in metrics["orders_by_customer"]:
        if metrics["orders_by_customer"][name] == 1:
            print(f"- {name}: {metrics['orders_by_customer'][name]} order")
        else:
            print(f"- {name}: {metrics['orders_by_customer'][name]} orders")
    print()
    print("Revenue by country: ")
    for country in metrics["revenue_by_country"]:
        print(f"- {country}: {format_money(metrics['revenue_by_country'][country])} PLN")
    print()
    print("Revenue by category: ")
    for category in metrics["revenue_by_category"]:
        print(f"- {category}: {format_money(metrics['revenue_by_category'][category])} PLN")

    print()
    print(f"Total revenue: {format_money(metrics['total_revenue'])} PLN")
    print(f"Total orders: {metrics['total_orders']}")
    print(f"Average order value: {format_money(metrics['average_order_value'])} PLN")
    print(f"Customer with most orders: {top_results['orders_by_customer']['name']} - {top_results['orders_by_customer']['value']} orders.")
    print(f"Customer with highest revenue: {top_results['revenue_by_customer']['name']} - {format_money(top_results['revenue_by_customer']['value'])} PLN")
    print(f"Country with highest revenue: {top_results['revenue_by_country']['name']} - {format_money(top_results['revenue_by_country']['value'])} PLN")
    print(f"Category with highest revenue: {top_results['revenue_by_category']['name']} - {format_money(top_results['revenue_by_category']['value'])} PLN")
    print(f"Unique customers: {len(metrics['unique_customers'])}")

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
    except ValueError as error:
        print(f"Error: {error}")
        exit()

    if not orders:
        print("Error: CSV file contains no order data.")
        exit()

    metrics = calculate_metrics(orders)
    top_results = calculate_top_results(metrics)

    print_report(metrics, top_results)
    
    
if __name__ == "__main__":
    main()



