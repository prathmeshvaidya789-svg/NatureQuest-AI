# 🌿 NatureQuest-AI

> **Hacktoberfest 2026 Touch Grass Challenge Entry**  
> A responsive, privacy-first web application that motivates students and developers to disconnect from screen fatigue and explore the outdoors through personalized, AI-guided nature missions, gamification, and mindful field journaling.

---

## 📖 Overview

Tech marathons, late-night debugging sessions, and continuous screen time take a heavy toll on cognitive focus and physical well-being. **NatureQuest-AI** transforms the outdoor world into an interactive quest log.

Whether you have 15 minutes between lectures or an hour on the weekend, NatureQuest-AI synthesizes your chosen activity, available time, difficulty preference, and setting into a concrete, mindful outdoor mission with actionable steps, safety reminders, and gamified progress.

---

## 🌟 Upgraded Features

### 1. 🤖 Local AI Mission Generation
- **Local Ollama Model (`qwen2.5:0.5b`):** Connects to `http://localhost:11434/api/tags` for health checks and calls `http://localhost:11434/api/generate` with `format="json"` for structured generation.
- **Rich Schema:** Generates a catchy title, codename, **concrete objective**, **why this activity gets you outdoors** explanation, **3–5 actionable steps**, required items, and safety stewardship tips.
- **Robust Validation & Error Handling:** Validates schema types, handles timeouts or daemon drops gracefully, and clearly labels fallback missions when active.

### 2. 🏆 Gamification & Anti-Duplicate Rewards
- **XP on Completion:** XP is awarded **only** when a mission is marked as completed (scaled by duration and difficulty, with a bonus for local AI generation).
- **Anti-Duplicate Protection:** The app prevents accidental duplicate rewards and duplicate XP for the same mission.
- **Explorer Ranks (6 Levels):** Progress from *Sprout Scout* (Lvl 1) to *Master Naturalist* (Lvl 6) with real-time level progress bars.
- **Active Daily Streak (🔥):** Automatically calculated from actual `completed_at` calendar dates.
- **Badges & Achievements:** 10 unlocks (e.g., *First Footprint*, *Trail Strider*, *Consistency Flame*, *Field Scribe*) evaluated strictly against actual user records.

### 3. 📝 Nature Journal (Privacy-First)
- **Mindful Observations:** Record field notes, sensory observations, and date stamps.
- **Optional Field Photos:** Attach photos (`.jpg`, `.png`, `.webp`) saved locally in `journal_photos/`.
- **Zero Precise Location Tracking:** Does not gather GPS coordinates or IP geolocations; users choose general settings (e.g. *Campus Quad*, *Neighborhood Park*).

### 4. 📊 Progress Dashboard
- **Actual Saved Data:** Displays verified mission counts, cumulative outdoor air minutes, weekly activity, XP, and active streaks.
- **Weekly Activity Chart:** Interactive 7-day bar chart showing daily outdoor minutes logged over the past week.
- **Achievement Gallery:** Clean visual badges displaying unlock status and requirements.
- **Completed Missions Logbook:** Searchable history of completed missions with student reflection notes and export/clear controls.

### 5. 💾 Offline-Friendly Missions
- **Mission Stash:** Every generated quest can be stashed to `saved_missions.json` to remain accessible offline without internet or Ollama.
- **Instant Offline Generator:** Create handcrafted curated missions instantly with zero dependencies.
- **Transparent Offline Status:** Clearly identifies whether a quest came from local Ollama AI, the offline stash, or the curated offline bank.

---

## 🛠️ Tech Stack

- **Frontend Framework:** [Streamlit](https://streamlit.io/) (Python)
- **Local AI Engine:** [qwen2.5:0.5b](https://ollama.com/library/qwen2.5) via [Ollama](https://ollama.com)
- **Styling:** Streamlit Theming Engine + Vanilla CSS (Forest Green, Sage & Warm Amber)
- **Local Persistence:** Local JSON files (`completed_missions.json`, `nature_journal.json`, `saved_missions.json`) & local photo directory (`journal_photos/`)

---

## 🚀 Quickstart Guide for Windows

Follow these steps in **PowerShell**:

### 1. Prerequisites
- **Python 3.10+** ([python.org](https://www.python.org/downloads/))
- **Ollama** installed ([ollama.com/download](https://ollama.com/download/windows))

*(Note: If Ollama is not installed, the app runs smoothly in **Curated Offline Fallback Mode**).*

---

### 2. Setup Virtual Environment & Dependencies

```powershell
# Navigate to the project directory
cd c:\Users\user\OneDrive\Desktop\NatureQuest-AI

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# Install / update dependencies
pip install -r requirements.txt
```

---

### 3. Start the Local AI Model (Ollama)

Make sure Ollama is running and the model tag `qwen2.5:0.5b` is downloaded:

```powershell
ollama run qwen2.5:0.5b
```

Once started, Ollama listens in the background at `http://localhost:11434`. (Type `/bye` to exit the chat prompt; the background daemon remains active).

---

### 4. Launch the Web Application

In a terminal window:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

The app opens automatically in your browser at:
👉 **`http://localhost:8501`**

---

## 🧪 Testing & Verification

We maintain an automated integration test suite (`test_upgraded_app.py`) built on Streamlit's `AppTest` framework that verifies all 5 core features:

To run the automated test suite:

```powershell
.\.venv\Scripts\python.exe C:\Users\user\.gemini\antigravity-ide\brain\5b03b537-a0b4-43cc-a427-7249c6ee17fb\scratch\test_upgraded_app.py
```

### Verified Test Results:
- ✅ **Test 1 (Sidebar Status):** Health check at `http://localhost:11434/api/tags` returned `200 OK` with model `qwen2.5:0.5b`. Sidebar correctly shows `🟢 Ollama Connected`.
- ✅ **Test 2 (AI Generation):** Generates structured quest using `/api/generate` with valid title, objective, 3–5 steps, required items, safety tips, and outdoor rationale.
- ✅ **Test 3 (Gamification & Duplicate Prevention):** Awarded 125 XP on mission completion; duplicate attempt on the same quest was blocked with a warning.
- ✅ **Test 4 (Nature Journal):** Saved field observation with notes and date; verified zero GPS collection.
- ✅ **Test 5 (Progress Dashboard):** Verified real-time metric computation (missions, XP, active daily streak, 7-day activity).
- ✅ **Test 6 (Offline Fallback & Stash):** Stashed missions persist; simulated offline daemon smoothly switched to Curated Offline Fallback Mode.

---

## ⚠️ Known Limitations & Transparency

1. **Local AI Dependency:** AI generation requires the Ollama background daemon and the `qwen2.5:0.5b` model weights. If Ollama is closed, the app automatically switches to Curated Fallback Mode.
2. **Local Storage:** All user data, completed quests, and journal photos are stored locally on your machine in `.gitignore`'d JSON files and the `journal_photos/` folder. Clearing your browser cache or deleting JSON files resets local progress.
3. **No GPS / Cloud Sync:** To safeguard privacy, location data is never captured, and missions are not synced to external cloud databases.

---

## 🛡️ Safety & Stewardship (Leave No Trace)

Every NatureQuest-AI mission promotes outdoor ethics:
1. **Plan ahead and prepare.**
2. **Travel on durable surfaces.**
3. **Dispose of waste properly.**
4. **Leave what you find.**
5. **Respect wildlife from a safe distance.**
6. **Be considerate of other visitors.**

---

## 📄 License & Hacktoberfest Note

Created for the **Hacktoberfest 2026 Touch Grass Challenge**. Distributed under the MIT License.
