"""
Pathfinding Engine for RailNav AI
Implements Dijkstra's Algorithm and A* Search with Accessibility and Obstacle Avoidance
"""
import math
import heapq

def euclidean_distance(node_a, node_b):
    """Euclidean distance heuristic for A* in 2D coordinate space"""
    dx = node_a['x'] - node_b['x']
    dy = node_a['y'] - node_b['y']
    # If on different floors, add a 15-meter vertical distance equivalent
    floor_penalty = 15.0 if node_a.get('floor', 0) != node_b.get('floor', 0) else 0.0
    return math.sqrt(dx * dx + dy * dy) + floor_penalty


class StationGraph:
    def __init__(self, nodes_dict, edges_list):
        """
        nodes_dict: dict of node_id -> node_dict
        edges_list: list of edge_dict
        """
        self.nodes = nodes_dict
        self.adj = {node_id: [] for node_id in nodes_dict}
        self.edges_map = {}

        for edge in edges_list:
            u = edge['node_a']
            v = edge['node_b']
            if u in self.nodes and v in self.nodes:
                self.adj[u].append((v, edge))
                self.edges_map[(u, v)] = edge
                if edge.get('bidirectional', True):
                    self.adj[v].append((u, edge))
                    self.edges_map[(v, u)] = edge

    def find_shortest_path(self, start_id, end_id, wheelchair_only=False, algorithm='a_star'):
        """
        Finds the shortest optimal path between start_id and end_id
        using A* or Dijkstra's algorithm.
        Returns:
            dict with {
                'success': bool,
                'path_nodes': list of node dicts,
                'total_distance': float (meters),
                'estimated_seconds': int,
                'instructions': list of step instructions,
                'wheelchair_friendly': bool
            }
        """
        if start_id not in self.nodes or end_id not in self.nodes:
            return {
                'success': False,
                'error': f"Start '{start_id}' or End '{end_id}' not found in station graph.",
                'path_nodes': [],
                'total_distance': 0,
                'instructions': []
            }

        if start_id == end_id:
            dest_node = self.nodes[end_id]
            return {
                'success': True,
                'path_nodes': [dest_node],
                'total_distance': 0.0,
                'estimated_seconds': 0,
                'instructions': [{
                    'step': 1,
                    'action': 'arrive',
                    'icon': 'fa-flag-checkered',
                    'text': f"You are already at {dest_node['name']}.",
                    'distance': 0,
                    'floor': dest_node.get('floor', 0),
                    'node_id': end_id
                }],
                'wheelchair_friendly': True
            }

        target_node = self.nodes[end_id]

        # Priority queue entries: (f_score, current_distance, current_node_id, path_nodes, path_edges)
        pq = []
        start_h = euclidean_distance(self.nodes[start_id], target_node) if algorithm == 'a_star' else 0.0
        heapq.heappush(pq, (start_h, 0.0, start_id, [start_id], []))

        # Best distance recorded to reach node
        best_dist = {start_id: 0.0}

        found_path_nodes = None
        found_path_edges = None
        final_distance = 0.0

        while pq:
            f_score, dist, current, path, edges = heapq.heappop(pq)

            if current == end_id:
                found_path_nodes = path
                found_path_edges = edges
                final_distance = dist
                break

            if dist > best_dist.get(current, float('inf')):
                continue

            for neighbor, edge in self.adj.get(current, []):
                # Filter 1: Obstacle Avoidance (Blocked edges)
                if edge.get('is_blocked', False):
                    continue

                # Filter 2: Accessibility / Wheelchair filter
                if wheelchair_only and not edge.get('is_wheelchair_accessible', True):
                    continue

                # Filter 3: Accessible node validation
                if wheelchair_only and not self.nodes[neighbor].get('is_accessible', True):
                    continue

                # Cost weight: distance + slight penalty for high congestion
                edge_cost = edge.get('distance', 1.0)
                congestion = edge.get('congestion_level', 'low')
                if congestion == 'high':
                    edge_cost *= 1.35
                elif congestion == 'medium':
                    edge_cost *= 1.15

                new_dist = dist + edge_cost

                if new_dist < best_dist.get(neighbor, float('inf')):
                    best_dist[neighbor] = new_dist
                    h = euclidean_distance(self.nodes[neighbor], target_node) if algorithm == 'a_star' else 0.0
                    heapq.heappush(pq, (new_dist + h, new_dist, neighbor, path + [neighbor], edges + [edge]))

        if not found_path_nodes:
            # If wheelchair mode failed, notify user
            if wheelchair_only:
                return {
                    'success': False,
                    'error': 'No step-free / wheelchair accessible route found. Check if elevators or ramps are temporarily under maintenance.',
                    'path_nodes': [],
                    'total_distance': 0,
                    'instructions': []
                }
            return {
                'success': False,
                'error': f"No connected pathway between {self.nodes[start_id]['name']} and {self.nodes[end_id]['name']}.",
                'path_nodes': [],
                'total_distance': 0,
                'instructions': []
            }

        # Build full path node objects
        path_node_objs = [self.nodes[nid] for nid in found_path_nodes]

        # Generate human-readable turn-by-turn guidance
        instructions = self._generate_turn_by_turn(path_node_objs, found_path_edges, wheelchair_only)

        # Walking speed: 1.2 m/s standard, 0.85 m/s for wheelchair/luggage
        speed = 0.85 if wheelchair_only else 1.2
        estimated_seconds = int(final_distance / speed)
        # Add transit delays for lifts/escalators
        for edge in found_path_edges:
            ptype = edge.get('pathway_type', '')
            if ptype == 'elevator':
                estimated_seconds += 40
            elif ptype in ('escalator', 'stairs', 'ramp'):
                estimated_seconds += 15

        return {
            'success': True,
            'path_nodes': path_node_objs,
            'total_distance': round(final_distance, 1),
            'estimated_seconds': estimated_seconds,
            'estimated_minutes': max(1, math.ceil(estimated_seconds / 60)),
            'instructions': instructions,
            'wheelchair_friendly': wheelchair_only or all(e.get('is_wheelchair_accessible', True) for e in found_path_edges)
        }

    def _generate_turn_by_turn(self, path_nodes, path_edges, wheelchair_only):
        """
        Creates intuitive, human-friendly directions with direction bearings,
        landmark cues, and floor-level change alerts.
        """
        if len(path_nodes) == 1:
            return [{
                'step': 1,
                'action': 'arrive',
                'icon': 'fa-flag-checkered',
                'text': f"You have arrived at {path_nodes[0]['name']}.",
                'distance': 0,
                'floor': path_nodes[0].get('floor', 0),
                'node_id': path_nodes[0]['id']
            }]

        instructions = []
        step_num = 1

        for i in range(len(path_nodes) - 1):
            curr_n = path_nodes[i]
            next_n = path_nodes[i + 1]
            edge = path_edges[i] if i < len(path_edges) else {}
            edge_dist = round(edge.get('distance', 10.0), 1)
            pathway_type = edge.get('pathway_type', 'walkway')

            curr_floor = curr_n.get('floor', 0)
            next_floor = next_n.get('floor', 0)

            # Check vertical transition
            if curr_floor != next_floor:
                floor_name = "Foot Overbridge (Level 1)" if next_floor == 1 else "Ground Concourse (Level 0)"
                if pathway_type == 'elevator':
                    action = 'elevator'
                    icon = 'fa-elevator'
                    text = f"Take Lift / Elevator to {floor_name}."
                elif pathway_type == 'ramp':
                    action = 'ramp'
                    icon = 'fa-wheelchair'
                    text = f"Take the accessible ramp to {floor_name}."
                elif pathway_type == 'escalator':
                    action = 'escalator'
                    icon = 'fa-arrow-up-right-dots'
                    direction = 'up' if next_floor > curr_floor else 'down'
                    text = f"Take the escalator {direction} to {floor_name}."
                else:
                    action = 'stairs'
                    icon = 'fa-stairs'
                    direction = 'up' if next_floor > curr_floor else 'down'
                    text = f"Take the stairs {direction} to {floor_name}."

                instructions.append({
                    'step': step_num,
                    'action': action,
                    'icon': icon,
                    'text': text,
                    'distance': edge_dist,
                    'floor': next_floor,
                    'node_id': next_n['id']
                })
                step_num += 1
                continue

            # Determine turn angle relative to previous trajectory
            action = 'straight'
            icon = 'fa-arrow-up'
            direction_word = 'straight'

            if i > 0:
                prev_n = path_nodes[i - 1]
                v1_x = curr_n['x'] - prev_n['x']
                v1_y = curr_n['y'] - prev_n['y']
                v2_x = next_n['x'] - curr_n['x']
                v2_y = next_n['y'] - curr_n['y']

                # Angle between vectors
                cross = v1_x * v2_y - v1_y * v2_x
                dot = v1_x * v2_x + v1_y * v2_y
                angle = math.atan2(cross, dot) * (180.0 / math.pi)

                if angle > 35:
                    action = 'turn_right'
                    icon = 'fa-arrow-turn-down-right' if angle > 80 else 'fa-arrow-trend-up'
                    direction_word = 'right'
                elif angle < -35:
                    action = 'turn_left'
                    icon = 'fa-arrow-turn-down-left' if angle < -80 else 'fa-arrow-trend-down'
                    direction_word = 'left'

            # Craft friendly instruction text
            if i == 0:
                text = f"Start from {curr_n['name']} and walk {round(edge_dist)}m towards {next_n['name']}."
            else:
                if direction_word != 'straight':
                    text = f"Turn {direction_word} towards {next_n['name']} and proceed {round(edge_dist)}m."
                else:
                    text = f"Continue straight past {curr_n['name']} for {round(edge_dist)}m towards {next_n['name']}."

            if next_n.get('description'):
                text += f" ({next_n['description']})"

            instructions.append({
                'step': step_num,
                'action': action,
                'icon': icon,
                'text': text,
                'distance': edge_dist,
                'floor': curr_floor,
                'node_id': next_n['id']
            })
            step_num += 1

        # Destination arrival step
        dest_node = path_nodes[-1]
        instructions.append({
            'step': step_num,
            'action': 'arrive',
            'icon': 'fa-circle-check',
            'text': f"Arrive at destination: {dest_node['name']}.",
            'distance': 0,
            'floor': dest_node.get('floor', 0),
            'node_id': dest_node['id']
        })

        return instructions
