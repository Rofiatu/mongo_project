from db_operations import retrieve_documents
import pandas as pd

documents = retrieve_documents()

def flatten_to_dataframe(documents):
    flat_data = []
    for d in documents:
        base_info = {
            'idValue': d['_id'],
            'couponUsed': d['couponUsed'],
            'customerAge': d['customer']['age'],
            'customerEmail': d['customer']['email'],
            'customerGender': d['customer']['gender'],
            'customerSatisfaction': d['customer']['satisfaction'],
            'purchaseMethod': d['purchaseMethod'],
            'saleDate': d['saleDate'],
            'storeLocation': d['storeLocation']
        }
        for item in d['items']:
            flat_item = {
                'itemName': item['name'],
                'itemPrice': item['price'],
                'itemQuantity': item['quantity'],
                'itemTags': item['tags']
            }
            combined_info = {**base_info, **flat_item}
            flat_data.append(combined_info)

    df = pd.DataFrame(flat_data)
    return df

def export_to_csv(df, filename):
    df.to_csv(filename, index=False)

df = flatten_to_dataframe(documents)
export_to_csv(df, 'data.csv')
