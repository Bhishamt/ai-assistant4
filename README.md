# Iron Man Jarvis AI Assistant 🤖

An intelligent, voice-enabled AI Assistant inspired by Iron Man's JARVIS. Built with Python, LiveKit Agents, Realtime Gemini/LLM models, OpenWeather API, Google Search API, and native Windows automation capabilities.

---

## 🌟 Key Features

- 🎙️ **Real-Time Voice & Multimodal Interaction**: Powered by LiveKit Agents and Google's Realtime LLM models.
- 🔍 **Google Search Integration**: Instant web searches via Google Custom Search API with structured result parsing.
- 🌤️ **Weather Information**: Real-time weather data by city or auto-detected IP/saved address via OpenWeather API.
- 🖥️ **Windows App & Window Control**: Launch, focus, bring to foreground, and close desktop applications safely.
- 📁 **File & Folder Management**: Fuzzy search file indexing, automatic window activation on file launch, and directory navigation.
- 🖱️ **Safe Keyboard & Mouse Automation**: Token-protected controller for mouse movement, clicks, scrolling, hotkeys, and volume adjustments.

---

## 🛡️ Architecture & Security Guardrails

- **Token-Gated Hardware Controller**: Mouse and keyboard control functions (`keyboard_mouse_CTRL.py`) feature a `SafeController` pattern that auto-activates only with secret tokens during tool execution.
- **Robust Path & Directory Handling**: File indexing (`jarvis_file_opener.py`) gracefully handles non-existent paths and permission restrictions.
- **Async Execution & Timeout Safety**: Weather and search operations enforce HTTP timeouts and fallback logic to guarantee real-time voice responsiveness.

---

## 📁 Repository Structure

```text
├── agent.py                 # Main LiveKit entry point and Assistant agent definition
├── jarvis_prompts.py        # System instructions and behavior prompts
├── jarvis_get_weather.py    # OpenWeather API integration and location detection
├── jarvis_google_search.py # Google Custom Search API integration
├── jarvis_window_CTRL.py   # Windows app launching, focus, and window controls
├── jarvis_file_opener.py   # Desktop file searching and media playback
├── keyboard_mouse_CTRL.py  # Automation for mouse movement, clicks, and keyboard shortcuts
├── addrees.json            # Location metadata configuration
└── requirements.txt        # Python dependencies
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites

- Python 3.9+
- Windows OS (for GUI & window control features)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables Setup

Create a `.env` file in the root directory with the following keys:

```env
LIVEKIT_URL=your_livekit_url
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
GOOGLE_SEARCH_API_KEY=your_google_search_api_key
SEARCH_ENGINE_ID=your_custom_search_engine_id
OPENWEATHER_API_KEY=your_openweather_api_key
```

---

## 🚀 Running the Assistant

Run the agent worker using:

```bash
python agent.py start
```

---

## 🤝 Author & License

Developed by **Bhisham Thakur** ([@Bhishamt](https://github.com/Bhishamt)).
Released under the MIT License.

