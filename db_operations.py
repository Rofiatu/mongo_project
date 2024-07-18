import pymongo

def connect_to_mongodb():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = client["testdb"]
    mycoll = mydb["sales"]
    return mycoll

def retrieve_documents():
    mycoll = connect_to_mongodb()
    documents = list(mycoll.find())
    return documents