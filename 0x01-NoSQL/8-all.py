#!/usr/bin/env python3
"""list all documents in python"""
import pymongo


def list_all(mongo_collection):
    """function lists all documents in a collection
    Returns an empty list if no document
    """
    return [doc for doc in mongo_collection.find()]

