/**
 * Voice Assistance Engine using Web Speech API
 * Implements Text-to-Speech (TTS) Voice Guidance & Speech Recognition (STT)
 */

const VoiceEngine = {
  ttsEnabled: true,
  synth: window.speechSynthesis || null,
  recognition: null,
  isListening: false,
  currentLanguage: 'en', // 'en', 'hi', 'ta'
  voices: [],

  init() {
    if (this.synth) {
      this.loadVoices();
      if (this.synth.onvoiceschanged !== undefined) {
        this.synth.onvoiceschanged = () => this.loadVoices();
      }
    }

    // Initialize Web Speech Recognition if available
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRec) {
      this.recognition = new SpeechRec();
      this.recognition.continuous = false;
      this.recognition.interimResults = false;
      this.recognition.lang = 'en-IN'; // Indian English by default

      this.recognition.onstart = () => {
        this.isListening = true;
        this.updateVisualizer(true, "Listening... Say 'Platform 3' or 'Restroom'");
        const micBtn = document.getElementById('btn-voice-search');
        if (micBtn) micBtn.classList.add('listening');
      };

      this.recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        this.handleVoiceQuery(transcript);
      };

      this.recognition.onerror = (event) => {
        this.updateVisualizer(false);
        this.isListening = false;
        const micBtn = document.getElementById('btn-voice-search');
        if (micBtn) micBtn.classList.remove('listening');
      };

      this.recognition.onend = () => {
        this.isListening = false;
        const micBtn = document.getElementById('btn-voice-search');
        if (micBtn) micBtn.classList.remove('listening');
        setTimeout(() => this.updateVisualizer(false), 2000);
      };
    }
  },

  loadVoices() {
    if (!this.synth) return;
    this.voices = this.synth.getVoices();
  },

  getPreferredVoice(lang) {
    if (!this.voices || this.voices.length === 0) return null;
    if (lang === 'hi') {
      return this.voices.find(v => v.lang.startsWith('hi')) || this.voices[0];
    }
    if (lang === 'ta') {
      return this.voices.find(v => v.lang.startsWith('ta')) || this.voices[0];
    }
    // Indian English or clear English voice
    return this.voices.find(v => v.lang === 'en-IN') ||
           this.voices.find(v => v.lang.startsWith('en')) ||
           this.voices[0];
  },

  speak(text) {
    if (!this.ttsEnabled || !this.synth) return;

    this.synth.cancel(); // Stop any pending utterance
    const utterance = new SpeechSynthesisUtterance(text);
    const voice = this.getPreferredVoice(this.currentLanguage);
    if (voice) utterance.voice = voice;
    utterance.rate = 0.95; // Clear passenger announcement pace
    utterance.pitch = 1.0;

    utterance.onstart = () => {
      this.updateVisualizer(true, text);
    };

    utterance.onend = () => {
      setTimeout(() => this.updateVisualizer(false), 1200);
    };

    this.synth.speak(utterance);
  },

  stop() {
    if (this.synth) this.synth.cancel();
    this.updateVisualizer(false);
  },

  startVoiceRecognition() {
    if (!this.recognition) {
      // Fallback if browser doesn't support Web Speech Recognition
      const query = prompt("Speak or type station voice query (e.g. 'Platform 3', 'Restroom', 'Food', 'Wheelchair'):", "Platform 3");
      if (query) this.handleVoiceQuery(query);
      return;
    }

    try {
      if (this.isListening) {
        this.recognition.stop();
      } else {
        AudioSynthesizer.playChime(660, 0.15);
        this.recognition.start();
      }
    } catch (e) {
      console.warn("Speech recognition error:", e);
    }
  },

  handleVoiceQuery(query) {
    if (!query) return;
    const cleanQuery = query.toLowerCase().trim();
    this.updateVisualizer(true, `Recognized: "${query}"`);

    // Put into search bar
    const searchInput = document.getElementById('facility-search-input');
    if (searchInput) {
      searchInput.value = query;
      searchInput.dispatchEvent(new Event('input'));
    }

    // Direct Smart Intent Routing
    if (cleanQuery.includes('platform 1')) {
      window.startNavigationTo('ndls_p1_center');
      this.speak("Routing to Platform 1 Vande Bharat Express");
    } else if (cleanQuery.includes('platform 2')) {
      window.startNavigationTo('ndls_p2_center');
      this.speak("Routing to Platform 2 Bhopal Shatabdi");
    } else if (cleanQuery.includes('platform 3')) {
      window.startNavigationTo('ndls_p3_center');
      this.speak("Routing to Platform 3 Mumbai Rajdhani");
    } else if (cleanQuery.includes('platform 4')) {
      window.startNavigationTo('ndls_p4_center');
      this.speak("Routing to Platform 4 Howrah Rajdhani");
    } else if (cleanQuery.includes('washroom') || cleanQuery.includes('restroom') || cleanQuery.includes('toilet')) {
      window.startNavigationTo('ndls_restroom_ground');
      this.speak("Routing to Main Station Restrooms and Divyang Washroom");
    } else if (cleanQuery.includes('food') || cleanQuery.includes('eat') || cleanQuery.includes('restaurant')) {
      window.startNavigationTo('ndls_food_plaza');
      this.speak("Routing to IRCTC Jan Aahar Food Plaza");
    } else if (cleanQuery.includes('ticket') || cleanQuery.includes('booking')) {
      window.startNavigationTo('ndls_uts_counters');
      this.speak("Routing to UTS General Ticketing Office");
    } else if (cleanQuery.includes('wheelchair') || cleanQuery.includes('help')) {
      openModal('sos-modal');
      this.speak("Opening Wheelchair and Sahayak assistance desk");
    } else {
      this.speak(`Searching station facilities for ${query}`);
    }
  },

  updateVisualizer(show, message = "") {
    const el = document.getElementById('voice-visualizer');
    const msgEl = document.getElementById('voice-status-msg');
    if (!el) return;

    if (show) {
      el.style.display = 'flex';
      if (msgEl && message) msgEl.textContent = message;
    } else {
      el.style.display = 'none';
    }
  }
};
