'''
Module for working with Firebase Cloud Firestore.
'''

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


def add_to_database(id, youtube_link, transcription):
    doc_ref = db.collection('id').document(str(id))
    doc_ref.set({
        'youtube_link': youtube_link,
        'transcription': transcription
    })


def get_from_database(id):
    doc_ref = db.collection('id').document(str(id))
    doc = doc_ref.get()
    return doc.to_dict()
