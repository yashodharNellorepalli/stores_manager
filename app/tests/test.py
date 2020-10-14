import json
import unittest

from app import app


class AppTest(unittest.TestCase):
    def test_get_api_status(self):
        tester = app.test_client(self)
        response = tester.get('/stores/api/status?job_id=1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, 'application/json')

    def test_get_api_visits(self):
        tester = app.test_client(self)
        response = tester.get('/stores/api/visits?startdate=2020-10-10&enddate=2020-10-20')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_get_api_visits_store_id_not_exist(self):
        tester = app.test_client(self)
        response = tester.get('/stores/api/visits?startdate=2020-10-10&enddate=2020-10-20&store=1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, 'application/json')

    def test_get_api_visits_store_id_exist(self):
        tester = app.test_client(self)
        response = tester.get('/stores/api/visits?startdate=2020-10-10&enddate=2020-10-20&store=S00339198')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_post_api_submit(self):
        tester = app.test_client(self)
        data = {
            "count": 2,
            "visits": [
                {
                    "store_id": "S00339218",
                    "image_url": [
                        "https://www.gstatic.com/webp/gallery/4.jpg",
                        "https://www.gstatic.com/webp/gallery/5.jpg"
                    ],
                    "visit_time": "2020-10-10 10:00:00"
                },
                {
                    "store_id": "S00339204",
                    "image_url": [
                        "https://www.gstatic.com/webp/gallery/1.jpg"
                    ],
                    "visit_time": "2020-10-10 10:00:00"
                }
            ]
        }
        response = tester.post('/stores/api/submit', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')

    def test_post_api_submit_count_mismatch_visits(self):
        tester = app.test_client(self)
        data = {
            "count": 20,
            "visits": [
                {
                    "store_id": "S00339218",
                    "image_url": [
                        "https://www.gstatic.com/webp/gallery/4.jpg",
                        "https://www.gstatic.com/webp/gallery/5.jpg"
                    ],
                    "visit_time": "2020-10-10 10:00:00"
                },
                {
                    "store_id": "S00339204",
                    "image_url": [
                        "https://www.gstatic.com/webp/gallery/1.jpg"
                    ],
                    "visit_time": "2020-10-10 10:00:00"
                }
            ]
        }
        response = tester.post('/stores/api/submit', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, 'application/json')


if __name__ == "__main__":
    unittest.main()
