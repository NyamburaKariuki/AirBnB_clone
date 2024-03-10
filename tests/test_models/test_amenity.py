#!/usr/bin/python3
"""Unit tests for the `amenity` module.
"""
import os
import unittest
from models import storage
from datetime import datetime
from models.amenity import Amenity
from models.engine.file_storage import FileStorage


class TestAmenity(unittest.TestCase):
    """Test cases for the `Amenity` class."""

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_parameters(self):
        """Test for class attributes"""

        x = Amenity()
        y = Amenity(**x.to_dict())
        z = Amenity("hi", "how", "in")

        k = f"{type(x).__name__}.{x.id}"
        self.assertIsInstance(x.name, str)
        self.assertIn(k, storage.all())
        self.assertEqual(x.name, "")

    def test_init(self):
        """test for public instances"""
        x = Amenity()
        y = Amenity(**x.to_dict())
        self.assertIsInstance(x.id, str)
        self.assertIsInstance(x.created_at, datetime)
        self.assertIsInstance(x.updated_at, datetime)
        self.assertEqual(x.updated_at, y.updated_at)

    def test_string(self):
        """Test for string representation"""
        x = Amenity()
        string = f"[{type(x).__name__}] ({x.id}) {x.__dict__}"
        self.assertEqual(x.__str__(), string)

    def test_save(self):
        """Test method for save"""
        x = Amenity()
        old_up = x.updated_at
        x.save()
        self.assertNotEqual(x.updated_at, old_up)

    def test_to_dict(self):
        """Test method for to_dict"""
        x = Amenity()
        y = Amenity(**x.to_dict())
        x_todict = y.to_dict()
        self.assertIsInstance(x_todict, dict)
        self.assertEqual(x_todict['__class__'], type(y).__name__)
        self.assertIn('created_at', x_todict.keys())
        self.assertIn('updated_at', x_todict.keys())
        self.assertNotEqual(x, y)


if __name__ == "__main__":
    unittest.main()
