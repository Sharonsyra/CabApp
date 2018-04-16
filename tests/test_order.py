import unittest
import os
import json
from app.orders.views import create_app, db

class OrderTestCase(unittest.TestCase):
    """This class represents the order test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.order = {'name': 'Go to Radisson Blu'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_order_creation(self):
        """Test API can create a order (POST request)"""
        res = self.client().post('/orders/', data=self.order)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Go to Radisson Blu', str(res.data))

    def test_api_can_get_all_orders(self):
        """Test API can get a order (GET request)."""
        res = self.client().post('/orders/', data=self.order)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/orders/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to Radisson Blu', str(res.data))

    def test_api_can_get_order_by_id(self):
        """Test API can get a single order by using it's id."""
        rv = self.client().post('/orders/', data=self.order)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/orders/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to Radisson Blu', str(result.data))

    def test_order_can_be_edited(self):
        """Test API can edit an existing order. (PUT request)"""
        rv = self.client().post(
            '/orders/',
            data={'name': 'Go to Kisumu'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/orders/1',
            data={
                "name": "Go to Kisumu Dala"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/orders/1')
        self.assertIn('Dala', str(results.data))

    def test_order_deletion(self):
        """Test API can delete an existing order. (DELETE request)."""
        rv = self.client().post(
            '/orders/',
            data={'name': 'Go to Kisumu'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/orders/1')
        self.assertEqual(res.status_code, 200)
        result = self.client().get('/orders/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()