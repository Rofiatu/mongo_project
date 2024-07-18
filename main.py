import db_operations as dbo
import kpi_calculations as kpi
import json_to_csv as jtc

def main():
    # Retrieve documents from MongoDB
    documents = dbo.retrieve_documents()

    # Calculate KPIs
    total_sales_value = kpi.calculate_total_sales_value()
    num_customers = kpi.calculate_number_of_customers()
    avg_sale_per_customer = kpi.calculate_average_sale_per_customer(total_sales_value, num_customers)
    avg_price_per_item = kpi.calculate_average_price_per_item()
    individual_avg_per_item = kpi.calculate_individual_average_price_per_item()
    total_qty = kpi.calculate_total_quantity_sold()
    item_count = kpi.calculate_total_item_count()

    print(f'Total Sales Value: {total_sales_value}')
    print(f'Number of Unique Customers: {num_customers}')
    print(f'Average sale per Customer: {avg_sale_per_customer}')
    print(f'Average Price per Item: {avg_price_per_item}')
    for item_name, stats in individual_avg_per_item.items():
        print(f"Average price for {item_name}: ${stats['average_price']:.2f}")
    print(f'Total Qty Sold: {total_qty}')
    print(f'Total Count of Items: {item_count}')

    # Flatten documents to DataFrame
    df = jtc.flatten_to_dataframe(documents)

    # Export to CSV
    jtc.export_to_csv(df, 'data.csv')

if __name__ == "__main__":
    main()
