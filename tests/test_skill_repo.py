import unittest

from src.storage.models import Base
from src.storage.repositories.skill_repo import SkillRepo
from tests.conf_log_test import BaseTestCase


class TestSkillRepo(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill_repo = SkillRepo(isTest=True)

        Base.metadata.create_all(cls.skill_repo.db.engine)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(cls.skill_repo.db.engine)

    def setUp(self):
        skills = self.skill_repo.get_all()
        for skill in skills:
            self.skill_repo.delete(skill.id)

    def test_create(self):
        skill_id = self.skill_repo.create("Python")
        self.assertIsInstance(skill_id, int)
        self.assertGreater(skill_id, 0)

    def test_get_by_id(self):
        skill_id = self.skill_repo.create("JavaScript")
        skill = self.skill_repo.get_by_id(skill_id)
        self.assertIsNotNone(skill)
        self.assertEqual(skill.name, "JavaScript")

    def test_get_by_id_not_found(self):
        skill = self.skill_repo.get_by_id(999)
        self.assertIsNone(skill)

    def test_get_all(self):
        self.skill_repo.create("Python")
        self.skill_repo.create("SQL")
        skills = self.skill_repo.get_all()
        self.assertEqual(len(skills), 2)
        self.assertEqual(skills[0].name, "Python")
        self.assertEqual(skills[1].name, "SQL")

    def test_update(self):
        skill_id = self.skill_repo.create("Old Name")
        updated_skill = self.skill_repo.update(skill_id, name="New Name")
        self.assertEqual(updated_skill.name, "New Name")

    def test_update_not_found(self):
        with self.assertRaises(ValueError):
            self.skill_repo.update(999, name="Fail")

    def test_delete(self):
        skill_id = self.skill_repo.create("To Delete")
        result = self.skill_repo.delete(skill_id)
        self.assertTrue(result)
        skill = self.skill_repo.get_by_id(skill_id)
        self.assertIsNone(skill)

    def test_delete_not_found(self):
        with self.assertRaises(ValueError):
            self.skill_repo.delete(999)


if __name__ == "__main__":
    unittest.main()
