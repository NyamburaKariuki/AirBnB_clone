#!/usr/bin/python3
"""review module"""
from models.base_model import BaseModel


class Review(BaseModel):
    """represents review"""
    place_id = ""
    user_id = ""
    text = ""
