from pymongo import MongoClient

client = MongoClient(host='mongodb://guygubaby.top', port=27017)

image_box = client.imagebox

emoji_db = image_box.emoji
