"""
Seed Data for RailNav AI
Populates stations, nodes, edges, facilities, and live train schedules.
"""
from models import db, Station, Node, Edge, Facility, TrainSchedule, AssistanceRequest

def seed_database():
    """Populates initial database if empty"""
    if Station.query.first():
        print("Database already seeded.")
        return

    print("Seeding RailNav AI database...")

    # 1. Main Station: New Delhi Central (NDLS)
    ndls = Station(
        id='NDLS',
        code='NDLS',
        name='New Delhi Railway Station',
        city='New Delhi',
        division='Northern Railway',
        lat=28.6429,
        lng=77.2195,
        floors_count=2,
        description='One of the busiest railway stations in India with 16 platforms, handling over 500,000 passengers daily.'
    )

    # Secondary Station: Puratchi Thalaivar Dr. M.G. Ramachandran Central (MAS)
    mas = Station(
        id='MAS',
        code='MAS',
        name='Chennai Central Railway Station',
        city='Chennai',
        division='Southern Railway',
        lat=13.0827,
        lng=80.2707,
        floors_count=2,
        description='Historic terminus station connecting North and South India with modern passenger facilities.'
    )

    db.session.add(ndls)
    db.session.add(mas)
    db.session.commit()

    # --- NDLS NODES (Level 0: Ground Concourse & Platforms, Level 1: Foot Overbridges) ---
    nodes_data = [
        # Entrances & Gates (Floor 0)
        {'id': 'ndls_gate1', 'name': 'Gate 1 (Paharganj Main Entry)', 'cat': 'gate', 'fl': 0, 'x': 80, 'y': 300, 'acc': True, 'desc': 'Direct auto/taxi porch drop-off', 'qr': 'QR-NDLS-GATE1'},
        {'id': 'ndls_gate2', 'name': 'Gate 2 (Ajmeri Gate Metro Entry)', 'cat': 'gate', 'fl': 0, 'x': 80, 'y': 120, 'acc': True, 'desc': 'Direct Airport Metro Express walkway', 'qr': 'QR-NDLS-GATE2'},
        {'id': 'ndls_gate3', 'name': 'Gate 3 (VIP & Parking Entry)', 'cat': 'gate', 'fl': 0, 'x': 80, 'y': 480, 'acc': True, 'desc': 'Near premium parking and wheelchair stand', 'qr': 'QR-NDLS-GATE3'},

        # Concourse Hallway Hubs (Floor 0)
        {'id': 'ndls_concourse_main', 'name': 'Central Concourse Plaza', 'cat': 'walkway', 'fl': 0, 'x': 200, 'y': 300, 'acc': True, 'desc': 'Grand hall with digital display boards', 'qr': 'QR-NDLS-CONCOURSE'},
        {'id': 'ndls_concourse_north', 'name': 'North Concourse Hall', 'cat': 'walkway', 'fl': 0, 'x': 200, 'y': 150, 'acc': True, 'desc': 'Near Metro connector and UTS hall', 'qr': 'QR-NDLS-CONCOURSE-N'},
        {'id': 'ndls_concourse_south', 'name': 'South Concourse Hall', 'cat': 'walkway', 'fl': 0, 'x': 200, 'y': 450, 'acc': True, 'desc': 'Near Cloak Room and Waiting Hall', 'qr': 'QR-NDLS-CONCOURSE-S'},

        # Ticketing & Inquiries (Floor 0)
        {'id': 'ndls_uts_counters', 'name': 'UTS General Ticket Booking', 'cat': 'ticket', 'fl': 0, 'x': 140, 'y': 220, 'acc': True, 'desc': 'Counters 1-12 for unreserved journeys', 'qr': 'QR-NDLS-UTS'},
        {'id': 'ndls_prs_counters', 'name': 'PRS Reserved Ticket Office', 'cat': 'ticket', 'fl': 0, 'x': 140, 'y': 380, 'acc': True, 'desc': 'Air-conditioned reservation building', 'qr': 'QR-NDLS-PRS'},
        {'id': 'ndls_atvm_booth', 'name': 'ATVM Automated Smart Card Kiosks', 'cat': 'ticket', 'fl': 0, 'x': 240, 'y': 250, 'acc': True, 'desc': 'Instant touch ticket vending machines', 'qr': 'QR-NDLS-ATVM'},
        {'id': 'ndls_helpdesk', 'name': 'Sahyog Passenger Helpdesk & May I Help You', 'cat': 'helpdesk', 'fl': 0, 'x': 240, 'y': 350, 'acc': True, 'desc': '24/7 Railway staff assistance', 'qr': 'QR-NDLS-HELPDESK'},

        # Amenities (Floor 0)
        {'id': 'ndls_food_plaza', 'name': 'IRCTC Jan Aahar & Food Track', 'cat': 'food', 'fl': 0, 'x': 280, 'y': 180, 'acc': True, 'desc': 'Meals, snacks, South/North Indian food', 'qr': 'QR-NDLS-FOOD'},
        {'id': 'ndls_waiting_hall', 'name': 'General Waiting Lounge', 'cat': 'lounge', 'fl': 0, 'x': 280, 'y': 420, 'acc': True, 'desc': 'Clean seating with charging points', 'qr': 'QR-NDLS-WAITING'},
        {'id': 'ndls_restroom_ground', 'name': 'Main Restrooms & Divyang Washroom', 'cat': 'restroom', 'fl': 0, 'x': 140, 'y': 440, 'acc': True, 'desc': 'Accessible toilet & baby care room', 'qr': 'QR-NDLS-WASHROOM'},
        {'id': 'ndls_water_booth1', 'name': 'RO Drinking Water Booth 1', 'cat': 'water', 'fl': 0, 'x': 260, 'y': 310, 'acc': True, 'desc': 'Free purified chilled water', 'qr': 'QR-NDLS-WATER1'},
        {'id': 'ndls_cloak_room', 'name': 'Cloak Room & Luggage Scanner', 'cat': 'cloak_room', 'fl': 0, 'x': 110, 'y': 520, 'acc': True, 'desc': 'Secure luggage deposit with receipts', 'qr': 'QR-NDLS-CLOAK'},
        {'id': 'ndls_medical_booth', 'name': 'Emergency Medical Room (First Aid)', 'cat': 'medical', 'fl': 0, 'x': 280, 'y': 480, 'acc': True, 'desc': '24/7 on-duty doctor and stretcher', 'qr': 'QR-NDLS-MEDICAL'},
        {'id': 'ndls_rpf_booth', 'name': 'RPF Police Help Post & Security', 'cat': 'police', 'fl': 0, 'x': 110, 'y': 80, 'acc': True, 'desc': 'Security outpost, emergency helpline 139', 'qr': 'QR-NDLS-RPF'},
        {'id': 'ndls_wheelchair_post', 'name': 'Divyangjan Sahayak & Wheelchair Booth', 'cat': 'helpdesk', 'fl': 0, 'x': 160, 'y': 320, 'acc': True, 'desc': 'Free wheelchair & battery cart service', 'qr': 'QR-NDLS-WHEELCHAIR'},
        {'id': 'ndls_atm_zone', 'name': 'Bank ATM Kiosk (SBI, BOB)', 'cat': 'atm', 'fl': 0, 'x': 140, 'y': 160, 'acc': True, 'desc': '24-hour cash withdrawal', 'qr': 'QR-NDLS-ATM'},

        # Concourse to FOB Vertical Transit Nodes (Floor 0 Ground level)
        {'id': 'ndls_lift_c1_f0', 'name': 'Central Concourse Lift L1 (Ground)', 'cat': 'lift', 'fl': 0, 'x': 320, 'y': 300, 'acc': True, 'desc': 'Direct elevator to Central Foot Overbridge', 'qr': 'QR-NDLS-LIFT-C1-0'},
        {'id': 'ndls_escala_c1_f0', 'name': 'Central Escalator E1 (Ground to FOB)', 'cat': 'escalator', 'fl': 0, 'x': 320, 'y': 250, 'acc': False, 'desc': 'Upwards escalator to Overbridge', 'qr': 'QR-NDLS-ESC-C1-0'},
        {'id': 'ndls_stairs_c1_f0', 'name': 'Central Stairs S1 (Ground to FOB)', 'cat': 'stairs', 'fl': 0, 'x': 320, 'y': 350, 'acc': False, 'desc': 'Wide footway stairs', 'qr': 'QR-NDLS-STAIRS-C1-0'},
        {'id': 'ndls_ramp_south_f0', 'name': 'South Overbridge Accessible Ramp R1 (Ground)', 'cat': 'ramp', 'fl': 0, 'x': 320, 'y': 520, 'acc': True, 'desc': 'Step-free gentle slope ramp to South FOB', 'qr': 'QR-NDLS-RAMP-S1-0'},

        # Platform 1 Nodes (Direct Concourse Access at Level 0)
        {'id': 'ndls_p1_north', 'name': 'Platform 1 (North - Coach 1-8)', 'cat': 'platform', 'fl': 0, 'x': 400, 'y': 160, 'acc': True, 'desc': 'Vande Bharat / Rajdhani boarding zone', 'qr': 'QR-NDLS-P1-N'},
        {'id': 'ndls_p1_center', 'name': 'Platform 1 (Center - Coach 9-16)', 'cat': 'platform', 'fl': 0, 'x': 400, 'y': 300, 'acc': True, 'desc': 'Main platform concourse interface', 'qr': 'QR-NDLS-P1-C'},
        {'id': 'ndls_p1_south', 'name': 'Platform 1 (South - Coach 17-24)', 'cat': 'platform', 'fl': 0, 'x': 400, 'y': 440, 'acc': True, 'desc': 'Near South overbridge ramp and cafeteria', 'qr': 'QR-NDLS-P1-S'},

        # Platform 2 & 3 Nodes (Island Platform, Level 0)
        {'id': 'ndls_p2_p3_lift_f0', 'name': 'Platform 2/3 Elevator L2 (Ground)', 'cat': 'lift', 'fl': 0, 'x': 520, 'y': 300, 'acc': True, 'desc': 'Accessible elevator connecting to FOB 1', 'qr': 'QR-NDLS-LIFT-P23-0'},
        {'id': 'ndls_p2_p3_stairs_f0', 'name': 'Platform 2/3 Stairs (Ground)', 'cat': 'stairs', 'fl': 0, 'x': 520, 'y': 250, 'acc': False, 'desc': 'Stairs up to Overbridge', 'qr': 'QR-NDLS-STAIRS-P23-0'},
        {'id': 'ndls_p2_p3_ramp_f0', 'name': 'Platform 2/3 Ramp R2 (Ground)', 'cat': 'ramp', 'fl': 0, 'x': 520, 'y': 500, 'acc': True, 'desc': 'Wheelchair accessible ramp to South FOB', 'qr': 'QR-NDLS-RAMP-P23-0'},
        {'id': 'ndls_p2_center', 'name': 'Platform 2 (Center - Bhopal Shatabdi)', 'cat': 'platform', 'fl': 0, 'x': 520, 'y': 200, 'acc': True, 'desc': 'Track 2 boarding line', 'qr': 'QR-NDLS-P2-C'},
        {'id': 'ndls_p3_center', 'name': 'Platform 3 (Center - Mumbai Rajdhani)', 'cat': 'platform', 'fl': 0, 'x': 520, 'y': 380, 'acc': True, 'desc': 'Track 3 boarding line', 'qr': 'QR-NDLS-P3-C'},

        # Platform 4 & 5 Nodes (Island Platform, Level 0)
        {'id': 'ndls_p4_p5_lift_f0', 'name': 'Platform 4/5 Elevator L3 (Ground)', 'cat': 'lift', 'fl': 0, 'x': 640, 'y': 300, 'acc': True, 'desc': 'Accessible elevator connecting to FOB 1', 'qr': 'QR-NDLS-LIFT-P45-0'},
        {'id': 'ndls_p4_p5_stairs_f0', 'name': 'Platform 4/5 Stairs (Ground)', 'cat': 'stairs', 'fl': 0, 'x': 640, 'y': 250, 'acc': False, 'desc': 'Stairs up to Overbridge', 'qr': 'QR-NDLS-STAIRS-P45-0'},
        {'id': 'ndls_p4_p5_ramp_f0', 'name': 'Platform 4/5 Ramp R3 (Ground)', 'cat': 'ramp', 'fl': 0, 'x': 640, 'y': 500, 'acc': True, 'desc': 'Wheelchair ramp to South FOB', 'qr': 'QR-NDLS-RAMP-P45-0'},
        {'id': 'ndls_p4_center', 'name': 'Platform 4 (Center - Howrah Rajdhani)', 'cat': 'platform', 'fl': 0, 'x': 640, 'y': 200, 'acc': True, 'desc': 'Track 4 boarding line', 'qr': 'QR-NDLS-P4-C'},
        {'id': 'ndls_p5_center', 'name': 'Platform 5 (Center - Tamil Nadu Exp)', 'cat': 'platform', 'fl': 0, 'x': 640, 'y': 380, 'acc': True, 'desc': 'Track 5 boarding line', 'qr': 'QR-NDLS-P5-C'},

        # Platform 6 & 7 Nodes (Island Platform, Level 0)
        {'id': 'ndls_p6_p7_lift_f0', 'name': 'Platform 6/7 Elevator L4 (Ground)', 'cat': 'lift', 'fl': 0, 'x': 760, 'y': 300, 'acc': True, 'desc': 'Accessible elevator connecting to FOB 1', 'qr': 'QR-NDLS-LIFT-P67-0'},
        {'id': 'ndls_p6_p7_stairs_f0', 'name': 'Platform 6/7 Stairs (Ground)', 'cat': 'stairs', 'fl': 0, 'x': 760, 'y': 250, 'acc': False, 'desc': 'Stairs up to Overbridge', 'qr': 'QR-NDLS-STAIRS-P67-0'},
        {'id': 'ndls_p6_center', 'name': 'Platform 6 (Center - Sealdah Duronto)', 'cat': 'platform', 'fl': 0, 'x': 760, 'y': 200, 'acc': True, 'desc': 'Track 6 boarding line', 'qr': 'QR-NDLS-P6-C'},
        {'id': 'ndls_p7_center', 'name': 'Platform 7 (Center - Garib Rath)', 'cat': 'platform', 'fl': 0, 'x': 760, 'y': 380, 'acc': True, 'desc': 'Track 7 boarding line', 'qr': 'QR-NDLS-P7-C'},

        # --- LEVEL 1: FOOT OVERBRIDGES & SKYWALK (Floor 1) ---
        # Central Foot Overbridge (FOB 1) - Equipped with Lifts and Escalators
        {'id': 'ndls_fob1_concourse_lift_f1', 'name': 'Central FOB Lift Landing (Concourse side)', 'cat': 'lift', 'fl': 1, 'x': 320, 'y': 300, 'acc': True, 'desc': 'Overbridge level lift exit', 'qr': 'QR-NDLS-FOB1-L1'},
        {'id': 'ndls_fob1_concourse_esc_f1', 'name': 'Central FOB Escalator Landing', 'cat': 'escalator', 'fl': 1, 'x': 320, 'y': 250, 'acc': False, 'desc': 'Overbridge escalator top', 'qr': 'QR-NDLS-FOB1-ESC'},
        {'id': 'ndls_fob1_concourse_stairs_f1', 'name': 'Central FOB Stairs Landing', 'cat': 'stairs', 'fl': 1, 'x': 320, 'y': 350, 'acc': False, 'desc': 'Overbridge stairs top', 'qr': 'QR-NDLS-FOB1-STAIRS'},
        {'id': 'ndls_fob1_span_p1', 'name': 'Central FOB Span (over Platform 1)', 'cat': 'fob', 'fl': 1, 'x': 400, 'y': 300, 'acc': True, 'desc': 'Skywalk corridor over Platform 1', 'qr': 'QR-NDLS-FOB1-P1'},
        {'id': 'ndls_fob1_span_p23', 'name': 'Central FOB Span (Platform 2/3 Junction)', 'cat': 'fob', 'fl': 1, 'x': 520, 'y': 300, 'acc': True, 'desc': 'Access to Lift 2 & Stairs down to P2/3', 'qr': 'QR-NDLS-FOB1-P23'},
        {'id': 'ndls_fob1_span_p45', 'name': 'Central FOB Span (Platform 4/5 Junction)', 'cat': 'fob', 'fl': 1, 'x': 640, 'y': 300, 'acc': True, 'desc': 'Access to Lift 3 & Stairs down to P4/5', 'qr': 'QR-NDLS-FOB1-P45'},
        {'id': 'ndls_fob1_span_p67', 'name': 'Central FOB Span (Platform 6/7 Junction)', 'cat': 'fob', 'fl': 1, 'x': 760, 'y': 300, 'acc': True, 'desc': 'Access to Lift 4 & Stairs down to P6/7', 'qr': 'QR-NDLS-FOB1-P67'},
        {'id': 'ndls_exec_lounge_f1', 'name': 'IRCTC Executive AC Lounge', 'cat': 'lounge', 'fl': 1, 'x': 450, 'y': 250, 'acc': True, 'desc': 'Premium lounge with buffet and shower facilities', 'qr': 'QR-NDLS-EXEC-LOUNGE'},

        # South Foot Overbridge (FOB 2) - Specially designed with Continuous Step-Free Ramps (100% Wheelchair Friendly!)
        {'id': 'ndls_fob2_ramp_concourse_f1', 'name': 'South FOB Ramp Landing (Concourse)', 'cat': 'ramp', 'fl': 1, 'x': 320, 'y': 520, 'acc': True, 'desc': 'Ramp top connecting to South Overbridge', 'qr': 'QR-NDLS-FOB2-RAMP-C'},
        {'id': 'ndls_fob2_span_p1', 'name': 'South Accessible FOB (Platform 1 Span)', 'cat': 'fob', 'fl': 1, 'x': 400, 'y': 520, 'acc': True, 'desc': 'Wide corridor for wheelchairs and luggage trolleys', 'qr': 'QR-NDLS-FOB2-P1'},
        {'id': 'ndls_fob2_span_p23', 'name': 'South Accessible FOB (Platform 2/3 Ramp Top)', 'cat': 'ramp', 'fl': 1, 'x': 520, 'y': 500, 'acc': True, 'desc': 'Ramp descending to Platform 2/3', 'qr': 'QR-NDLS-FOB2-P23'},
        {'id': 'ndls_fob2_span_p45', 'name': 'South Accessible FOB (Platform 4/5 Ramp Top)', 'cat': 'ramp', 'fl': 1, 'x': 640, 'y': 500, 'acc': True, 'desc': 'Ramp descending to Platform 4/5', 'qr': 'QR-NDLS-FOB2-P45'}
    ]

    for n in nodes_data:
        node = Node(
            id=n['id'],
            station_id='NDLS',
            name=n['name'],
            category=n['cat'],
            floor=n['fl'],
            x=n['x'],
            y=n['y'],
            is_accessible=n['acc'],
            description=n['desc'],
            qr_token=n['qr']
        )
        db.session.add(node)

    db.session.commit()

    # --- NDLS EDGES (Connecting Nodes with accurate distance in meters and accessibility flags) ---
    edges_data = [
        # Concourse Level 0 Entrances to Central Plaza
        ('ndls_gate1', 'ndls_concourse_main', 25.0, 'walkway', True, False, 'low', 'Direct concourse walkway from Gate 1'),
        ('ndls_gate2', 'ndls_concourse_north', 20.0, 'walkway', True, False, 'low', 'Walkway from Gate 2 Metro entrance'),
        ('ndls_gate3', 'ndls_concourse_south', 22.0, 'walkway', True, False, 'low', 'Walkway from Gate 3 VIP porch'),

        # Concourse Interconnections
        ('ndls_concourse_north', 'ndls_concourse_main', 30.0, 'walkway', True, False, 'medium', 'Central concourse corridor'),
        ('ndls_concourse_main', 'ndls_concourse_south', 30.0, 'walkway', True, False, 'medium', 'Central concourse corridor'),

        # Concourse to Ticketing & Amenities
        ('ndls_concourse_north', 'ndls_uts_counters', 15.0, 'walkway', True, False, 'high', 'Corridor to UTS Ticket counters'),
        ('ndls_concourse_north', 'ndls_rpf_booth', 20.0, 'walkway', True, False, 'low', 'Corridor to RPF Police booth'),
        ('ndls_concourse_north', 'ndls_atm_zone', 12.0, 'walkway', True, False, 'low', 'Corridor to ATM kiosks'),
        ('ndls_concourse_north', 'ndls_food_plaza', 20.0, 'walkway', True, False, 'medium', 'Path to IRCTC Food Plaza'),

        ('ndls_concourse_main', 'ndls_atvm_booth', 10.0, 'walkway', True, False, 'low', 'Touchscreen ATVM area'),
        ('ndls_concourse_main', 'ndls_helpdesk', 10.0, 'walkway', True, False, 'low', 'Sahyog Helpdesk kiosk'),
        ('ndls_concourse_main', 'ndls_water_booth1', 12.0, 'walkway', True, False, 'low', 'Drinking water kiosk'),
        ('ndls_concourse_main', 'ndls_wheelchair_post', 15.0, 'walkway', True, False, 'low', 'Divyangjan Assistance booth'),

        ('ndls_concourse_south', 'ndls_prs_counters', 18.0, 'walkway', True, False, 'medium', 'Path to PRS Reservation building'),
        ('ndls_concourse_south', 'ndls_waiting_hall', 20.0, 'walkway', True, False, 'medium', 'General Waiting Lounge entrance'),
        ('ndls_concourse_south', 'ndls_restroom_ground', 15.0, 'walkway', True, False, 'medium', 'Path to clean washrooms'),
        ('ndls_concourse_south', 'ndls_cloak_room', 25.0, 'walkway', True, False, 'low', 'Path to Cloak Room'),
        ('ndls_concourse_south', 'ndls_medical_booth', 22.0, 'walkway', True, False, 'low', 'Emergency First Aid room path'),

        # Concourse to Platform 1 (Direct Level 0 access)
        ('ndls_food_plaza', 'ndls_p1_north', 25.0, 'walkway', True, False, 'medium', 'Walkway to Platform 1 North'),
        ('ndls_concourse_main', 'ndls_p1_center', 35.0, 'walkway', True, False, 'medium', 'Direct concourse entrance to Platform 1'),
        ('ndls_waiting_hall', 'ndls_p1_south', 25.0, 'walkway', True, False, 'low', 'Walkway to Platform 1 South'),
        ('ndls_p1_north', 'ndls_p1_center', 35.0, 'walkway', True, False, 'medium', 'Platform 1 along tracks'),
        ('ndls_p1_center', 'ndls_p1_south', 35.0, 'walkway', True, False, 'medium', 'Platform 1 along tracks'),

        # Ground Concourse to Vertical Transit Nodes (Central FOB)
        ('ndls_concourse_main', 'ndls_lift_c1_f0', 20.0, 'walkway', True, False, 'low', 'Walk to Lift L1'),
        ('ndls_concourse_main', 'ndls_escala_c1_f0', 20.0, 'walkway', True, False, 'medium', 'Walk to Escalator E1'),
        ('ndls_concourse_main', 'ndls_stairs_c1_f0', 20.0, 'walkway', True, False, 'medium', 'Walk to Central Stairs S1'),

        # Vertical Edges (Level 0 to Level 1)
        # Lift 1 (Vertical Elevator)
        ('ndls_lift_c1_f0', 'ndls_fob1_concourse_lift_f1', 8.0, 'elevator', True, False, 'low', 'Take Lift L1 between Concourse and Central FOB'),
        # Escalator 1 (Upward)
        ('ndls_escala_c1_f0', 'ndls_fob1_concourse_esc_f1', 14.0, 'escalator', False, False, 'medium', 'Take Escalator E1 to Central FOB'),
        # Stairs 1
        ('ndls_stairs_c1_f0', 'ndls_fob1_concourse_stairs_f1', 14.0, 'stairs', False, False, 'low', 'Take Stairs S1 to Central FOB'),

        # South Ramp (Level 0 to Level 1 - 100% Wheelchair Step-Free!)
        ('ndls_concourse_south', 'ndls_ramp_south_f0', 25.0, 'walkway', True, False, 'low', 'Walkway to South Accessible Ramp'),
        ('ndls_ramp_south_f0', 'ndls_fob2_ramp_concourse_f1', 30.0, 'ramp', True, False, 'low', 'Accessible ramp to South Overbridge'),

        # FOB 1 Interconnections (Level 1)
        ('ndls_fob1_concourse_lift_f1', 'ndls_fob1_concourse_esc_f1', 10.0, 'walkway', True, False, 'low', 'Central FOB lobby'),
        ('ndls_fob1_concourse_lift_f1', 'ndls_fob1_concourse_stairs_f1', 10.0, 'walkway', True, False, 'low', 'Central FOB lobby'),
        ('ndls_fob1_concourse_lift_f1', 'ndls_fob1_span_p1', 20.0, 'bridge', True, False, 'medium', 'Central FOB span over Platform 1'),
        ('ndls_fob1_span_p1', 'ndls_exec_lounge_f1', 15.0, 'walkway', True, False, 'low', 'Entrance to IRCTC Executive Lounge'),
        ('ndls_fob1_span_p1', 'ndls_fob1_span_p23', 30.0, 'bridge', True, False, 'medium', 'Central FOB span between Platform 1 and Platform 2/3'),
        ('ndls_fob1_span_p23', 'ndls_fob1_span_p45', 30.0, 'bridge', True, False, 'medium', 'Central FOB span between Platform 2/3 and Platform 4/5'),
        ('ndls_fob1_span_p45', 'ndls_fob1_span_p67', 30.0, 'bridge', True, False, 'medium', 'Central FOB span between Platform 4/5 and Platform 6/7'),

        # FOB 1 down to Platforms (Lifts and Stairs)
        # Platform 2 & 3
        ('ndls_fob1_span_p23', 'ndls_p2_p3_lift_f0', 8.0, 'elevator', True, False, 'low', 'Take Lift L2 between FOB 1 and Platform 2/3'),
        ('ndls_fob1_span_p23', 'ndls_p2_p3_stairs_f0', 14.0, 'stairs', False, False, 'medium', 'Take Stairs from FOB 1 down to Platform 2/3'),
        ('ndls_p2_p3_lift_f0', 'ndls_p2_center', 15.0, 'walkway', True, False, 'medium', 'Walkway on Platform 2/3'),
        ('ndls_p2_p3_lift_f0', 'ndls_p3_center', 15.0, 'walkway', True, False, 'medium', 'Walkway on Platform 2/3'),
        ('ndls_p2_p3_stairs_f0', 'ndls_p2_center', 12.0, 'walkway', True, False, 'medium', 'Walkway on Platform 2/3'),
        ('ndls_p2_p3_stairs_f0', 'ndls_p3_center', 12.0, 'walkway', True, False, 'medium', 'Walkway on Platform 2/3'),

        # Platform 4 & 5
        ('ndls_fob1_span_p45', 'ndls_p4_p5_lift_f0', 8.0, 'elevator', True, False, 'low', 'Take Lift L3 between FOB 1 and Platform 4/5'),
        ('ndls_fob1_span_p45', 'ndls_p4_p5_stairs_f0', 14.0, 'stairs', False, False, 'medium', 'Take Stairs from FOB 1 down to Platform 4/5'),
        ('ndls_p4_p5_lift_f0', 'ndls_p4_center', 15.0, 'walkway', True, False, 'medium', 'Walkway on Platform 4/5'),
        ('ndls_p4_p5_lift_f0', 'ndls_p5_center', 15.0, 'walkway', True, False, 'medium', 'Walkway on Platform 4/5'),
        ('ndls_p4_p5_stairs_f0', 'ndls_p4_center', 12.0, 'walkway', True, False, 'medium', 'Walkway on Platform 4/5'),
        ('ndls_p4_p5_stairs_f0', 'ndls_p5_center', 12.0, 'walkway', True, False, 'medium', 'Walkway on Platform 4/5'),

        # Platform 6 & 7
        ('ndls_fob1_span_p67', 'ndls_p6_p7_lift_f0', 8.0, 'elevator', True, False, 'low', 'Take Lift L4 between FOB 1 and Platform 6/7'),
        ('ndls_fob1_span_p67', 'ndls_p6_p7_stairs_f0', 14.0, 'stairs', False, False, 'medium', 'Take Stairs from FOB 1 down to Platform 6/7'),
        ('ndls_p6_p7_lift_f0', 'ndls_p6_center', 15.0, 'walkway', True, False, 'medium', 'Walkway on Platform 6/7'),
        ('ndls_p6_p7_lift_f0', 'ndls_p7_center', 15.0, 'walkway', True, False, 'medium', 'Walkway on Platform 6/7'),
        ('ndls_p6_p7_stairs_f0', 'ndls_p6_center', 12.0, 'walkway', True, False, 'medium', 'Walkway on Platform 6/7'),
        ('ndls_p6_p7_stairs_f0', 'ndls_p7_center', 12.0, 'walkway', True, False, 'medium', 'Walkway on Platform 6/7'),

        # South FOB 2 (Wheelchair Friendly Ramps connecting platforms)
        ('ndls_fob2_ramp_concourse_f1', 'ndls_fob2_span_p1', 20.0, 'bridge', True, False, 'low', 'South FOB span'),
        ('ndls_fob2_span_p1', 'ndls_p1_south', 25.0, 'ramp', True, False, 'low', 'Ramp down to Platform 1 South'),
        ('ndls_fob2_span_p1', 'ndls_fob2_span_p23', 30.0, 'bridge', True, False, 'low', 'South FOB span between P1 and P2/3'),
        ('ndls_fob2_span_p23', 'ndls_p2_p3_ramp_f0', 25.0, 'ramp', True, False, 'low', 'Accessible ramp down to Platform 2/3'),
        ('ndls_p2_p3_ramp_f0', 'ndls_p3_center', 25.0, 'walkway', True, False, 'low', 'Walkway on Platform 2/3'),
        ('ndls_fob2_span_p23', 'ndls_fob2_span_p45', 30.0, 'bridge', True, False, 'low', 'South FOB span between P2/3 and P4/5'),
        ('ndls_fob2_span_p45', 'ndls_p4_p5_ramp_f0', 25.0, 'ramp', True, False, 'low', 'Accessible ramp down to Platform 4/5'),
        ('ndls_p4_p5_ramp_f0', 'ndls_p5_center', 25.0, 'walkway', True, False, 'low', 'Walkway on Platform 4/5')
    ]

    for (na, nb, dist, ptype, w_acc, blk, cong, desc) in edges_data:
        edge = Edge(
            station_id='NDLS',
            node_a=na,
            node_b=nb,
            distance=dist,
            pathway_type=ptype,
            is_wheelchair_accessible=w_acc,
            is_blocked=blk,
            congestion_level=cong,
            bidirectional=True,
            description=desc
        )
        db.session.add(edge)

    db.session.commit()

    # --- FACILITIES (Searchable amenities) ---
    facilities_data = [
        {'nid': 'ndls_p1_center', 'name': 'Platform 1', 'cat': 'platform', 'ico': 'fa-train', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Main Concourse level platform. Vande Bharat Express & Rajdhani.'},
        {'nid': 'ndls_p2_center', 'name': 'Platform 2', 'cat': 'platform', 'ico': 'fa-train', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Island platform with lift and stairs. Bhopal Shatabdi.'},
        {'nid': 'ndls_p3_center', 'name': 'Platform 3', 'cat': 'platform', 'ico': 'fa-train', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Island platform with lift and ramp. Mumbai Rajdhani Express.'},
        {'nid': 'ndls_p4_center', 'name': 'Platform 4', 'cat': 'platform', 'ico': 'fa-train', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Island platform with lift and stairs. Howrah Rajdhani.'},
        {'nid': 'ndls_p5_center', 'name': 'Platform 5', 'cat': 'platform', 'ico': 'fa-train', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Island platform with lift and ramp. Tamil Nadu Express.'},
        {'nid': 'ndls_p6_center', 'name': 'Platform 6', 'cat': 'platform', 'ico': 'fa-train', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Island platform with elevator. Sealdah Duronto.'},
        {'nid': 'ndls_p7_center', 'name': 'Platform 7', 'cat': 'platform', 'ico': 'fa-train', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Island platform with elevator. Garib Rath Express.'},

        {'nid': 'ndls_uts_counters', 'name': 'UTS General Ticket Counter', 'cat': 'ticket', 'ico': 'fa-ticket', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Unreserved general ticketing windows with digital queue tokens.'},
        {'nid': 'ndls_prs_counters', 'name': 'PRS Reservation Complex', 'cat': 'ticket', 'ico': 'fa-id-card', 'fl': 0, 'hrs': '08:00 - 20:00', 'st': 'operational', 'dt': 'Air-conditioned reservation booking and cancellation hall.'},
        {'nid': 'ndls_atvm_booth', 'name': 'Smart Card ATVM Kiosks', 'cat': 'ticket', 'ico': 'fa-credit-card', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': '8 Touchscreen ticketing kiosks accepting UPI and Rail Smart Card.'},

        {'nid': 'ndls_food_plaza', 'name': 'IRCTC Jan Aahar & Food Court', 'cat': 'food', 'ico': 'fa-utensils', 'fl': 0, 'hrs': '06:00 - 23:30', 'st': 'operational', 'dt': 'Clean subsidized meals, thali, snacks, tea/coffee & packed food.'},
        {'nid': 'ndls_waiting_hall', 'name': 'General Passenger Waiting Hall', 'cat': 'waiting_hall', 'ico': 'fa-couch', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Spacious hall with mobile charging sockets and flight-style flight display.'},
        {'nid': 'ndls_exec_lounge_f1', 'name': 'IRCTC Executive AC Lounge', 'cat': 'waiting_hall', 'ico': 'fa-crown', 'fl': 1, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'VIP AC Lounge on Level 1 Overbridge with WiFi, recliners and buffet.'},

        {'nid': 'ndls_restroom_ground', 'name': 'Public Restrooms & Divyang Toilet', 'cat': 'restroom', 'ico': 'fa-restroom', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Pay and use modern toilets, baby care room, wheelchair step-free stall.'},
        {'nid': 'ndls_water_booth1', 'name': 'Chilled RO Water Dispenser', 'cat': 'water', 'ico': 'fa-faucet-drip', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Pure drinking water conforming to WHO standards. Refill ₹5.'},
        {'nid': 'ndls_cloak_room', 'name': 'Cloak Room & Luggage Lockers', 'cat': 'cloak_room', 'ico': 'fa-suitcase-rolling', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Computerized baggage deposit. Padlocked luggage accepted.'},

        {'nid': 'ndls_medical_booth', 'name': 'Emergency Medical Room (First Aid)', 'cat': 'medical', 'ico': 'fa-briefcase-medical', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Immediate medical emergency care with oxygen, stretcher, and doctor.'},
        {'nid': 'ndls_rpf_booth', 'name': 'RPF Help Post & Station Security', 'cat': 'police', 'ico': 'fa-shield-halved', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Railway Protection Force post. Emergency hotline 139.'},
        {'nid': 'ndls_wheelchair_post', 'name': 'Divyangjan Sahayak & Wheelchair Desk', 'cat': 'helpdesk', 'ico': 'fa-wheelchair', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Free wheelchair assistance and battery-operated carts for senior citizens.'},
        {'nid': 'ndls_helpdesk', 'name': 'Sahyog Passenger Information Center', 'cat': 'helpdesk', 'ico': 'fa-circle-info', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Multilingual station guide, audio announcements and inquiry counter.'},
        {'nid': 'ndls_atm_zone', 'name': 'State Bank of India ATM', 'cat': 'atm', 'ico': 'fa-money-bill-wave', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Dual ATMs with cash deposit and cash withdrawal machines.'},

        {'nid': 'ndls_lift_c1_f0', 'name': 'Elevator Lift L1 (Concourse to FOB)', 'cat': 'lift', 'ico': 'fa-elevator', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Spacious 16-passenger lift connecting ground concourse to Overbridge 1.'},
        {'nid': 'ndls_p2_p3_lift_f0', 'name': 'Elevator Lift L2 (Platform 2/3 to FOB)', 'cat': 'lift', 'ico': 'fa-elevator', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Elevator connecting Platform 2/3 to Central Overbridge.'},
        {'nid': 'ndls_p4_p5_lift_f0', 'name': 'Elevator Lift L3 (Platform 4/5 to FOB)', 'cat': 'lift', 'ico': 'fa-elevator', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Elevator connecting Platform 4/5 to Central Overbridge.'},
        {'nid': 'ndls_p6_p7_lift_f0', 'name': 'Elevator Lift L4 (Platform 6/7 to FOB)', 'cat': 'lift', 'ico': 'fa-elevator', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Elevator connecting Platform 6/7 to Central Overbridge.'},

        {'nid': 'ndls_gate1', 'name': 'Gate 1 - Paharganj Entrance', 'cat': 'gate', 'ico': 'fa-door-open', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Main Paharganj entrance with taxi lane and auto stand.'},
        {'nid': 'ndls_gate2', 'name': 'Gate 2 - Ajmeri Gate & Metro', 'cat': 'gate', 'ico': 'fa-door-open', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Direct skywalk to Delhi Airport Metro Express & Yellow Line.'},
        {'nid': 'ndls_gate3', 'name': 'Gate 3 - VIP & Bhavbhuti Marg', 'cat': 'gate', 'ico': 'fa-door-open', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Easy vehicular drop-off and wheelchair ramp access.'}
    ]

    for f in facilities_data:
        fac = Facility(
            station_id='NDLS',
            node_id=f['nid'],
            name=f['name'],
            category=f['cat'],
            icon=f['ico'],
            floor=f['fl'],
            operating_hours=f['hrs'],
            status=f['st'],
            details=f['dt']
        )
        db.session.add(fac)

    db.session.commit()

    # --- LIVE TRAIN SCHEDULE ---
    trains_data = [
        {'no': '20901', 'name': 'Vande Bharat Express', 'type': 'Vande Bharat', 'plat': '1', 'arr': '11:45', 'dep': '12:00', 'st': 'Boarding Now', 'delay': 0},
        {'no': '12952', 'name': 'Mumbai Tejas Rajdhani', 'type': 'Rajdhani', 'plat': '3', 'arr': '12:15', 'dep': '12:35', 'st': 'On Time', 'delay': 0},
        {'no': '12002', 'name': 'Bhopal Shatabdi Express', 'type': 'Shatabdi', 'plat': '2', 'arr': '12:40', 'dep': '13:00', 'st': 'On Time', 'delay': 0},
        {'no': '12622', 'name': 'Tamil Nadu Superfast Express', 'type': 'Superfast', 'plat': '5', 'arr': '13:05', 'dep': '13:30', 'st': 'Delayed 15m', 'delay': 15},
        {'no': '12302', 'name': 'Howrah Rajdhani Express', 'type': 'Rajdhani', 'plat': '4', 'arr': '13:50', 'dep': '14:10', 'st': 'On Time', 'delay': 0},
        {'no': '12424', 'name': 'Dibrugarh Rajdhani Express', 'type': 'Rajdhani', 'plat': '6', 'arr': '14:20', 'dep': '14:45', 'st': 'On Time', 'delay': 0},
        {'no': '12260', 'name': 'Sealdah AC Duronto', 'type': 'Duronto', 'plat': '7', 'arr': '14:50', 'dep': '15:15', 'st': 'On Time', 'delay': 0}
    ]

    for t in trains_data:
        ts = TrainSchedule(
            station_id='NDLS',
            train_number=t['no'],
            train_name=t['name'],
            train_type=t['type'],
            platform=t['plat'],
            arrival_time=t['arr'],
            departure_time=t['dep'],
            status=t['st'],
            delay_minutes=t['delay']
        )
        db.session.add(ts)

    # Initial sample Assistance Request
    sample_req = AssistanceRequest(
        station_id='NDLS',
        request_type='wheelchair',
        passenger_name='Sunil Kumar (Senior Citizen)',
        contact_phone='+91 98765 43210',
        pickup_node_id='ndls_gate1',
        destination_node_id='ndls_p1_center',
        status='assigned',
        notes='Passenger needs wheelchair assistance with 1 heavy suitcase from Gate 1 to Coach C-4.'
    )
    # --- CHENNAI CENTRAL (MAS) NODES, EDGES, FACILITIES & TRAINS ---
    mas_nodes = [
        {'id': 'mas_gate1', 'name': 'Gate 1 (Main Heritage Concourse Entry)', 'cat': 'gate', 'fl': 0, 'x': 80, 'y': 300, 'acc': True, 'desc': 'EVR Periyar Salai porch drop-off', 'qr': 'QR-MAS-GATE1'},
        {'id': 'mas_gate2', 'name': 'Gate 2 (Moore Market Suburban & Metro)', 'cat': 'gate', 'fl': 0, 'x': 80, 'y': 150, 'acc': True, 'desc': 'Direct Chennai Central Metro & MMC walkway', 'qr': 'QR-MAS-GATE2'},
        {'id': 'mas_concourse', 'name': 'Grand Concourse Plaza', 'cat': 'walkway', 'fl': 0, 'x': 200, 'y': 300, 'acc': True, 'desc': 'Heritage central hall with flight-style train boards', 'qr': 'QR-MAS-CONCOURSE'},
        {'id': 'mas_uts', 'name': 'UTS General Ticket Booking Hall', 'cat': 'ticket', 'fl': 0, 'x': 140, 'y': 220, 'acc': True, 'desc': 'General unreserved ticket windows', 'qr': 'QR-MAS-UTS'},
        {'id': 'mas_prs', 'name': 'PRS Reserved Ticket Complex', 'cat': 'ticket', 'fl': 0, 'x': 140, 'y': 420, 'acc': True, 'desc': 'Passenger reservation counters', 'qr': 'QR-MAS-PRS'},
        {'id': 'mas_food', 'name': 'Saravana Bhavan & Jan Aahar Food Court', 'cat': 'food', 'fl': 0, 'x': 280, 'y': 200, 'acc': True, 'desc': 'South Indian tiffin, meals, snacks and coffee', 'qr': 'QR-MAS-FOOD'},
        {'id': 'mas_restroom', 'name': 'Main Washrooms & Divyangjan Restroom', 'cat': 'restroom', 'fl': 0, 'x': 140, 'y': 490, 'acc': True, 'desc': 'Clean accessible restrooms', 'qr': 'QR-MAS-RESTROOM'},
        {'id': 'mas_lift_c1_f0', 'name': 'Central Lift L1 (Concourse to FOB)', 'cat': 'lift', 'fl': 0, 'x': 320, 'y': 300, 'acc': True, 'desc': 'Accessible elevator to Overbridge', 'qr': 'QR-MAS-LIFT1-0'},
        {'id': 'mas_p1_center', 'name': 'Platform 1 (Mysuru Vande Bharat)', 'cat': 'platform', 'fl': 0, 'x': 400, 'y': 220, 'acc': True, 'desc': 'Direct level access from concourse', 'qr': 'QR-MAS-P1-C'},
        {'id': 'mas_p2_center', 'name': 'Platform 2 (Mangalore Mail)', 'cat': 'platform', 'fl': 0, 'x': 520, 'y': 200, 'acc': True, 'desc': 'Track 2 boarding platform', 'qr': 'QR-MAS-P2-C'},
        {'id': 'mas_p3_center', 'name': 'Platform 3 (Cheran Superfast)', 'cat': 'platform', 'fl': 0, 'x': 520, 'y': 380, 'acc': True, 'desc': 'Track 3 boarding platform', 'qr': 'QR-MAS-P3-C'},
        {'id': 'mas_p4_center', 'name': 'Platform 4 (Tamil Nadu Exp to NDLS)', 'cat': 'platform', 'fl': 0, 'x': 640, 'y': 200, 'acc': True, 'desc': 'Track 4 boarding platform', 'qr': 'QR-MAS-P4-C'},
        {'id': 'mas_fob_lift_f1', 'name': 'Central FOB Lift Top (Level 1)', 'cat': 'lift', 'fl': 1, 'x': 320, 'y': 300, 'acc': True, 'desc': 'Overbridge level elevator landing', 'qr': 'QR-MAS-FOB-L1'},
        {'id': 'mas_fob_span_p1', 'name': 'Central FOB Span (Platform 1)', 'cat': 'fob', 'fl': 1, 'x': 400, 'y': 300, 'acc': True, 'desc': 'Overbridge corridor', 'qr': 'QR-MAS-FOB-P1'},
        {'id': 'mas_fob_span_p23', 'name': 'Central FOB Span (Platform 2/3)', 'cat': 'fob', 'fl': 1, 'x': 520, 'y': 300, 'acc': True, 'desc': 'Overbridge stairs and lift to P2/3', 'qr': 'QR-MAS-FOB-P23'}
    ]

    for n in mas_nodes:
        node = Node(
            id=n['id'],
            station_id='MAS',
            name=n['name'],
            category=n['cat'],
            floor=n['fl'],
            x=n['x'],
            y=n['y'],
            is_accessible=n['acc'],
            description=n['desc'],
            qr_token=n['qr']
        )
        db.session.add(node)

    mas_edges = [
        ('mas_gate1', 'mas_concourse', 25.0, 'walkway', True, False, 'low', 'Main entrance walkway'),
        ('mas_gate2', 'mas_concourse', 30.0, 'walkway', True, False, 'low', 'Moore Market walkway'),
        ('mas_concourse', 'mas_uts', 18.0, 'walkway', True, False, 'medium', 'Walkway to UTS booking'),
        ('mas_concourse', 'mas_prs', 22.0, 'walkway', True, False, 'low', 'Walkway to PRS reservation'),
        ('mas_concourse', 'mas_food', 20.0, 'walkway', True, False, 'medium', 'Path to Saravana Bhavan'),
        ('mas_concourse', 'mas_restroom', 25.0, 'walkway', True, False, 'low', 'Path to restrooms'),
        ('mas_concourse', 'mas_p1_center', 30.0, 'walkway', True, False, 'medium', 'Direct concourse walkway to Platform 1'),
        ('mas_concourse', 'mas_lift_c1_f0', 20.0, 'walkway', True, False, 'low', 'Walk to Lift L1'),
        ('mas_lift_c1_f0', 'mas_fob_lift_f1', 8.0, 'elevator', True, False, 'low', 'Take Lift L1 to Overbridge Level 1'),
        ('mas_fob_lift_f1', 'mas_fob_span_p1', 20.0, 'bridge', True, False, 'low', 'Overbridge span over Platform 1'),
        ('mas_fob_span_p1', 'mas_fob_span_p23', 30.0, 'bridge', True, False, 'low', 'Overbridge span to Platform 2/3'),
        ('mas_fob_span_p23', 'mas_p2_center', 15.0, 'stairs', False, False, 'medium', 'Stairs down to Platform 2'),
        ('mas_fob_span_p23', 'mas_p3_center', 15.0, 'stairs', False, False, 'medium', 'Stairs down to Platform 3'),
        ('mas_p1_center', 'mas_p2_center', 40.0, 'walkway', True, False, 'low', 'Platform concourse crossing')
    ]

    for (na, nb, dist, ptype, w_acc, blk, cong, desc) in mas_edges:
        edge = Edge(
            station_id='MAS',
            node_a=na,
            node_b=nb,
            distance=dist,
            pathway_type=ptype,
            is_wheelchair_accessible=w_acc,
            is_blocked=blk,
            congestion_level=cong,
            bidirectional=True,
            description=desc
        )
        db.session.add(edge)

    mas_facilities = [
        {'nid': 'mas_p1_center', 'name': 'Platform 1', 'cat': 'platform', 'ico': 'fa-train', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Mysuru Vande Bharat Express departure platform.'},
        {'nid': 'mas_p2_center', 'name': 'Platform 2', 'cat': 'platform', 'ico': 'fa-train', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Mangalore Mail departure platform.'},
        {'nid': 'mas_p3_center', 'name': 'Platform 3', 'cat': 'platform', 'ico': 'fa-train', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Cheran Superfast Express.'},
        {'nid': 'mas_uts', 'name': 'UTS General Booking Counters', 'cat': 'ticket', 'ico': 'fa-ticket', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'General unreserved ticket booking.'},
        {'nid': 'mas_food', 'name': 'Saravana Bhavan Restaurant', 'cat': 'food', 'ico': 'fa-utensils', 'fl': 0, 'hrs': '06:00 - 23:00', 'st': 'operational', 'dt': 'Authentic South Indian vegetarian food & filter coffee.'},
        {'nid': 'mas_restroom', 'name': 'Restrooms & Divyang Toilet', 'cat': 'restroom', 'ico': 'fa-restroom', 'fl': 0, 'hrs': '24 Hours', 'st': 'operational', 'dt': 'Clean pay-and-use washrooms.'}
    ]

    for f in mas_facilities:
        fac = Facility(
            station_id='MAS',
            node_id=f['nid'],
            name=f['name'],
            category=f['cat'],
            icon=f['ico'],
            floor=f['fl'],
            operating_hours=f['hrs'],
            status=f['st'],
            details=f['dt']
        )
        db.session.add(fac)

    mas_trains = [
        {'no': '20608', 'name': 'Mysuru - Chennai Vande Bharat', 'type': 'Vande Bharat', 'plat': '1', 'arr': '12:25', 'dep': '13:00', 'st': 'On Time', 'delay': 0},
        {'no': '12602', 'name': 'Mangalore Central Superfast Mail', 'type': 'Superfast', 'plat': '2', 'arr': '13:30', 'dep': '13:55', 'st': 'On Time', 'delay': 0},
        {'no': '12674', 'name': 'Cheran Superfast Express', 'type': 'Superfast', 'plat': '3', 'arr': '14:10', 'dep': '14:35', 'st': 'On Time', 'delay': 0},
        {'no': '12621', 'name': 'Tamil Nadu Express to NDLS', 'type': 'Superfast', 'plat': '4', 'arr': '21:30', 'dep': '22:00', 'st': 'On Time', 'delay': 0}
    ]

    for t in mas_trains:
        ts = TrainSchedule(
            station_id='MAS',
            train_number=t['no'],
            train_name=t['name'],
            train_type=t['type'],
            platform=t['plat'],
            arrival_time=t['arr'],
            departure_time=t['dep'],
            status=t['st'],
            delay_minutes=t['delay']
        )
        db.session.add(ts)

    db.session.commit()
    print("Database seeding completed successfully!")
