#!/usr/bin/env python3
"""function changes all topics of a school document based on the name
"""
import pymongo


def update_topics(mongo_collection, name, topics):
    """change all topics
    mongo_collection:  will be the pymongo collection object
    name: (string) will be the school name to update
    topics: list of strings) will be the list of topics approached in the
    school
    """
    return mongo_collection.update_many({"name": name},
                                        {"$set": {"topics": topics}})