#!/usr/bin/env python3
"""script provides statsabout Nginx logs stored in MongoDB"""


from pymongo import MongoClient


def check_Nginx_stats():
    """ stats about Nginx logs stored in MongoDB:"""
    client = MongoClient('mongodb://127.0.0.1:27017') # db
    nginxCollection = client.logs.nginx # collection

    numOfDoc = nginxCollection.count_documents({})
    print("{} logs".format(numOfDoc))
    print("Methods:")
    methodsList = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methodsList:
        methodCount = nginxCollection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, methodCount))
    status = nginxCollection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(status))


if __name__ == "__main__":
    check_Nginx_stats() 