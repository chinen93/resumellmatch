import unittest
from datetime import date

from sqlalchemy import create_engine

from src.storage.models import Base
from src.storage.repositories.skill_repo import SkillRepo
from src.storage.repositories.star_repo import StarEntryRepo, StarMetadataRepo
from src.storage.repositories.user_repo import UserRepo


class TestStarMetadataRepo(unittest.TestCase):
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

        users = UserRepo.get_all()
        for user in users:
            UserRepo.delete(user.id)

        # Create a test user
        self.user_id = UserRepo.create("Test User", "test@example.com")

    def test_create(self):
        user = UserRepo.get_by_id(user_id=self.user_id)
        self.assertEqual(len(user.star_metadatas), 0)

        start = date(2020, 1, 1)
        end = date(2023, 12, 31)
        star_id = StarMetadataRepo.create(
            user_id=self.user_id,
            type="work",
            title="Engineer",
            subtitle="Company",
            location="City",
            start_date=start,
            end_date=end,
        )
        self.assertIsInstance(star_id, int)
        self.assertGreater(star_id, 0)

        user = UserRepo.get_by_id(user_id=self.user_id)
        self.assertEqual(user.star_metadatas[0].id, star_id)

    def test_get_by_id(self):
        start = date(2020, 1, 1)
        end = date(2023, 12, 31)
        star_id = StarMetadataRepo.create(
            user_id=self.user_id,
            type="work",
            title="Engineer",
            subtitle="Company",
            location="City",
            start_date=start,
            end_date=end,
        )
        star = StarMetadataRepo.get_by_id(star_id)
        self.assertIsNotNone(star)
        self.assertEqual(star.title, "Engineer")
        self.assertEqual(star.user_id, self.user_id)

    def test_get_by_id_not_found(self):
        star = StarMetadataRepo.get_by_id(999)
        self.assertIsNone(star)

    def test_get_all(self):
        start1 = date(2020, 1, 1)
        end1 = date(2023, 12, 31)
        StarMetadataRepo.create(
            user_id=self.user_id,
            type="work",
            title="Engineer",
            subtitle="Company",
            location="City",
            start_date=start1,
            end_date=end1,
        )
        start2 = date(2018, 6, 1)
        end2 = date(2019, 12, 31)
        StarMetadataRepo.create(
            user_id=self.user_id,
            type="education",
            title="Degree",
            subtitle="University",
            location="Town",
            start_date=start2,
            end_date=end2,
        )
        stars = StarMetadataRepo.get_all(self.user_id)
        self.assertEqual(len(stars), 2)
        self.assertEqual(stars[0].title, "Engineer")
        self.assertEqual(stars[1].title, "Degree")

    def test_update(self):
        start = date(2020, 1, 1)
        end = date(2023, 12, 31)
        star_id = StarMetadataRepo.create(
            user_id=self.user_id,
            type="work",
            title="Engineer",
            subtitle="Company",
            location="City",
            start_date=start,
            end_date=end,
        )
        new_end = date(2024, 1, 1)
        updated_star = StarMetadataRepo.update(
            star_id, title="Senior Engineer", end_date=new_end
        )
        self.assertEqual(updated_star.title, "Senior Engineer")
        self.assertEqual(updated_star.end_date, new_end)

    def test_update_not_found(self):
        with self.assertRaises(ValueError):
            StarMetadataRepo.update(999, title="Fail")

    def test_delete(self):
        start = date(2020, 1, 1)
        end = date(2023, 12, 31)
        star_id = StarMetadataRepo.create(
            user_id=self.user_id,
            type="work",
            title="Engineer",
            subtitle="Company",
            location="City",
            start_date=start,
            end_date=end,
        )
        result = StarMetadataRepo.delete(star_id)
        self.assertTrue(result)
        star = StarMetadataRepo.get_by_id(star_id)
        self.assertIsNone(star)

    def test_delete_not_found(self):
        with self.assertRaises(ValueError):
            StarMetadataRepo.delete(999)


class TestStarEntryRepo(unittest.TestCase):
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

        users = UserRepo.get_all()
        for user in users:
            UserRepo.delete(user.id)

        # Create a test user and star_metadata
        self.user_id = UserRepo.create("Test User", "test@example.com")
        start = date(2020, 1, 1)
        end = date(2023, 12, 31)
        self.star_metadata_id = StarMetadataRepo.create(
            user_id=self.user_id,
            type="work",
            title="Engineer",
            subtitle="Company",
            location="City",
            start_date=start,
            end_date=end,
        )

        self.skill_id_1 = SkillRepo.create("Python")
        self.skill_id_2 = SkillRepo.create("Python3")

    def test_create(self):
        entry_id = StarEntryRepo.create(
            metadata_id=self.star_metadata_id,
            title="Project A",
            situation="Situation",
            task="Task",
            action="Action",
            result="Result",
            skills=[self.skill_id_1, self.skill_id_2],
        )
        self.assertIsInstance(entry_id, int)
        self.assertGreater(entry_id, 0)

    def test_get_by_id(self):
        entry_id = StarEntryRepo.create(
            metadata_id=self.star_metadata_id,
            title="Project B",
            situation="Situation",
            task="Task",
            action="Action",
            result="Result",
            skills=[self.skill_id_1, self.skill_id_2],
        )
        entry = StarEntryRepo.get_by_id(entry_id)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.title, "Project B")
        self.assertEqual(entry.metadata_id, self.star_metadata_id)

    def test_get_by_id_not_found(self):
        entry = StarEntryRepo.get_by_id(999)
        self.assertIsNone(entry)

    def test_get_all(self):
        StarEntryRepo.create(
            metadata_id=self.star_metadata_id,
            title="Entry1",
            situation="Sit1",
            task="Task1",
            action="Act1",
            result="Res1",
        )
        StarEntryRepo.create(
            metadata_id=self.star_metadata_id,
            title="Entry2",
            situation="Sit2",
            task="Task2",
            action="Act2",
            result="Res2",
        )
        entries = StarEntryRepo.get_all(self.star_metadata_id)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0].title, "Entry1")
        self.assertEqual(entries[1].title, "Entry2")

    def test_update(self):
        entry_id = StarEntryRepo.create(
            metadata_id=self.star_metadata_id,
            title="Old Title",
            situation="Old Sit",
            task="Old Task",
            action="Old Act",
            result="Old Res",
        )
        updated_entry = StarEntryRepo.update(
            entry_id, title="New Title", result="New Res"
        )
        self.assertEqual(updated_entry.title, "New Title")
        self.assertEqual(updated_entry.result, "New Res")

    def test_update_not_found(self):
        with self.assertRaises(ValueError):
            StarEntryRepo.update(999, title="Fail")

    def test_delete(self):
        entry_id = StarEntryRepo.create(
            metadata_id=self.star_metadata_id,
            title="To Delete",
            situation="Sit",
            task="Task",
            action="Action",
            result="Result",
        )
        result = StarEntryRepo.delete(entry_id)
        self.assertTrue(result)
        entry = StarEntryRepo.get_by_id(entry_id)
        self.assertIsNone(entry)

    def test_delete_not_found(self):
        with self.assertRaises(ValueError):
            StarEntryRepo.delete(999)


if __name__ == "__main__":
    unittest.main()
