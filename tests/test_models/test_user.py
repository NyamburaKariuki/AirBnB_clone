#!/usr/bin/python3
"""Unit tests for the `state` module.
"""
import os
import unittest
from models.engine.file_storage import FileStorage
from models.user import User
from models import storage
from datetime import datetime


class TestState(unittest.TestCase):
    """Test cases for the class User."""

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_params(self):
        user1 = User()
        x = f"{type(user1).__name__}.{user1.id}"
        self.assertIn(x, storage.all())
        self.assertIsInstance(user1.email, str)
        self.assertIsInstance(user1.password, str)
        self.assertIsInstance(user1.first_name, str)
        self.assertIsInstance(user1.last_name, str)

    def test_init(self):
        """Test for public instances"""
        user1 = User()
        user2 = User(**user1.to_dict())
        self.assertIsInstance(user1.id, str)
        self.assertIsInstance(user1.created_at, datetime)
        self.assertIsInstance(user1.updated_at, datetime)
        self.assertEqual(user1.updated_at, user2.updated_at)

    def test_str(self):
        """Test for string rep"""
        user1 = User()
        string = f"[{type(user1).__name__}] ({user1.id}) {user1.__dict__}"
        self.assertEqual(user1.__str__(), string)

    def test_save(self):
        """Test method for save"""
        user1 = User()
        old_update = user1.updated_at
        user1.save()
        self.assertNotEqual(user1.updated_at, old_update)

    def test_todict(self):
        """Test for dict"""
        user1 = User()
        user2 = User(**user1.to_dict())
        a_dict = user2.to_dict()
        self.assertIsInstance(a_dict, dict)
        self.assertEqual(a_dict['__class__'], type(user2).__name__)
        self.assertIn('created_at', a_dict.keys())
        self.assertIn('updated_at', a_dict.keys())
        self.assertNotEqual(user1, user2)


if __name__ == "__main__":
    unittest.main()
