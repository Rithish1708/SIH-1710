"""
RailNav AI – Smart Railway Station Navigation and Assistance System
SIH 1710 Flask Web Application
"""
import os
import io
from flask import Flask, render_template, request, jsonify, send_file
from models import db, Station, Node, Edge, Facility, TrainSchedule, AssistanceRequest
from pathfinder import StationGraph
from seed_data import seed_database
import qrcode

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'railnav.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sih-railnav-ai-secure-key-2026'

db.init_app(app)

# Initialize database on startup
with app.app_context():
    db.create_all()
    seed_database()


def get_station_graph(station_id='NDLS'):
    """Builds an in-memory graph for Dijkstra/A* pathfinding"""
    nodes = Node.query.filter_by(station_id=station_id).all()
    edges = Edge.query.filter_by(station_id=station_id).all()
    
    nodes_dict = {n.id: n.to_dict() for n in nodes}
    edges_list = [e.to_dict() for e in edges]
    return StationGraph(nodes_dict, edges_list)


# --- HTML PAGE ROUTES ---

@app.route('/')
def index():
    """Main Passenger Navigation View (Mobile & Kiosk responsive)"""
    station_id = request.args.get('station', 'NDLS')
    station = db.session.get(Station, station_id) or Station.query.first()
    stations = Station.query.all()
    return render_template('index.html', current_station=station, stations=stations)


@app.route('/admin')
def admin():
    """Station Management & Facility Operations Dashboard"""
    station_id = request.args.get('station', 'NDLS')
    station = db.session.get(Station, station_id) or Station.query.first()
    stations = Station.query.all()
    return render_template('admin.html', current_station=station, stations=stations)


@app.route('/qr-codes')
def qr_codes():
    """Station Checkpoint QR Code Generation & Kiosk Display Sheet"""
    station_id = request.args.get('station', 'NDLS')
    station = db.session.get(Station, station_id) or Station.query.first()
    nodes = Node.query.filter_by(station_id=station.id).all()
    return render_template('qr_codes.html', current_station=station, nodes=nodes)


# --- REST API ENDPOINTS ---

@app.route('/api/stations', methods=['GET'])
def api_stations():
    stations = Station.query.all()
    return jsonify([s.to_dict() for s in stations])


@app.route('/api/nodes', methods=['GET'])
def api_nodes():
    station_id = request.args.get('station_id', 'NDLS')
    nodes = Node.query.filter_by(station_id=station_id).all()
    return jsonify([n.to_dict() for n in nodes])


@app.route('/api/edges', methods=['GET'])
def api_edges():
    station_id = request.args.get('station_id', 'NDLS')
    edges = Edge.query.filter_by(station_id=station_id).all()
    return jsonify([e.to_dict() for e in edges])


@app.route('/api/facilities', methods=['GET'])
def api_facilities():
    station_id = request.args.get('station_id', 'NDLS')
    category = request.args.get('category')
    query_str = request.args.get('search', '').strip().lower()

    query = Facility.query.filter_by(station_id=station_id)
    if category and category != 'all':
        query = query.filter_by(category=category)

    facilities = query.all()
    if query_str:
        facilities = [
            f for f in facilities
            if query_str in f.name.lower() or query_str in f.category.lower() or query_str in f.details.lower()
        ]

    return jsonify([f.to_dict() for f in facilities])


@app.route('/api/trains', methods=['GET'])
def api_trains():
    station_id = request.args.get('station_id', 'NDLS')
    trains = TrainSchedule.query.filter_by(station_id=station_id).order_by(TrainSchedule.departure_time).all()
    return jsonify([t.to_dict() for t in trains])


@app.route('/api/route', methods=['GET'])
def api_route():
    """
    Computes shortest optimal path between two nodes.
    Supports wheelchair accessibility mode and dynamic avoidance of blocked pathways.
    """
    station_id = request.args.get('station_id', 'NDLS')
    start_id = request.args.get('from')
    end_id = request.args.get('to')
    wheelchair = request.args.get('wheelchair', 'false').lower() == 'true'
    algo = request.args.get('algo', 'a_star')

    if not start_id or not end_id:
        return jsonify({'success': False, 'error': 'Missing start (from) or end (to) node ID.'}), 400

    graph = get_station_graph(station_id)
    result = graph.find_shortest_path(start_id, end_id, wheelchair_only=wheelchair, algorithm=algo)
    return jsonify(result)


@app.route('/api/qr_resolve', methods=['GET'])
def api_qr_resolve():
    """Resolves a scanned QR code token to the corresponding node location"""
    token = request.args.get('code', '').strip()
    if not token:
        return jsonify({'success': False, 'error': 'No QR code provided.'}), 400

    node = Node.query.filter_by(qr_token=token).first()
    if not node:
        return jsonify({'success': False, 'error': f"Unknown checkpoint QR code: '{token}'."}), 404

    return jsonify({'success': True, 'node': node.to_dict()})


@app.route('/api/qr_image/<qr_token>', methods=['GET'])
def api_qr_image(qr_token):
    """Generates a high-quality branded PNG QR code on the fly"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=3,
    )
    qr.add_data(qr_token)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#0F172A", back_color="#FFFFFF")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')


@app.route('/api/assistance', methods=['GET', 'POST'])
def api_assistance():
    """SOS & Divyangjan Wheelchair / Porter Booking Requests"""
    if request.method == 'POST':
        data = request.json or request.form
        req = AssistanceRequest(
            station_id=data.get('station_id', 'NDLS'),
            request_type=data.get('request_type', 'wheelchair'),
            passenger_name=data.get('passenger_name', 'Anonymous Passenger'),
            contact_phone=data.get('contact_phone', 'Not provided'),
            pickup_node_id=data.get('pickup_node_id', 'ndls_gate1'),
            destination_node_id=data.get('destination_node_id'),
            status='pending',
            notes=data.get('notes', '')
        )
        db.session.add(req)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Assistance request logged! RPF and Sahayak station staff alerted.', 'request': req.to_dict()})

    # GET requests for admin
    station_id = request.args.get('station_id', 'NDLS')
    reqs = AssistanceRequest.query.filter_by(station_id=station_id).order_by(AssistanceRequest.id.desc()).all()
    return jsonify([r.to_dict() for r in reqs])


@app.route('/api/assistance/<int:req_id>/status', methods=['POST'])
def api_update_assistance_status(req_id):
    data = request.json or {}
    new_status = data.get('status', 'assigned')
    req = db.session.get(AssistanceRequest, req_id)
    if not req:
        return jsonify({'success': False, 'error': 'Request not found.'}), 404

    req.status = new_status
    db.session.commit()
    return jsonify({'success': True, 'request': req.to_dict()})


@app.route('/api/admin/facility/status', methods=['POST'])
def api_admin_facility_status():
    """Updates facility operational status (e.g. lift under maintenance)"""
    data = request.json or {}
    fac_id = data.get('facility_id')
    new_status = data.get('status', 'operational')

    fac = db.session.get(Facility, fac_id)
    if not fac:
        return jsonify({'success': False, 'error': 'Facility not found'}), 404

    fac.status = new_status
    db.session.commit()
    return jsonify({'success': True, 'facility': fac.to_dict()})


@app.route('/api/admin/edge/block', methods=['POST'])
def api_admin_edge_block():
    """Toggles pathway blocked status for maintenance or crowd management"""
    data = request.json or {}
    edge_id = data.get('edge_id')
    is_blocked = data.get('is_blocked', True)

    edge = db.session.get(Edge, edge_id)
    if not edge:
        return jsonify({'success': False, 'error': 'Edge not found'}), 404

    edge.is_blocked = is_blocked
    db.session.commit()
    return jsonify({'success': True, 'edge': edge.to_dict()})


@app.route('/api/admin/train/platform', methods=['POST'])
def api_admin_train_platform():
    """Updates train platform allocation"""
    data = request.json or {}
    train_id = data.get('train_id')
    new_plat = data.get('platform')

    train = db.session.get(TrainSchedule, train_id)
    if not train:
        return jsonify({'success': False, 'error': 'Train not found'}), 404

    train.platform = str(new_plat)
    db.session.commit()
    return jsonify({'success': True, 'train': train.to_dict()})


if __name__ == '__main__':
    print("Starting RailNav AI Server on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
