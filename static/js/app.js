/**
 * Main Passenger Navigation Application Controller
 * Handles UI events, state, search, route calculation and simulation
 */

const AppState = {
  currentStationId: window.CURRENT_STATION_ID || 'NDLS',
  userLocationNodeId: 'ndls_gate1', // default starting gate
  targetDestinationNodeId: null,
  wheelchairMode: false,
  kioskMode: false,
  highContrast: false,
  selectedCategory: 'all',
  nodes: [],
  facilities: [],
  trains: [],
  activeRoute: null,
  currentStepIndex: 0,
  language: 'en'
};

document.addEventListener('DOMContentLoaded', () => {
  initApp();
});

async function initApp() {
  // 1. Initialize Map and Speech Engine
  StationMap.init('station-map');
  VoiceEngine.init();

  // 2. Fetch Initial Station Data
  await loadStationData();

  // 3. Attach Event Listeners
  setupEventListeners();

  console.log("RailNav AI Passenger Application initialized successfully.");
}

async function loadStationData() {
  try {
    const stationId = AppState.currentStationId;

    // Load Nodes
    const nodesRes = await fetch(`/api/nodes?station_id=${stationId}`);
    AppState.nodes = await nodesRes.json();
    StationMap.loadNodes(AppState.nodes);

    // Load Facilities
    await loadFacilities();

    // Load Live Trains
    await loadTrains();

  } catch (err) {
    console.error("Failed to load station data:", err);
  }
}

async function loadFacilities(category = 'all', searchQuery = '') {
  try {
    const stationId = AppState.currentStationId;
    let url = `/api/facilities?station_id=${stationId}&category=${category}`;
    if (searchQuery) url += `&search=${encodeURIComponent(searchQuery)}`;

    const res = await fetch(url);
    AppState.facilities = await res.json();
    renderFacilitiesList(AppState.facilities);
  } catch (err) {
    console.error("Failed to load facilities:", err);
  }
}

function renderFacilitiesList(facilities) {
  const container = document.getElementById('facilities-list-container');
  const countBadge = document.getElementById('facility-count-badge');
  if (!container) return;

  if (countBadge) countBadge.textContent = `${facilities.length} found`;

  if (facilities.length === 0) {
    container.innerHTML = `
      <div style="padding: 24px; text-align: center; color: var(--text-muted); font-size: 0.85rem;">
        <i class="fa-solid fa-circle-question" style="font-size: 1.5rem; margin-bottom: 8px;"></i>
        <p>No facilities found matching your search.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = facilities.map(fac => {
    const statusClass = `status-${fac.status || 'operational'}`;
    const statusLabel = (fac.status || 'operational').toUpperCase();

    return `
      <div class="facility-card-item" onclick="startNavigationTo('${fac.node_id}', '${fac.name.replace(/'/g, "\\'")}')">
        <div class="facility-meta">
          <div class="fac-icon-box">
            <i class="fa-solid ${fac.icon || 'fa-map-marker-alt'}"></i>
          </div>
          <div class="fac-details">
            <h4>${fac.name}</h4>
            <p>
              <span>Floor: ${fac.floor === 1 ? 'Level 1 (FOB)' : 'Ground Level'}</span>
              <span>&bull;</span>
              <span><i class="status-dot ${statusClass}"></i> ${statusLabel}</span>
            </p>
          </div>
        </div>
        <button class="btn-icon" style="width: 32px; height: 32px; border-radius: 50%; color: var(--cyan-glow);" title="Navigate here">
          <i class="fa-solid fa-diamond-turn-right"></i>
        </button>
      </div>
    `;
  }).join('');
}

async function loadTrains() {
  try {
    const stationId = AppState.currentStationId;
    const res = await fetch(`/api/trains?station_id=${stationId}`);
    AppState.trains = await res.json();
    renderTrainsList(AppState.trains);
  } catch (err) {
    console.error("Failed to load trains:", err);
  }
}

function renderTrainsList(trains) {
  const container = document.getElementById('trains-list-container');
  if (!container) return;

  if (trains.length === 0) {
    container.innerHTML = `<p style="color: var(--text-muted); font-size: 0.8rem; text-align: center;">No trains scheduled in this window.</p>`;
    return;
  }

  container.innerHTML = trains.map(t => {
    // Determine platform node
    const platNodeId = getPlatformNodeId(t.platform);
    return `
      <div class="train-item-row">
        <div class="train-info">
          <h4>${t.train_number} - ${t.train_name}</h4>
          <p>
            <span style="color: var(--ir-saffron); font-weight: 600;">Dep: ${t.departure_time}</span>
            <span>&bull;</span>
            <span style="color: ${t.delay_minutes > 0 ? '#ef4444' : '#10b981'};">${t.status}</span>
          </p>
        </div>
        <div class="train-platform-badge">
          <span class="plat-num">PF ${t.platform}</span>
          <button class="btn-nav-train" onclick="startNavigationTo('${platNodeId}', 'Platform ${t.platform} (${t.train_name.replace(/'/g, "\\'")})')">
            <i class="fa-solid fa-diamond-turn-right"></i> Navigate
          </button>
        </div>
      </div>
    `;
  }).join('');
}

function getPlatformNodeId(platNum) {
  const num = String(platNum);
  if (num === '1') return 'ndls_p1_center';
  if (num === '2') return 'ndls_p2_center';
  if (num === '3') return 'ndls_p3_center';
  if (num === '4') return 'ndls_p4_center';
  if (num === '5') return 'ndls_p5_center';
  if (num === '6') return 'ndls_p6_center';
  if (num === '7') return 'ndls_p7_center';
  return 'ndls_p1_center';
}

function setupEventListeners() {
  // Search input live filtering
  const searchInput = document.getElementById('facility-search-input');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const q = e.target.value.trim();
      loadFacilities(AppState.selectedCategory, q);
    });
  }

  // Voice Search button
  const voiceSearchBtn = document.getElementById('btn-voice-search');
  if (voiceSearchBtn) {
    voiceSearchBtn.addEventListener('click', () => {
      VoiceEngine.startVoiceRecognition();
    });
  }

  // Category filter chips
  const chipsContainer = document.getElementById('category-chips');
  if (chipsContainer) {
    chipsContainer.addEventListener('click', (e) => {
      const chip = e.target.closest('.chip-btn');
      if (!chip) return;

      document.querySelectorAll('.chip-btn').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');

      AppState.selectedCategory = chip.dataset.category || 'all';
      const q = searchInput ? searchInput.value.trim() : '';
      loadFacilities(AppState.selectedCategory, q);
      AudioSynthesizer.playChime(500, 0.08);
    });
  }

  // Wheelchair mode buttons (Header + Map overlay)
  const btnToggleWheelchair = document.getElementById('btn-toggle-wheelchair');
  const btnMapWheelchair = document.getElementById('btn-map-wheelchair');

  if (btnToggleWheelchair) {
    btnToggleWheelchair.addEventListener('click', toggleWheelchairMode);
  }
  if (btnMapWheelchair) {
    btnMapWheelchair.addEventListener('click', toggleWheelchairMode);
  }

  // Voice guidance toggle button
  const btnToggleVoice = document.getElementById('btn-toggle-voice');
  if (btnToggleVoice) {
    btnToggleVoice.addEventListener('click', () => {
      VoiceEngine.ttsEnabled = !VoiceEngine.ttsEnabled;
      btnToggleVoice.classList.toggle('active', VoiceEngine.ttsEnabled);
      AudioSynthesizer.playChime(VoiceEngine.ttsEnabled ? 660 : 330, 0.15);
      if (VoiceEngine.ttsEnabled) {
        VoiceEngine.speak("Voice guidance enabled");
      }
    });
  }

  // Kiosk mode toggle button
  const btnToggleKiosk = document.getElementById('btn-toggle-kiosk');
  if (btnToggleKiosk) {
    btnToggleKiosk.addEventListener('click', () => {
      AppState.kioskMode = !AppState.kioskMode;
      document.body.classList.toggle('kiosk-mode', AppState.kioskMode);
      btnToggleKiosk.classList.toggle('active', AppState.kioskMode);
      AudioSynthesizer.playChime(550, 0.15);
    });
  }

  // High contrast mode toggle button
  const btnToggleContrast = document.getElementById('btn-toggle-contrast');
  if (btnToggleContrast) {
    btnToggleContrast.addEventListener('click', () => {
      AppState.highContrast = !AppState.highContrast;
      document.body.classList.toggle('accessible-contrast', AppState.highContrast);
      btnToggleContrast.classList.toggle('active', AppState.highContrast);
      AudioSynthesizer.playChime(600, 0.15);
    });
  }

  // Language selector
  const langSelector = document.getElementById('lang-selector');
  if (langSelector) {
    langSelector.addEventListener('change', (e) => {
      AppState.language = e.target.value;
      VoiceEngine.currentLanguage = AppState.language;
      updateUILanguage(AppState.language);
      AudioSynthesizer.playChime(600, 0.1);
    });
  }
}

const I18N = {
  en: {
    searchPlaceholder: "Search platform, ticket, food, washroom...",
    categories: {
      all: "All",
      platform: "Platforms",
      restroom: "Restrooms",
      ticket: "Ticketing",
      food: "Food Plaza",
      waiting_hall: "Lounges",
      lift: "Lifts & Ramps",
      medical: "Medical & RPF"
    },
    speechBtn: "Spoken Guide",
    accOn: "Accessible Route: ON ♿",
    accOff: "Accessible Route: Off",
    stepFreeBadge: "Step-Free ♿"
  },
  hi: {
    searchPlaceholder: "प्लेटफ़ॉर्म, टिकट, खान-पान, शौचालय खोजें...",
    categories: {
      all: "सभी",
      platform: "प्लेटफ़ॉर्म",
      restroom: "शौचालय",
      ticket: "टिकट काउंटर",
      food: "खान-पान",
      waiting_hall: "प्रतीक्षालय",
      lift: "लिफ्ट एवं रैंप",
      medical: "चिकित्सा व सुरक्षा"
    },
    speechBtn: "ध्वनि मार्गदर्शन",
    accOn: "सुगम्य मार्ग: चालू ♿",
    accOff: "सुगम्य मार्ग: बंद",
    stepFreeBadge: "सुगम्य मार्ग ♿"
  },
  ta: {
    searchPlaceholder: "நடைமேடை, டிக்கெட், உணவு, கழிவறை தேடவும்...",
    categories: {
      all: "அனைத்தும்",
      platform: "நடைமேடை",
      restroom: "கழிவறை",
      ticket: "டிக்கெட் மையம்",
      food: "உணவகம்",
      waiting_hall: "காத்திருப்பு அறை",
      lift: "மின்தூக்கி & சாய்வுதளம்",
      medical: "மருத்துவம் & காவல்துறை"
    },
    speechBtn: "குரல் வழிகாட்டி",
    accOn: "சாய்வுதள பாதை: ஆன் ♿",
    accOff: "சாய்வுதள பாதை: ஆஃப்",
    stepFreeBadge: "தடையில்லா பாதை ♿"
  }
};

function updateUILanguage(lang) {
  const dict = I18N[lang] || I18N.en;

  // Search placeholder
  const searchInput = document.getElementById('facility-search-input');
  if (searchInput) searchInput.placeholder = dict.searchPlaceholder;

  // Category chips
  document.querySelectorAll('.chip-btn').forEach(btn => {
    const cat = btn.dataset.category;
    if (cat && dict.categories[cat]) {
      // Preserve icon
      const icon = btn.querySelector('i');
      btn.innerHTML = '';
      if (icon) btn.appendChild(icon);
      btn.appendChild(document.createTextNode(' ' + dict.categories[cat]));
    }
  });

  // Speech button
  const speechLabel = document.getElementById('speech-btn-label');
  if (speechLabel) speechLabel.textContent = dict.speechBtn;

  // Accessible route label
  const lbl = document.getElementById('wheelchair-label');
  if (lbl) lbl.textContent = AppState.wheelchairMode ? dict.accOn : dict.accOff;

  // Accessibility badge
  const accBadge = document.getElementById('route-accessibility-badge');
  if (accBadge) accBadge.innerHTML = `<i class="fa-solid fa-wheelchair"></i> ${dict.stepFreeBadge}`;
}

function toggleWheelchairMode() {
  AppState.wheelchairMode = !AppState.wheelchairMode;

  const btnH = document.getElementById('btn-toggle-wheelchair');
  const btnM = document.getElementById('btn-map-wheelchair');
  const lbl = document.getElementById('wheelchair-label');

  if (btnH) btnH.classList.toggle('active', AppState.wheelchairMode);
  if (btnM) btnM.classList.toggle('active', AppState.wheelchairMode);
  if (lbl) lbl.textContent = AppState.wheelchairMode ? "Accessible Route: ON ♿" : "Accessible Route: Off";

  AudioSynthesizer.playChime(AppState.wheelchairMode ? 700 : 350, 0.15);

  if (AppState.wheelchairMode) {
    VoiceEngine.speak("Wheelchair accessible step-free route mode activated. Stairs and escalators excluded.");
  }

  // Re-calculate route if currently active
  if (AppState.targetDestinationNodeId) {
    startNavigationTo(AppState.targetDestinationNodeId);
  }
}

// Global hook: Start Navigation
window.startNavigationTo = async function(destNodeId, destName = "") {
  AppState.targetDestinationNodeId = destNodeId;
  const startId = AppState.userLocationNodeId || 'ndls_gate1';
  const stationId = AppState.currentStationId;
  const wheelchair = AppState.wheelchairMode;

  try {
    const url = `/api/route?station_id=${stationId}&from=${startId}&to=${destNodeId}&wheelchair=${wheelchair}`;
    const res = await fetch(url);
    const data = await res.json();

    if (!data.success) {
      alert(data.error || "Route could not be calculated.");
      return;
    }

    AppState.activeRoute = data;
    AppState.currentStepIndex = 0;

    // Render route on map
    StationMap.renderRoutePolyline(data.path_nodes);

    // Render turn-by-turn drawer
    renderActiveRouteDrawer(data, destName);

    AudioSynthesizer.playSuccess();

    // Spoken guidance for first step
    if (data.instructions && data.instructions.length > 0) {
      const firstStep = data.instructions[0].text;
      VoiceEngine.speak(firstStep);
    }

  } catch (err) {
    console.error("Navigation error:", err);
  }
};

function renderActiveRouteDrawer(routeData, destName = "") {
  const card = document.getElementById('active-route-card');
  const title = document.getElementById('route-dest-title');
  const startText = document.getElementById('route-start-text');
  const distEl = document.getElementById('route-total-distance');
  const etaEl = document.getElementById('route-total-eta');
  const stepsContainer = document.getElementById('turn-steps-container');
  const accBadge = document.getElementById('route-accessibility-badge');

  if (!card) return;

  const destNode = routeData.path_nodes[routeData.path_nodes.length - 1];
  const startNode = routeData.path_nodes[0];

  title.textContent = destName || destNode.name;
  startText.textContent = `From: ${startNode.name}`;
  distEl.textContent = `${Math.round(routeData.total_distance)} m`;
  etaEl.textContent = `• ~${routeData.estimated_minutes} min walk`;

  if (accBadge) {
    accBadge.style.display = routeData.wheelchair_friendly ? 'inline-flex' : 'none';
  }

  // Populate steps list
  stepsContainer.innerHTML = routeData.instructions.map((step, idx) => `
    <div class="turn-step-item ${idx === 0 ? 'active-step' : ''}" id="step-item-${idx}" onclick="focusStep(${idx})">
      <div class="step-icon-wrap">
        <i class="fa-solid ${step.icon || 'fa-arrow-up'}"></i>
      </div>
      <div class="step-text">
        <p>${step.text}</p>
        ${step.distance > 0 ? `<span class="step-dist">${step.distance} meters</span>` : ''}
      </div>
    </div>
  `).join('');

  card.style.display = 'block';
}

window.simulateStepForward = function() {
  if (!AppState.activeRoute || !AppState.activeRoute.instructions) return;

  const steps = AppState.activeRoute.instructions;
  if (AppState.currentStepIndex < steps.length - 1) {
    AppState.currentStepIndex++;
    focusStep(AppState.currentStepIndex);
  } else {
    AudioSynthesizer.playSuccess();
    VoiceEngine.speak("You have reached your destination.");
  }
};

window.focusStep = function(stepIdx) {
  AppState.currentStepIndex = stepIdx;
  const steps = AppState.activeRoute.instructions;
  const currentStep = steps[stepIdx];

  // Update step visual highlight
  document.querySelectorAll('.turn-step-item').forEach(el => el.classList.remove('active-step'));
  const activeEl = document.getElementById(`step-item-${stepIdx}`);
  if (activeEl) {
    activeEl.classList.add('active-step');
    activeEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  // Move user marker to this step's node
  if (currentStep.node_id) {
    StationMap.updateUserMarker(currentStep.node_id);
    AppState.userLocationNodeId = currentStep.node_id;
  }

  // Auto-switch floor if step changes floor
  if (currentStep.floor !== undefined && currentStep.floor !== StationMap.currentFloor) {
    StationMap.switchFloor(currentStep.floor);
  }

  AudioSynthesizer.playTurnAlert();
  VoiceEngine.speak(currentStep.text);
};

window.clearActiveRoute = function() {
  AppState.activeRoute = null;
  AppState.targetDestinationNodeId = null;
  StationMap.clearRoute();
  VoiceEngine.stop();

  const card = document.getElementById('active-route-card');
  if (card) card.style.display = 'none';

  AudioSynthesizer.playChime(400, 0.1);
};

window.setUserLocation = function(nodeId) {
  AppState.userLocationNodeId = nodeId;
  StationMap.updateUserMarker(nodeId);
  const node = AppState.nodes.find(n => n.id === nodeId);
  const name = node ? node.name : nodeId;
  VoiceEngine.speak(`Current location set to ${name}`);
  AudioSynthesizer.playSuccess();

  // If navigating, recalculate from here
  if (AppState.targetDestinationNodeId) {
    startNavigationTo(AppState.targetDestinationNodeId);
  }
};

window.switchFloor = function(floor) {
  StationMap.switchFloor(floor);
};

window.resetMapView = function() {
  StationMap.resetView();
};

window.startVoiceSearch = function() {
  VoiceEngine.startVoiceRecognition();
};

window.toggleSpeechReadout = function() {
  if (!AppState.activeRoute) return;
  const currentStep = AppState.activeRoute.instructions[AppState.currentStepIndex];
  if (currentStep) {
    VoiceEngine.speak(currentStep.text);
  }
};

window.stopSpeechReadout = function() {
  VoiceEngine.stop();
};

// QR Checkpoint Resolver
window.simulateQRScan = async function(token) {
  closeModal('qr-modal');
  try {
    const res = await fetch(`/api/qr_resolve?code=${encodeURIComponent(token)}`);
    const data = await res.json();
    if (data.success && data.node) {
      setUserLocation(data.node.id);
      alert(`Checkpoint Identified: ${data.node.name} (${data.node.description})`);
    } else {
      alert("Invalid QR Checkpoint");
    }
  } catch (e) {
    console.error("QR error:", e);
  }
};

window.handleManualQR = function() {
  const token = document.getElementById('manual-qr-input').value.trim();
  if (token) simulateQRScan(token);
};
