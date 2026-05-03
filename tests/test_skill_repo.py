import unittest

from src.storage.models import Base
from src.storage.repositories import SkillRepo
from tests.conf_log_test import BaseTestCase


class TestSkillRepo(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.skill_repo = SkillRepo(isTest=True)

        engine = cls.skill_repo.db.engine
        assert engine is not None

        Base.metadata.create_all(engine)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        engine = cls.skill_repo.db.engine
        assert engine is not None

        Base.metadata.drop_all(engine)

    def setUp(self):
        skills = self.skill_repo.get_all()
        for skill in skills:
            assert skill.id is not None
            self.skill_repo.delete(skill.id)

    def test_create(self):
        skill_id = self.skill_repo.create_from_fields(1, "Python")
        self.assertIsInstance(skill_id, int)
        self.assertGreater(skill_id, 0)

    def test_get_by_id(self):
        skill_id = self.skill_repo.create_from_fields(2, "JavaScript")
        skill = self.skill_repo.get_by_id(skill_id)
        self.assertIsNotNone(skill)
        assert skill is not None
        self.assertEqual(skill.name, "JavaScript")

    def test_get_by_id_not_found(self):
        skill = self.skill_repo.get_by_id(999)
        self.assertIsNone(skill)

    def test_get_all(self):
        self.skill_repo.create_from_fields(1, "Python")
        self.skill_repo.create_from_fields(2, "SQL")
        skills = self.skill_repo.get_all()
        self.assertEqual(len(skills), 2)
        self.assertEqual(skills[0].name, "Python")
        self.assertEqual(skills[1].name, "SQL")

    def test_update(self):
        skill_id = self.skill_repo.create_from_fields(1, "Old Name")

        skill = self.skill_repo.get_by_id(skill_id)
        assert skill is not None

        skill.name = "New Name"
        self.skill_repo.create_or_update(skill)
        updated_skill = self.skill_repo.get_by_id(skill_id)

        assert updated_skill is not None
        self.assertEqual(updated_skill.name, "New Name")

    def test_update_not_found(self):
        result = self.skill_repo.delete(999)
        self.assertFalse(result)

    def test_delete(self):
        skill_id = self.skill_repo.create_from_fields(1, "To Delete")
        result = self.skill_repo.delete(skill_id)
        self.assertTrue(result)
        skill = self.skill_repo.get_by_id(skill_id)
        self.assertIsNone(skill)

    def test_delete_not_found(self):
        result = self.skill_repo.delete(999)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
