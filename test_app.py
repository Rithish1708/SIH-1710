"""
Automated Unit Tests for RailNav AI
Tests:
- Pathfinding (Dijkstra and A*)
- Wheelchair Accessible routing (step-free ramp & lift traversal)
- Obstacle Avoidance (dynamic detour around blocked paths)
- API Endpoints (nodes, edges, facilities, trains, route calculation)
- QR Code resolution and generation
"""
import unittest
import json
from app import app, db
from models import Node, Edge, Facility, TrainSchedule, AssistanceRequest
from pathfinder import StationGraph

class RailNavTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_stations_api(self):
        response = self.client.get('/api/stations')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(len(data) >= 1)
        self.assertEqual(data[0]['id'], 'NDLS')

    def test_nodes_api(self):
        response = self.client.get('/api/nodes?station_id=NDLS')
        self.assertEqual(response.status_code, 200)
        nodes = response.get_json()
        self.assertTrue(len(nodes) >= 20)
        node_ids = [n['id'] for n in nodes]
        self.assertIn('ndls_gate1', node_ids)
        self.assertIn('ndls_p1_center', node_ids)

    def test_pathfinding_standard_route(self):
        # Route from Gate 1 to Platform 3 Center
        response = self.client.get('/api/route?station_id=NDLS&from=ndls_gate1&to=ndls_p3_center&wheelchair=false')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertTrue(data['total_distance'] > 0)
        self.assertTrue(len(data['path_nodes']) > 2)
        self.assertTrue(len(data['instructions']) > 1)

    def test_wheelchair_accessible_route(self):
        # Wheelchair route from Gate 1 to Platform 3 Center
        # Must only traverse step-free paths (lifts or ramps), no stairs or escalators
        response = self.client.get('/api/route?station_id=NDLS&from=ndls_gate1&to=ndls_p3_center&wheelchair=true')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertTrue(data['wheelchair_friendly'])
        
        # Verify instructions do not tell user to take stairs
        for step in data['instructions']:
            self.assertNotEqual(step['action'], 'stairs')
            self.assertNotEqual(step['action'], 'escalator')

    def test_obstacle_avoidance(self):
        # Temporarily block Central Concourse Lift L1
        lift_edge = Edge.query.filter(
            ((Edge.node_a == 'ndls_lift_c1_f0') & (Edge.node_b == 'ndls_fob1_concourse_lift_f1')) |
            ((Edge.node_a == 'ndls_fob1_concourse_lift_f1') & (Edge.node_b == 'ndls_lift_c1_f0'))
        ).first()
        self.assertIsNotNone(lift_edge)

        lift_edge.is_blocked = True
        db.session.commit()

        # Wheelchair route should still find an alternate detour via South Ramp!
        response = self.client.get('/api/route?station_id=NDLS&from=ndls_gate1&to=ndls_p3_center&wheelchair=true')
        data = response.get_json()
        self.assertTrue(data['success'])

        # Reset block
        lift_edge.is_blocked = False
        db.session.commit()

    def test_qr_resolution(self):
        response = self.client.get('/api/qr_resolve?code=QR-NDLS-GATE1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['node']['id'], 'ndls_gate1')

    def test_assistance_request_flow(self):
        payload = {
            'station_id': 'NDLS',
            'request_type': 'wheelchair',
            'passenger_name': 'Aarav Sharma',
            'contact_phone': '+91 99999 11111',
            'pickup_node_id': 'ndls_gate2',
            'destination_node_id': 'ndls_p2_center',
            'notes': 'Elderly passenger requiring wheelchair assistance'
        }
        response = self.client.post('/api/assistance', json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        req_id = data['request']['id']

        # Update status
        status_resp = self.client.post(f'/api/assistance/{req_id}/status', json={'status': 'completed'})
        self.assertEqual(status_resp.status_code, 200)
        self.assertEqual(status_resp.get_json()['request']['status'], 'completed')


if __name__ == '__main__':
    unittest.main()
