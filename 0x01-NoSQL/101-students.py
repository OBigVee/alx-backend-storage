#!/usr/bin/env python3
"""Python function returns all students sorted by avg score"""
import pymongo


def top_students(mongo_collection):
    """return students sorted by avg scores"""
    return mongo_collection.aggregate([
        {
            "$project":
                {
                    "name": "$name",
                    "averageScore": {"$avg": "$topics.score"}
                }
        },
        {
            "$sort":
            {"averageScore": -1}
        }
])