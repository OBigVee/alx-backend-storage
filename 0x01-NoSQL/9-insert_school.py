#!/usr/bin/env python3
"""inserts a new documents in a collection based on kwargs"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """ inserts docs
    Returns _id
    """
    return mongo_collection.insert_one(kwargs).inserted_id