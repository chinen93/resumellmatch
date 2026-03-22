import unittest

from src.storage.models import Base
from src.storage.repositories.job_repo import (
    JobDescriptionParsedRepo,
    JobDescriptionRepo,
)
from tests.conf_log_test import BaseTestCase


class TestJobDescriptionRepo(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.job_desc_repo = JobDescriptionRepo(isTest=True)

        Base.metadata.create_all(cls.job_desc_repo.db.engine)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        Base.metadata.drop_all(cls.job_desc_repo.db.engine)

    def setUp(self):
        jobs = self.job_desc_repo.get_all()
        for job in jobs:
            self.job_desc_repo.delete(job.id)

    def test_create(self):
        job_id = self.job_desc_repo.create("http://example.com", "Engineer", "Job text")
        self.assertIsInstance(job_id, int)
        self.assertGreater(job_id, 0)

    def test_get_by_id(self):
        job_id = self.job_desc_repo.create("http://example.com", "Engineer", "Job text")
        job = self.job_desc_repo.get_by_id(job_id)
        self.assertIsNotNone(job)
        self.assertEqual(job.title, "Engineer")

    def test_get_by_id_not_found(self):
        job = self.job_desc_repo.get_by_id(999)
        self.assertIsNone(job)

    def test_get_all(self):
        self.job_desc_repo.create("http://example.com", "Engineer", "Job text")
        self.job_desc_repo.create("http://example2.com", "Manager", "Job text 2")
        jobs = self.job_desc_repo.get_all()
        self.assertEqual(len(jobs), 2)
        self.assertEqual(jobs[0].title, "Engineer")
        self.assertEqual(jobs[1].title, "Manager")

    def test_update(self):
        job_id = self.job_desc_repo.create("http://example.com", "Engineer", "Job text")
        updated_job = self.job_desc_repo.update(job_id, title="Senior Engineer")
        self.assertEqual(updated_job.title, "Senior Engineer")

    def test_update_not_found(self):
        with self.assertRaises(ValueError):
            self.job_desc_repo.update(999, title="Fail")

    def test_delete(self):
        job_id = self.job_desc_repo.create("http://example.com", "Engineer", "Job text")
        result = self.job_desc_repo.delete(job_id)
        self.assertTrue(result)
        job = self.job_desc_repo.get_by_id(job_id)
        self.assertIsNone(job)

    def test_delete_not_found(self):
        with self.assertRaises(ValueError):
            self.job_desc_repo.delete(999)


class TestJobDescriptionParsedRepo(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.job_desc_repo = JobDescriptionRepo(isTest=True)
        cls.job_desc_parsed_repo = JobDescriptionParsedRepo(isTest=True)

        Base.metadata.create_all(cls.job_desc_parsed_repo.db.engine)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        Base.metadata.drop_all(cls.job_desc_parsed_repo.db.engine)

    def setUp(self):
        jobs_parsed = self.job_desc_parsed_repo.get_all()
        for job in jobs_parsed:
            self.job_desc_parsed_repo.delete(job.id)

        jobs = self.job_desc_repo.get_all()
        for job in jobs:
            self.job_desc_repo.delete(job.id)

    def test_create(self):
        job_id = self.job_desc_repo.create("http://example.com", "Engineer", "Job text")
        parsed_id = self.job_desc_parsed_repo.create(
            job_id, "Summary", "skill1,skill2", "skill3", "keyword1,keyword2"
        )
        self.assertIsInstance(parsed_id, int)
        self.assertGreater(parsed_id, 0)

    def test_get_by_id(self):
        job_id = self.job_desc_repo.create("http://example.com", "Engineer", "Job text")
        parsed_id = self.job_desc_parsed_repo.create(
            job_id, "Summary", "skill1,skill2", "skill3", "keyword1,keyword2"
        )
        parsed = self.job_desc_parsed_repo.get_by_id(parsed_id)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed.summary, "Summary")

    def test_get_by_job_id(self):
        job_id = self.job_desc_repo.create("http://example.com", "Engineer", "Job text")
        _ = self.job_desc_parsed_repo.create(
            job_id, "Summary", "skill1,skill2", "skill3", "keyword1,keyword2"
        )
        parsed = self.job_desc_parsed_repo.get_by_job_id(job_id)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed.summary, "Summary")

    def test_get_all(self):
        job_id1 = self.job_desc_repo.create(
            "http://example.com", "Engineer", "Job text"
        )
        self.job_desc_parsed_repo.create(
            job_id1, "Summary1", "skill1", "skill2", "keyword1"
        )
        job_id2 = self.job_desc_repo.create(
            "http://example2.com", "Manager", "Job text 2"
        )
        self.job_desc_parsed_repo.create(
            job_id2, "Summary2", "skill3", "skill4", "keyword2"
        )
        parseds = self.job_desc_parsed_repo.get_all()
        self.assertEqual(len(parseds), 2)
        self.assertEqual(parseds[0].summary, "Summary1")
        self.assertEqual(parseds[1].summary, "Summary2")

    def test_update(self):
        job_id = self.job_desc_repo.create("http://example.com", "Engineer", "Job text")
        parsed_id = self.job_desc_parsed_repo.create(
            job_id, "Summary", "skill1,skill2", "skill3", "keyword1,keyword2"
        )
        updated_parsed = self.job_desc_parsed_repo.update(
            parsed_id, summary="Updated Summary"
        )
        self.assertEqual(updated_parsed.summary, "Updated Summary")

    def test_update_not_found(self):
        with self.assertRaises(ValueError):
            self.job_desc_parsed_repo.update(999, summary="Fail")

    def test_delete(self):
        job_id = self.job_desc_repo.create("http://example.com", "Engineer", "Job text")
        parsed_id = self.job_desc_parsed_repo.create(
            job_id, "Summary", "skill1,skill2", "skill3", "keyword1,keyword2"
        )
        result = self.job_desc_parsed_repo.delete(parsed_id)
        self.assertTrue(result)
        parsed = self.job_desc_parsed_repo.get_by_id(parsed_id)
        self.assertIsNone(parsed)

    def test_delete_not_found(self):
        with self.assertRaises(ValueError):
            self.job_desc_parsed_repo.delete(999)


if __name__ == "__main__":
    unittest.main()
