from pymongo import MongoClient

# =====================================
# CONEXIÓN A MONGODB
# =====================================

cliente = MongoClient(
    "mongodb://localhost:27017/"
)

# Base de datos

db = cliente["SEM_Web_Advisor"]

# Colección

coleccion = db["reportes"]