from bson import ObjectId
from app.db import books_collection

def add_book(data):
    books_collection.insert_one(data)

def get_all_books():
    return list(books_collection.find())

def update_book(book_id, updated_data):
    books_collection.update_one({"_id": ObjectId(book_id)}, {"$set": updated_data})

def delete_book(book_id):
    books_collection.delete_one({"_id": ObjectId(book_id)})

def search_books(field, value):
    from app.db import books_collection
    return list(books_collection.find({field: {'$regex': value, '$options': 'i'}}))
