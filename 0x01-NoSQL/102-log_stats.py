#!/usr/bin/env python3
"""improve 12-log_stats.py by adding the top 10 of the most
present IPs in the collection nginx of the db logs:"""

from ipaddress import ip_address
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
    
    print("IPs:")
    countIps = nginxCollection.aggregate([
        {"$group":
        {
            "_id": "$ip",
            "count": {"$sum": 1}
        }},
        {"$sort":{"count":-1}},
        {"$limit":10},
        {"$project":{
            "_id":0,
            "ip":"$_id",
            "count":1
        }}
    ])
    for topIp in countIps:
        count = topIp.get("count")
        ip_address = topIp.get("ip")
        print("\t{}: {}".format(ip_address,count))
   

if __name__ == "__main__":
    check_Nginx_stats() 