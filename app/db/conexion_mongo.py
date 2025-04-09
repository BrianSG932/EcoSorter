from pymongo import MongoClient

def get_db():
    # Conexión a MongoDB (usa el URI que ya tienes)
    client = MongoClient('mongodb+srv://BrianSG230:KmAq8alNdVqEbCJ9@ecosorter.cjb4gde.mongodb.net/')
    db = client['EcoSorter']
    return db, client