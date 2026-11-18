"""REST API behavior tests."""
import unittest

from service import create_app, _ACCOUNTS


class CustomerAccountsTests(unittest.TestCase):
    def setUp(self):
        _ACCOUNTS.clear()
        self.app = create_app({"TESTING": True})
        self.client = self.app.test_client()

    def create_one(self):
        return self.client.post(
            "/accounts",
            json={"name": "Asha Rao", "email": "asha@example.com"},
        )

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")

    def test_create_and_read(self):
        created = self.create_one()
        self.assertEqual(created.status_code, 201)
        account_id = created.json["id"]
        read = self.client.get("/accounts/" + account_id)
        self.assertEqual(read.status_code, 200)
        self.assertEqual(read.json["email"], "asha@example.com")

    def test_list(self):
        self.create_one()
        response = self.client.get("/accounts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_missing_required_fields(self):
        response = self.client.post("/accounts", json={"name": "Asha"})
        self.assertEqual(response.status_code, 400)

    def test_duplicate_email(self):
        self.create_one()
        response = self.client.post(
            "/accounts",
            json={"name": "Another", "email": "ASHA@example.com"},
        )
        self.assertEqual(response.status_code, 409)

    def test_update(self):
        account_id = self.create_one().json["id"]
        response = self.client.put(
            "/accounts/" + account_id,
            json={"name": "Asha R", "status": "inactive"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Asha R")
        self.assertEqual(response.json["status"], "inactive")

    def test_delete_and_not_found(self):
        account_id = self.create_one().json["id"]
        deleted = self.client.delete("/accounts/" + account_id)
        self.assertEqual(deleted.status_code, 204)
        missing = self.client.get("/accounts/" + account_id)
        self.assertEqual(missing.status_code, 404)

    def test_security_headers_present(self):
        response = self.client.get("/health")
        self.assertIn("X-Content-Type-Options", response.headers)
        self.assertIn("X-Frame-Options", response.headers)


if __name__ == "__main__":
    unittest.main()
