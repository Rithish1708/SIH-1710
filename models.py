"""
Database Models for RailNav AI
Railway Station Facility & Indoor Navigation System
"""
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Station(db.Model):
    __tablename__ = 'stations'
    
    id = db.Column(db.String(32), primary_key=True)  # e.g., 'NDLS', 'MAS'
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    division = db.Column(db.String(64), default='Northern Railway')
    lat = db.Column(db.Float, default=28.6429)
    lng = db.Column(db.Float, default=77.2195)
    floors_count = db.Column(db.Integer, default=2)
    description = db.Column(db.Text, default='Major Junction Railway Station')

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'city': self.city,
            'division': self.division,
            'lat': self.lat,
            'lng': self.lng,
            'floors_count': self.floors_count,
            'description': self.description
        }


class Node(db.Model):
    """
    Waypoints and facility locations within station premises
    """
    __tablename__ = 'nodes'
    
    id = db.Column(db.String(64), primary_key=True)
    station_id = db.Column(db.String(32), db.ForeignKey('stations.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(32), nullable=False)  # gate, platform, ticket, food, restroom, lounge, lift, escalator, ramp, stairs, medical, police, water, atm, kiosk, walkway
    floor = db.Column(db.Integer, default=0)             # 0: Ground/Platform, 1: Foot Overbridge / Skywalk
    x = db.Column(db.Float, nullable=False)              # SVG/Indoor map coordinate X
    y = db.Column(db.Float, nullable=False)              # SVG/Indoor map coordinate Y
    lat = db.Column(db.Float, nullable=True)             # Geographic latitude
    lng = db.Column(db.Float, nullable=True)             # Geographic longitude
    is_accessible = db.Column(db.Boolean, default=True)  # Wheelchair/Step-free accessible
    description = db.Column(db.String(256), default='')
    qr_token = db.Column(db.String(64), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'station_id': self.station_id,
            'name': self.name,
            'category': self.category,
            'floor': self.floor,
            'x': self.x,
            'y': self.y,
            'lat': self.lat,
            'lng': self.lng,
            'is_accessible': self.is_accessible,
            'description': self.description,
            'qr_token': self.qr_token
        }


class Edge(db.Model):
    """
    Pathways connecting waypoints/nodes
    """
    __tablename__ = 'edges'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    station_id = db.Column(db.String(32), db.ForeignKey('stations.id'), nullable=False)
    node_a = db.Column(db.String(64), nullable=False)
    node_b = db.Column(db.String(64), nullable=False)
    distance = db.Column(db.Float, nullable=False)  # Distance in meters
    pathway_type = db.Column(db.String(32), default='walkway')  # walkway, ramp, elevator, escalator, stairs, bridge
    is_wheelchair_accessible = db.Column(db.Boolean, default=True)
    is_blocked = db.Column(db.Boolean, default=False)  # Admin maintenance/crowd block
    congestion_level = db.Column(db.String(16), default='low')  # low, medium, high
    bidirectional = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(256), default='')

    def to_dict(self):
        return {
            'id': self.id,
            'station_id': self.station_id,
            'node_a': self.node_a,
            'node_b': self.node_b,
            'distance': self.distance,
            'pathway_type': self.pathway_type,
            'is_wheelchair_accessible': self.is_wheelchair_accessible,
            'is_blocked': self.is_blocked,
            'congestion_level': self.congestion_level,
            'bidirectional': self.bidirectional,
            'description': self.description
        }


class Facility(db.Model):
    """
    Passenger Amenities and Services mapped to nodes
    """
    __tablename__ = 'facilities'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    station_id = db.Column(db.String(32), db.ForeignKey('stations.id'), nullable=False)
    node_id = db.Column(db.String(64), db.ForeignKey('nodes.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(32), nullable=False)  # platform, ticket, restroom, food, waiting_hall, lift, escalator, medical, police, water, atm, cloak_room, helpdesk
    icon = db.Column(db.String(32), default='fa-map-marker-alt')
    floor = db.Column(db.Integer, default=0)
    operating_hours = db.Column(db.String(64), default='24 Hours')
    status = db.Column(db.String(32), default='operational')  # operational, maintenance, crowded
    details = db.Column(db.Text, default='')

    def to_dict(self):
        return {
            'id': self.id,
            'station_id': self.station_id,
            'node_id': self.node_id,
            'name': self.name,
            'category': self.category,
            'icon': self.icon,
            'floor': self.floor,
            'operating_hours': self.operating_hours,
            'status': self.status,
            'details': self.details
        }


class TrainSchedule(db.Model):
    """
    Live Train Arrival/Departure Schedule
    """
    __tablename__ = 'train_schedules'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    station_id = db.Column(db.String(32), db.ForeignKey('stations.id'), nullable=False)
    train_number = db.Column(db.String(16), nullable=False)
    train_name = db.Column(db.String(128), nullable=False)
    train_type = db.Column(db.String(32), default='Superfast Express')
    platform = db.Column(db.String(8), nullable=False)
    arrival_time = db.Column(db.String(16), default='12:30')
    departure_time = db.Column(db.String(16), default='12:45')
    status = db.Column(db.String(32), default='On Time')  # On Time, Delayed, Arrived, Boarding Now
    delay_minutes = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'station_id': self.station_id,
            'train_number': self.train_number,
            'train_name': self.train_name,
            'train_type': self.train_type,
            'platform': self.platform,
            'arrival_time': self.arrival_time,
            'departure_time': self.departure_time,
            'status': self.status,
            'delay_minutes': self.delay_minutes
        }


class AssistanceRequest(db.Model):
    """
    SOS and Passenger Special Assistance Requests
    """
    __tablename__ = 'assistance_requests'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    station_id = db.Column(db.String(32), db.ForeignKey('stations.id'), nullable=False)
    request_type = db.Column(db.String(32), default='wheelchair')  # wheelchair, medical_emergency, sahayak_porter, visual_guide
    passenger_name = db.Column(db.String(64), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    pickup_node_id = db.Column(db.String(64), nullable=False)
    destination_node_id = db.Column(db.String(64), nullable=True)
    status = db.Column(db.String(32), default='pending')  # pending, assigned, completed
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    notes = db.Column(db.Text, default='')

    def to_dict(self):
        return {
            'id': self.id,
            'station_id': self.station_id,
            'request_type': self.request_type,
            'passenger_name': self.passenger_name,
            'contact_phone': self.contact_phone,
            'pickup_node_id': self.pickup_node_id,
            'destination_node_id': self.destination_node_id,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else '',
            'notes': self.notes
        }
