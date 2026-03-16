import unittest

from sqlalchemy import create_engine

from src.storage.models import Base
from src.storage.repositories.skill_repo import SkillRepo


class TestSkillRepo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a test database
        cls.engine = create_engine("sqlite:///./output/test_storage.db", echo=False)
        Base.metadata.create_all(cls.engine)
        # Override the db instance for tests
        from src.storage import connection

        connection.DatabaseConnection._instance = None  # Reset singleton
        connection.DatabaseConnection._instance = connection.DatabaseConnection()
        connection.DatabaseConnection._instance.engine = cls.engine

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(cls.engine)

    def setUp(self):
        skills = SkillRepo.get_all()
        for skill in skills:
            SkillRepo.delete(skill.id)

    def test_create(self):
        skill_id = SkillRepo.create("Python")
        self.assertIsInstance(skill_id, int)
        self.assertGreater(skill_id, 0)

    def test_get_by_id(self):
        skill_id = SkillRepo.create("JavaScript")
        skill = SkillRepo.get_by_id(skill_id)
        self.assertIsNotNone(skill)
        self.assertEqual(skill.name, "JavaScript")

    def test_get_by_id_not_found(self):
        skill = SkillRepo.get_by_id(999)
        self.assertIsNone(skill)

    def test_get_all(self):
        SkillRepo.create("Python")
        SkillRepo.create("SQL")
        skills = SkillRepo.get_all()
        self.assertEqual(len(skills), 2)
        self.assertEqual(skills[0].name, "Python")
        self.assertEqual(skills[1].name, "SQL")

    def test_update(self):
        skill_id = SkillRepo.create("Old Name")
        updated_skill = SkillRepo.update(skill_id, name="New Name")
        self.assertEqual(updated_skill.name, "New Name")

    def test_update_not_found(self):
        with self.assertRaises(ValueError):
            SkillRepo.update(999, name="Fail")

    def test_delete(self):
        skill_id = SkillRepo.create("To Delete")
        result = SkillRepo.delete(skill_id)
        self.assertTrue(result)
        skill = SkillRepo.get_by_id(skill_id)
        self.assertIsNone(skill)

    def test_delete_not_found(self):
        with self.assertRaises(ValueError):
            SkillRepo.delete(999)


if __name__ == "__main__":
    unittest.main()
