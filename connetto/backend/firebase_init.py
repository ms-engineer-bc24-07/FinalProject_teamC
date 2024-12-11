# firebase_init.py
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('/Users/ami/teamC/FinalProject_teamC/connetto/backend/firebase_credentials.json')
firebase_admin.initialize_app(cred)

print("Firebase initialized successfully!")
