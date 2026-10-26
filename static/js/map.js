/**
 * Station Indoor Map Controller using Leaflet.js
 * Multi-level vector station floorplan with animated pathfinding and radar pulse
 */

const StationMap = {
  map: null,
  currentFloor: 0,
  nodes: [],
  edges: [],
  nodeMarkers: {},
  routeLayer: null,
  routePulseMarker: null,
  userMarker: null,
  floorLayers: { 0: null, 1: null },
  activePathNodes: [],
  userCurrentNodeId: 'ndls_gate1',

  init(containerId = 'station-map') {
    // Leaflet CRS.Simple for indoor planar coordinates [0 to 600] Y, [0 to 900] X
    const bounds = [[0, 0], [600, 900]];

    this.map = L.map(containerId, {
      crs: L.CRS.Simple,
      minZoom: -1,
      maxZoom: 2,
      zoomSnap: 0.25,
      zoomDelta: 0.5,
      attributionControl: false
    });

    this.map.fitBounds(bounds);

    // Floor feature groups
    this.floorLayers[0] = L.layerGroup().addTo(this.map);
    this.floorLayers[1] = L.layerGroup();

    // Render station vector architectural layout
    this.renderFloorplanSVG(0);
    this.renderFloorplanSVG(1);

    // Add user initial location marker
    this.updateUserMarker('ndls_gate1');
  },

  renderFloorplanSVG(floor) {
    const layer = this.floorLayers[floor];
    layer.clearLayers();

    if (floor === 0) {
      // --- LEVEL 0: GROUND CONCOURSE & PLATFORMS ---
      // Concourse Hall Outline
      const concourse = L.polygon([
        [50, 40], [550, 40], [550, 350], [50, 350]
      ], {
        color: '#1e3a8a',
        weight: 2,
        fillColor: '#0f172a',
        fillOpacity: 0.8
      }).bindTooltip("Main Station Concourse & Passenger Terminal", { sticky: true });
      layer.addLayer(concourse);

      // Entrance Porches
      const gates = [
        { bounds: [[100, 20], [140, 50]], label: "Gate 2 (Metro)" },
        { bounds: [[280, 20], [320, 50]], label: "Gate 1 (Paharganj Main)" },
        { bounds: [[460, 20], [500, 50]], label: "Gate 3 (VIP & Parking)" }
      ];
      gates.forEach(g => {
        const poly = L.rectangle(g.bounds, {
          color: '#d946ef',
          weight: 2,
          fillColor: '#4a044e',
          fillOpacity: 0.9
        }).bindTooltip(g.label, { permanent: true, direction: "left", className: "floor-label" });
        layer.addLayer(poly);
      });

      // Platform Surfaces & Railway Tracks
      const platforms = [
        { name: "Platform 1", rect: [[140, 380], [460, 420]], track: [[130, 435], [470, 435]] },
        { name: "Platform 2 & 3", rect: [[140, 500], [460, 540]], track1: [[130, 485], [470, 485]], track2: [[130, 555], [470, 555]] },
        { name: "Platform 4 & 5", rect: [[140, 620], [460, 660]], track1: [[130, 605], [470, 605]], track2: [[130, 675], [470, 675]] },
        { name: "Platform 6 & 7", rect: [[140, 740], [460, 780]], track1: [[130, 725], [470, 725]], track2: [[130, 795], [470, 795]] }
      ];

      platforms.forEach(p => {
        // Platform Deck
        const platRect = L.rectangle(p.rect, {
          color: '#3b82f6',
          weight: 1.5,
          fillColor: '#1e293b',
          fillOpacity: 0.95
        }).bindTooltip(p.name, { permanent: true, direction: "center", className: "platform-badge-tooltip" });
        layer.addLayer(platRect);

        // Railway Tracks with sleeper hash markings
        if (p.track) {
          this.renderTrackLine(layer, p.track);
        }
        if (p.track1) {
          this.renderTrackLine(layer, p.track1);
        }
        if (p.track2) {
          this.renderTrackLine(layer, p.track2);
        }
      });

    } else if (floor === 1) {
      // --- LEVEL 1: FOOT OVERBRIDGES (FOB) & SKYWALK ---
      // Central Foot Overbridge (Spanning across concourse to Platform 7)
      const centralFOB = L.polygon([
        [280, 300], [320, 300], [320, 800], [280, 800]
      ], {
        color: '#00d2ff',
        weight: 2,
        fillColor: '#0369a1',
        fillOpacity: 0.85,
        dashArray: '4, 4'
      }).bindTooltip("Central Foot Overbridge 1 (Lifts & Escalators)", { permanent: true, direction: "top" });
      layer.addLayer(centralFOB);

      // South Accessible Ramp Overbridge (Continuous Wheelchair Step-Free)
      const southFOB = L.polygon([
        [490, 300], [530, 300], [530, 700], [490, 700]
      ], {
        color: '#10b981',
        weight: 2,
        fillColor: '#064e3b',
        fillOpacity: 0.85
      }).bindTooltip("South Foot Overbridge 2 (100% Step-Free Ramps ♿)", { permanent: true, direction: "bottom" });
      layer.addLayer(southFOB);

      // Executive Lounge on Level 1
      const loungeRect = L.rectangle([[230, 420], [270, 480]], {
        color: '#fbbf24',
        weight: 1.5,
        fillColor: '#78350f',
        fillOpacity: 0.9
      }).bindTooltip("IRCTC Executive AC Lounge (Level 1)", { permanent: true, direction: "center" });
      layer.addLayer(loungeRect);
    }
  },

  renderTrackLine(layer, coords) {
    // Railway track rails
    const line = L.polyline(coords, {
      color: '#64748b',
      weight: 3,
      dashArray: '8, 8'
    });
    layer.addLayer(line);
  },

  loadNodes(nodesList) {
    this.nodes = nodesList;

    // Remove previous node markers
    Object.values(this.nodeMarkers).forEach(m => m.remove());
    this.nodeMarkers = {};

    nodesList.forEach(node => {
      const floor = node.floor || 0;
      const targetLayer = this.floorLayers[floor];
      if (!targetLayer) return;

      // Invert Y coordinate for Leaflet Simple CRS (600 - y)
      const latLng = [600 - node.y, node.x];

      // Custom HTML DivIcon based on category
      const iconClass = this.getCategoryIcon(node.category);
      const iconHtml = `
        <div class="station-node-icon node-icon-${node.category}" title="${node.name}">
          <i class="fa-solid ${iconClass}"></i>
        </div>
      `;

      const customIcon = L.divIcon({
        className: 'custom-leaflet-node',
        html: iconHtml,
        iconSize: [32, 32],
        iconAnchor: [16, 16]
      });

      const marker = L.marker(latLng, { icon: customIcon });

      // Interactive popup
      const popupContent = `
        <div style="font-family: 'Inter', sans-serif; min-width: 200px; color: #0c1322;">
          <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 4px; color: #1e3a8a;">
            ${node.name}
          </h4>
          <p style="font-size: 0.78rem; color: #475569; margin-bottom: 8px;">
            ${node.description || 'Station waypoint'}
          </p>
          <div style="display: flex; gap: 6px;">
            <button onclick="window.startNavigationTo('${node.id}')" 
              style="flex: 1; background: #ff8a00; color: white; border: none; padding: 6px 10px; border-radius: 6px; font-size: 0.78rem; font-weight: 700; cursor: pointer;">
              <i class="fa-solid fa-diamond-turn-right"></i> Navigate Here
            </button>
            <button onclick="window.setUserLocation('${node.id}')" 
              style="background: #e2e8f0; color: #1e293b; border: none; padding: 6px 8px; border-radius: 6px; font-size: 0.78rem; font-weight: 600; cursor: pointer;" title="Set as starting location">
              <i class="fa-solid fa-location-crosshairs"></i>
            </button>
          </div>
        </div>
      `;

      marker.bindPopup(popupContent);
      marker.addTo(targetLayer);
      this.nodeMarkers[node.id] = marker;
    });
  },

  getCategoryIcon(cat) {
    const map = {
      platform: 'fa-train',
      ticket: 'fa-ticket',
      food: 'fa-utensils',
      restroom: 'fa-restroom',
      lounge: 'fa-couch',
      lift: 'fa-elevator',
      escalator: 'fa-arrow-up-right-dots',
      ramp: 'fa-wheelchair',
      stairs: 'fa-stairs',
      medical: 'fa-briefcase-medical',
      police: 'fa-shield-halved',
      water: 'fa-faucet-drip',
      atm: 'fa-money-bill-wave',
      gate: 'fa-door-open',
      helpdesk: 'fa-circle-info'
    };
    return map[cat] || 'fa-map-pin';
  },

  switchFloor(floor) {
    if (this.currentFloor === floor) return;

    if (this.map.hasLayer(this.floorLayers[this.currentFloor])) {
      this.map.removeLayer(this.floorLayers[this.currentFloor]);
    }
    this.floorLayers[floor].addTo(this.map);
    this.currentFloor = floor;

    // Update active UI floor buttons
    document.querySelectorAll('.floor-btn').forEach(btn => btn.classList.remove('active'));
    const targetBtn = document.getElementById(`btn-floor-${floor}`);
    if (targetBtn) targetBtn.classList.add('active');

    AudioSynthesizer.playChime(587.33, 0.1);

    // If there is an active route, redraw path for visible floor
    if (this.activePathNodes && this.activePathNodes.length > 0) {
      this.renderRoutePolyline(this.activePathNodes);
    }
  },

  updateUserMarker(nodeId) {
    this.userCurrentNodeId = nodeId;
    const node = this.nodes.find(n => n.id === nodeId);
    if (!node) return;

    const latLng = [600 - node.y, node.x];

    if (this.userMarker) {
      this.userMarker.setLatLng(latLng);
    } else {
      const pulseHtml = `<div class="user-pulse-marker" title="Your current location"></div>`;
      const pulseIcon = L.divIcon({
        className: 'user-pulse-wrap',
        html: pulseHtml,
        iconSize: [22, 22],
        iconAnchor: [11, 11]
      });

      this.userMarker = L.marker(latLng, { icon: pulseIcon, zIndexOffset: 2000 }).addTo(this.map);
    }
  },

  renderRoutePolyline(pathNodes) {
    this.activePathNodes = pathNodes;

    // Clear existing route polyline
    if (this.routeLayer) {
      this.routeLayer.remove();
      this.routeLayer = null;
    }
    if (this.routePulseMarker) {
      this.routePulseMarker.remove();
      this.routePulseMarker = null;
    }

    if (!pathNodes || pathNodes.length < 2) return;

    // Group segments by floor
    const currentFloorPoints = [];
    const allFloorPoints = [];

    pathNodes.forEach(n => {
      const pt = [600 - n.y, n.x];
      allFloorPoints.push(pt);
      if (n.floor === this.currentFloor) {
        currentFloorPoints.push(pt);
      }
    });

    // If no points on current floor, alert passenger to switch floor
    const hasDifferentFloor = pathNodes.some(n => n.floor !== this.currentFloor);
    if (currentFloorPoints.length === 0 && hasDifferentFloor) {
      const destinationFloor = pathNodes[pathNodes.length - 1].floor;
      this.switchFloor(destinationFloor);
      return;
    }

    // Outer glow line
    const glowLine = L.polyline(currentFloorPoints.length > 1 ? currentFloorPoints : allFloorPoints, {
      color: '#00d2ff',
      weight: 8,
      opacity: 0.35,
      lineCap: 'round',
      lineJoin: 'round'
    });

    // Inner bright animated dashed line
    const coreLine = L.polyline(currentFloorPoints.length > 1 ? currentFloorPoints : allFloorPoints, {
      color: '#ff8a00',
      weight: 4,
      opacity: 0.95,
      dashArray: '10, 10',
      className: 'route-path-animated'
    });

    this.routeLayer = L.featureGroup([glowLine, coreLine]).addTo(this.map);

    // Zoom and pan smoothly to fit route
    if (currentFloorPoints.length > 1) {
      this.map.fitBounds(L.latLngBounds(currentFloorPoints), { padding: [60, 60], maxZoom: 1 });
    }
  },

  clearRoute() {
    if (this.routeLayer) {
      this.routeLayer.remove();
      this.routeLayer = null;
    }
    if (this.routePulseMarker) {
      this.routePulseMarker.remove();
      this.routePulseMarker = null;
    }
    this.activePathNodes = [];
  },

  resetView() {
    this.map.fitBounds([[0, 0], [600, 900]]);
    AudioSynthesizer.playChime(520, 0.1);
  }
};
