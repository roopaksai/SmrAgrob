from datetime import timedelta

class DevConfig:
    URL = "http://localhost:6600/api"
    DB_STRING = "mongodb+srv://roopak:hyMA38xFNjtIc9IB@cluster0.lxzxlsb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    DB_NAME = "smr_agro"
    
    JWT_SECRET_KEY = "AdminSecret-5937e2029b4aa10f3008f2a5cb372e537ba8d8a4bd05a87efb086634df175fec60167bf48cbfe399e5c98d7c8ea27137d44993ab28b71cfe2ae786f5d1952"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)