import unittest
from app import app

class WebTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    def test_home(self):
        self.assertEqual(self.client.get("/").status_code, 200)
    def test_routes(self):
        for dest, battery, stations, expected in [(25,10,[4,8,12,17],2),(10,10,[],0),(30,10,[8,20],None)]:
            response = self.client.post("/api/plan", json={"destination_km":dest,"range_km":battery,"station_km":stations})
            self.assertEqual(response.status_code,200)
            self.assertTrue(all(r["count"] == expected for r in response.json["results"]))
    def test_invalid(self):
        self.assertEqual(self.client.post("/api/plan",json={"destination_km":10,"range_km":0,"station_km":[]}).status_code,400)

if __name__ == "__main__":
    unittest.main()
