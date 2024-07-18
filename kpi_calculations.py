import pymongo
import decimal
from bson.decimal128 import Decimal128, create_decimal128_context
from decimal import Decimal, Context
from db_operations import connect_to_mongodb

mycoll = connect_to_mongodb()

def decimal128_to_decimal(value):
    decimal_context = Context(prec=6)
    with decimal.localcontext(decimal_context):
        return value.to_decimal()

def calculate_total_sales_value():
    
    pipeline = [
        {'$unwind': '$items'},
        {'$group': {
            '_id': None,
            'totalSalesValue': {'$sum': {'$multiply': ['$items.price', '$items.quantity']}}
        }}
    ]
    
    result = mycoll.aggregate(pipeline)
    total_sales_value = next(result)['totalSalesValue']
    
    total_sales_value = decimal128_to_decimal(total_sales_value)
    
    return total_sales_value

def calculate_number_of_customers():
    
    pipeline = [
        {'$group': {
            '_id': '$customer.email'
        }},
        {'$count': 'numCustomers'}
    ]
    
    result = mycoll.aggregate(pipeline)
    num_customers = next(result)['numCustomers']
    
    return num_customers

def calculate_average_sale_per_customer(total_sales_value, num_customers):
    if num_customers == 0:
        return Decimal('0')
    
    avg_sale_per_customer = total_sales_value / num_customers
    return avg_sale_per_customer

def calculate_average_price_per_item():
        
    average_price_pipeline = [
        {'$unwind': '$items'},
        {'$group': {
            '_id': None,
            'totalPrice': {'$sum': '$items.price'},
            'itemCount': {'$sum': 1}
        }},
        {'$project': {
            '_id': 0,
            'averagePrice': {'$divide': ['$totalPrice', '$itemCount']}
        }}
    ]
    
    result = mycoll.aggregate(average_price_pipeline)
    average_price = next(result)['averagePrice']
    
    average_price = decimal128_to_decimal(average_price)
    
    return average_price

def calculate_individual_average_price_per_item():
        
    average_prices = {}
    
    for document in mycoll.find():
        for item in document['items']:
            item_name = item['name']
            item_price = Decimal(item['price'].to_decimal())
            
            if item_name in average_prices:
                average_prices[item_name]['total_price'] += item_price
                average_prices[item_name]['count'] += 1
            else:
                average_prices[item_name] = {
                    'total_price': item_price,
                    'count': 1
                }
    
    for item_name, stats in average_prices.items():
        average_prices[item_name]['average_price'] = stats['total_price'] / stats['count']
    
    return average_prices

def calculate_total_quantity_sold():
        
    total_qty_pipeline = [
        {'$unwind': '$items'},
        {'$group': {
            '_id': None,
            'totalItems': {'$sum': '$items.quantity'}
        }},
        {'$project': {
            '_id': 0,
            'totalItems': 1
        }}
    ]
    
    result = mycoll.aggregate(total_qty_pipeline)
    total_qty = next(result)['totalItems']
    
    return total_qty

def calculate_total_item_count():
        
    item_count_pipeline = [
        {'$unwind': '$items'},
        {'$group': {
            '_id': None,
            'totalItemCount': {'$sum': 1}
        }},
        {'$project': {
            '_id': 0,
            'totalItemCount': 1
        }}
    ]
    
    result = mycoll.aggregate(item_count_pipeline)
    item_count = next(result)['totalItemCount']
    
    return item_count

# total_sales_value = calculate_total_sales_value()
# num_customers = calculate_number_of_customers()
# avg_sale_per_customer = calculate_average_sale_per_customer(total_sales_value, num_customers)
# avg_price_per_item = calculate_average_price_per_item()
# individual_avg_per_item = calculate_individual_average_price_per_item()
# total_qty = calculate_total_quantity_sold()
# item_count = calculate_total_item_count()

# print(f'Total Sales Value: {total_sales_value}')
# print(f'Number of Unique Customers: {num_customers}')
# print(f'Average sale per Customer: {avg_sale_per_customer}')
# print(f'Average Price per Item: {avg_price_per_item}')
# for item_name, stats in individual_avg_per_item.items():
#     print(f"Average price for {item_name}: ${stats['average_price']:.2f}")
# print(f'Total Qty Sold: {total_qty}')
# print(f'Total Count of Items: {item_count}')