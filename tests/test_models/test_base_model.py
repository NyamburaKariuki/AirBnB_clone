"""Testing the `base_model` module."""
import json
import os
import time
import unittest
import uuid
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestBase(unittest.TestCase):
    """Tests for the BaseModel.
    """

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_init(self):
        """Test passing cases BaseModel initialization.
        """
        x = BaseModel()
        y_uuid = str(uuid.uuid4())
        y = BaseModel(id=y_uuid, name="weeknd", a="Thriller")
        self.assertIsInstance(x.id, str)
        self.assertIsInstance(y.id, str)
        self.assertEqual(y_uuid, y.id)
        self.assertEqual(y.a, "Thriller")
        self.assertEqual(y.name, "weeknd")
        self.assertIsInstance(x.created_at, datetime)
        self.assertIsInstance(y.created_at, datetime)
        self.assertEqual(str(type(x)),
                         "<class 'models.base_model.BaseModel'>")

    def test_dict(self):
        """Test for dict"""
        x = BaseModel()
        y_uuid = str(uuid.uuid4())
        y = BaseModel(id=y_uuid, name="weeknd", a="Thriller")
        x_dict = x.to_dict()
        self.assertIsInstance(x_dict, dict)
        self.assertIn('id', x_dict.keys())
        self.assertIn('created_at', x_dict.keys())
        self.assertIn('updated_at', x_dict.keys())
        self.assertEqual(x_dict['__class__'], type(x).__name__)
        with self.assertRaises(KeyError) as e:
            y.to_dict()

    def test_save(self):
        """Test for save"""
        y = BaseModel()
        time.sleep(0.5)
        now = datetime.now()
        y.save()
        difference = y.updated_at - now
        self.assertTrue(abs(difference.total_seconds()) < 0.01)

    def test_save_storage(self):
        """Tests that storage.save() is called from save()."""
        y = BaseModel()
        y.save()
        key = "{}.{}".format(type(y).__name__, y.id)
        d = {key: y.to_dict()}
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        with open(FileStorage._FileStorage__file_path,
                  "r", encoding="utf-8") as file:
            self.assertEqual(len(file.read()), len(json.dumps(d)))
            file.seek(0)
            self.assertEqual(json.load(file), d)

    def test_save_no_args(self):
        """Tests save() with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            BaseModel.save()
        message = "save() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), message)

    def test_save_excess_args(self):
        """Tests save() with too many arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as e:
            BaseModel.save(self, 45)
        message = "save() takes 1 positional argument but 2 were given"
        self.assertEqual(str(e.exception), message)

    def test_str(self):
        """Test method for str representation"""
        b = BaseModel()
        string = f"[{type(b).__name__}] ({b.id}) {b.__dict__}"
        self.assertEqual(b.__str__(), string)


if __name__ == "__main__":
    unittest.main()
