#!/usr/bin/python3
"""Unit tests for the `city` module.
"""
import os
import unittest
from models.engine.file_storage import FileStorage
from models import storage
from models.city import City
from datetime import datetime

city1 = City()
city2 = City(**city1.to_dict())
city3 = City("hello", "wait", "in")


class TestCity(unittest.TestCase):
    """Test cases for the City class."""

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_parameters(self):
        """Test method for class attributes"""
        k = f"{type(city1).__name__}.{city1.id}"
        self.assertIsInstance(city1.name, str)
        self.assertEqual(city3.name, "")
        city1.name = "Mombasa"
        self.assertEqual(city1.name, "Mombasa")

    def test_init(self):
        """Test method for public instances"""
        self.assertIsInstance(city1.id, str)
        self.assertIsInstance(city1.created_at, datetime)
        self.assertIsInstance(city1.updated_at, datetime)
        self.assertEqual(city1.updated_at, city2.updated_at)

    def test_save(self):
        """Test method for save"""
        old_update = city1.updated_at
        city1.save()
        self.assertNotEqual(city1.updated_at, old_update)

    def test_to_dict(self):
        """Test method for dict"""
        a_dict = city2.to_dict()
        self.assertIsInstance(a_dict, dict)
        self.assertEqual(a_dict['__class__'], type(city2).__name__)
        self.assertIn('created_at', a_dict.keys())
        self.assertIn('updated_at', a_dict.keys())
        self.assertNotEqual(city1, city2)


if __name__ == "__main__":
    unittest.main()
