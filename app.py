"""
NatureQuest-AI
Hacktoberfest 2026 Touch Grass Challenge
Empowering students to reconnect with the outdoors through personalized, AI-guided missions.
"""

import os
import json
import random
import datetime
import hashlib
from typing import Dict, Any, Tuple, List, Optional
import requests
import streamlit as st
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()

DEFAULT_OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:0.5b")
DEFAULT_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "45"))

COMPLETED_MISSIONS_FILE = "completed_missions.json"
JOURNAL_FILE = "nature_journal.json"
SAVED_MISSIONS_FILE = "saved_missions.json"
PHOTOS_DIR = "journal_photos"

# Ensure local directories exist
os.makedirs(PHOTOS_DIR, exist_ok=True)

# Set Streamlit Page Config
st.set_page_config(
    page_title="NatureQuest-AI | Touch Grass Challenge",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Green & White CSS for high polish & responsive design
st.markdown(
    """
    <style>
    /* Global Styling */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%);
        color: #ffffff;
        padding: 2.2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 25px -5px rgba(27, 67, 50, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-banner h1 {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.02em;
    }
    .hero-banner p {
        color: #d8f3dc;
        font-size: 1.05rem;
        margin: 0;
        max-width: 820px;
        line-height: 1.5;
    }
    .hero-badge {
        display: inline-block;
        background-color: #40916c;
        color: #ffffff;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        margin-bottom: 0.8rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* Cards */
    .nature-card {
        background-color: #ffffff;
        border: 1px solid #d8e2dc;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }

    .badge-pill {
        display: inline-block;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .badge-green {
        background-color: #e8f5e9;
        color: #1b4332;
        border: 1px solid #c8e6c9;
    }
    .badge-accent {
        background-color: #d8f3dc;
        color: #2d6a4f;
        border: 1px solid #b7e4c7;
    }
    .badge-fallback {
        background-color: #fff3e0;
        color: #e65100;
        border: 1px solid #ffe082;
    }
    .badge-ollama {
        background-color: #e0f2fe;
        color: #0369a1;
        border: 1px solid #bae6fd;
    }
    .badge-xp {
        background-color: #fef3c7;
        color: #92400e;
        border: 1px solid #fde68a;
    }
    .badge-streak {
        background-color: #fee2e2;
        color: #b91c1c;
        border: 1px solid #fecaca;
    }
    .badge-level {
        background-color: #ede9fe;
        color: #5b21b6;
        border: 1px solid #ddd6fe;
    }
    .badge-locked {
        background-color: #f3f4f6;
        color: #9ca3af;
        border: 1px solid #e5e7eb;
    }

    /* Stat Cards */
    .stat-box {
        background-color: #ffffff;
        border-radius: 12px;
        border: 1px solid #e2ece9;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    .stat-number {
        font-size: 1.9rem;
        font-weight: 700;
        color: #2d6a4f;
        line-height: 1.2;
    }
    .stat-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: #52796f;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-top: 0.3rem;
    }

    /* Objective and Why-Outdoors callout boxes */
    .objective-callout {
        background-color: #f4fbf7;
        border-left: 4px solid #2d6a4f;
        padding: 0.9rem 1.1rem;
        border-radius: 0 10px 10px 0;
        margin: 0.8rem 0;
        color: #1b3322;
        font-size: 0.96rem;
    }
    .why-callout {
        background-color: #effaf4;
        border: 1px dashed #74c69d;
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        margin: 0.8rem 0;
        color: #204e38;
        font-size: 0.93rem;
        line-height: 1.45;
    }

    /* Step checklist list item */
    .step-item {
        background-color: #f8faf8;
        border-left: 4px solid #40916c;
        padding: 0.8rem 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.6rem;
        color: #1b3322;
        font-size: 0.95rem;
    }

    /* Journal Card */
    .journal-entry-card {
        background-color: #ffffff;
        border: 1px solid #d8e2dc;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 3px 8px rgba(0,0,0,0.02);
    }

    /* Badge Achievement Card */
    .badge-card {
        background-color: #ffffff;
        border-radius: 12px;
        border: 1px solid #e2ece9;
        padding: 1rem;
        text-align: center;
        margin-bottom: 0.8rem;
        height: 100%;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }

    /* Streamlit widget tweaks */
    div.stButton > button:first-child {
        background-color: #2d6a4f;
        color: white;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        padding: 0.6rem 1.4rem;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        background-color: #1b4332;
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(45, 106, 79, 0.3);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Storage & Persistence Helpers
# ---------------------------------------------------------------------------

def load_json_file(filepath: str, default: Any) -> Any:
    """Safely loads JSON data from a local file, returning default on error."""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_json_file(filepath: str, data: Any) -> bool:
    """Safely writes JSON data to a local file."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def load_completed_missions() -> List[Dict[str, Any]]:
    return load_json_file(COMPLETED_MISSIONS_FILE, [])

def save_completed_missions(missions: List[Dict[str, Any]]) -> bool:
    return save_json_file(COMPLETED_MISSIONS_FILE, missions)

def load_journal_entries() -> List[Dict[str, Any]]:
    return load_json_file(JOURNAL_FILE, [])

def save_journal_entries(entries: List[Dict[str, Any]]) -> bool:
    return save_json_file(JOURNAL_FILE, entries)

def load_saved_missions() -> List[Dict[str, Any]]:
    return load_json_file(SAVED_MISSIONS_FILE, [])

def save_saved_missions(missions: List[Dict[str, Any]]) -> bool:
    return save_json_file(SAVED_MISSIONS_FILE, missions)

# Initialize Session State
if "completed_missions" not in st.session_state:
    st.session_state.completed_missions = load_completed_missions()

if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = load_journal_entries()

if "saved_missions" not in st.session_state:
    st.session_state.saved_missions = load_saved_missions()

if "current_mission" not in st.session_state:
    st.session_state.current_mission = None

# ---------------------------------------------------------------------------
# Gamification Engine: XP, Levels, Badges, and Streaks
# ---------------------------------------------------------------------------

def calculate_mission_xp(duration: str, difficulty: str, source: str) -> int:
    """Calculates XP awarded for completing a mission based on duration and difficulty."""
    dur_val = 30
    if duration:
        first_token = duration.split()[0]
        if first_token.isdigit():
            dur_val = int(first_token)
    
    if dur_val <= 15:
        base = 50
    elif dur_val <= 30:
        base = 100
    elif dur_val <= 45:
        base = 150
    else:
        base = 200

    diff_lower = (difficulty or "Easy").lower()
    if "challenging" in diff_lower:
        mult = 1.5
    elif "medium" in diff_lower:
        mult = 1.25
    else:
        mult = 1.0

    xp = int(base * mult)
    if "ollama" in (source or "").lower():
        xp += 25  # Local AI engagement bonus
    return xp

LEVEL_DEFINITIONS = [
    (1, "Sprout Scout", 0, 150),
    (2, "Trail Walker", 150, 350),
    (3, "Canopy Explorer", 350, 650),
    (4, "Forest Ranger", 650, 1050),
    (5, "Wilderness Guide", 1050, 1550),
    (6, "Master Naturalist", 1550, 999999),
]

def calculate_level(total_xp: int) -> Tuple[int, str, int, int, float]:
    """Returns: (level_number, level_title, current_xp, next_level_xp, progress_fraction)"""
    for lvl, title, min_xp, max_xp in LEVEL_DEFINITIONS:
        if total_xp < max_xp:
            curr_in_lvl = max(0, total_xp - min_xp)
            span = max(1, max_xp - min_xp)
            prog = min(max(curr_in_lvl / span, 0.0), 1.0)
            return lvl, title, total_xp, max_xp, prog
    return 6, "Master Naturalist", total_xp, total_xp, 1.0

def calculate_streak(completed_missions: List[Dict[str, Any]]) -> int:
    """Calculates the active consecutive daily streak from actual completion dates."""
    if not completed_missions:
        return 0
    dates = set()
    for m in completed_missions:
        c_at = m.get("completed_at")
        if c_at:
            try:
                d_str = c_at.split()[0]
                d = datetime.datetime.strptime(d_str, "%Y-%m-%d").date()
                dates.add(d)
            except Exception:
                pass
    if not dates:
        return 0
    sorted_dates = sorted(dates, reverse=True)
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    latest = sorted_dates[0]
    
    # If the user hasn't completed a quest today or yesterday, streak is broken
    if latest != today and latest != yesterday:
        return 0
        
    streak = 1
    curr = latest
    for next_d in sorted_dates[1:]:
        if next_d == curr - datetime.timedelta(days=1):
            streak += 1
            curr = next_d
        elif next_d == curr:
            continue
        else:
            break
    return streak

BADGES = [
    {
        "id": "first_mission",
        "name": "First Footprint",
        "icon": "🌱",
        "description": "Complete your very first outdoor quest.",
        "check": lambda missions, journal, streak, mins: len(missions) >= 1
    },
    {
        "id": "walker",
        "name": "Trail Strider",
        "icon": "🚶",
        "description": "Complete at least 3 walking or trekking quests.",
        "check": lambda missions, journal, streak, mins: sum(1 for m in missions if m.get("activity") == "walking") >= 3
    },
    {
        "id": "birdwatcher",
        "name": "Avian Observer",
        "icon": "🦅",
        "description": "Complete at least 2 birdwatching quests.",
        "check": lambda missions, journal, streak, mins: sum(1 for m in missions if m.get("activity") == "birdwatching") >= 2
    },
    {
        "id": "gardener",
        "name": "Green Thumb",
        "icon": "🌿",
        "description": "Complete at least 2 gardening quests.",
        "check": lambda missions, journal, streak, mins: sum(1 for m in missions if m.get("activity") == "gardening") >= 2
    },
    {
        "id": "photographer",
        "name": "Shutter Naturalist",
        "icon": "📸",
        "description": "Complete at least 2 nature photography quests.",
        "check": lambda missions, journal, streak, mins: sum(1 for m in missions if m.get("activity") == "nature photography") >= 2
    },
    {
        "id": "hour_wild",
        "name": "Hour in the Wild",
        "icon": "⏱️",
        "description": "Log 60+ cumulative minutes touching grass.",
        "check": lambda missions, journal, streak, mins: mins >= 60
    },
    {
        "id": "streak_2",
        "name": "Consistency Flame",
        "icon": "🔥",
        "description": "Achieve an active daily streak of 2 or more days.",
        "check": lambda missions, journal, streak, mins: streak >= 2
    },
    {
        "id": "journal_entry",
        "name": "Field Scribe",
        "icon": "📝",
        "description": "Record your first observation in the Nature Journal.",
        "check": lambda missions, journal, streak, mins: len(journal) >= 1
    },
    {
        "id": "photographer_scribe",
        "name": "Visual Chronicler",
        "icon": "🖼️",
        "description": "Save a nature journal entry with a field photo.",
        "check": lambda missions, journal, streak, mins: any(bool(j.get("photo_path")) for j in journal)
    },
    {
        "id": "level_3",
        "name": "Canopy Pioneer",
        "icon": "🌲",
        "description": "Reach Level 3 (Canopy Explorer).",
        "check": lambda missions, journal, streak, mins: calculate_level(sum(m.get("xp_earned", 0) for m in missions))[0] >= 3
    }
]

def get_badges_status(completed_missions: List[Dict[str, Any]], journal_entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Evaluates earned badges against actual saved missions and journal data."""
    streak = calculate_streak(completed_missions)
    total_mins = sum(
        int(m.get("duration", "30").split()[0])
        for m in completed_missions
        if m.get("duration", "30").split()[0].isdigit()
    )
    results = []
    for b in BADGES:
        unlocked = b["check"](completed_missions, journal_entries, streak, total_mins)
        results.append({
            "id": b["id"],
            "name": b["name"],
            "icon": b["icon"],
            "description": b["description"],
            "unlocked": unlocked
        })
    return results

# ---------------------------------------------------------------------------
# Ollama Connection & Inference Logic
# ---------------------------------------------------------------------------

@st.cache_data(ttl=10, show_spinner=False)
def check_ollama_service(host_url: str, target_model: str) -> Tuple[bool, bool, List[str], str]:
    """
    Checks if Ollama daemon is reachable and whether the target model is installed.
    Verifies endpoint http://<host>/api/tags.
    Returns: (is_online, has_model, list_of_models, message)
    """
    tags_url = f"{host_url.rstrip('/')}/api/tags"
    try:
        response = requests.get(tags_url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            models = [m.get("name", "") for m in data.get("models", []) if m.get("name")]
            target_clean = target_model.strip().lower()
            
            # Match exact tag or normalized tag (e.g., qwen2.5:0.5b vs qwen2.5:0.5b:latest)
            has_model = False
            for m in models:
                m_clean = m.lower()
                if (
                    m_clean == target_clean
                    or m_clean == f"{target_clean}:latest"
                    or (target_clean.endswith(":latest") and m_clean == target_clean[:-7])
                    or (":" in target_clean and m_clean == target_clean)
                ):
                    has_model = True
                    break
            
            if has_model:
                msg = f"Connected to Ollama at {host_url}. Model '{target_model}' is installed and ready."
            else:
                installed_str = ", ".join(models) if models else "none"
                msg = f"Connected to Ollama at {host_url}, but model '{target_model}' was not found. Installed: [{installed_str}]."
                
            return True, has_model, models, msg
        return False, False, [], f"Ollama returned HTTP status {response.status_code} at {tags_url}."
    except requests.exceptions.ConnectionError:
        return False, False, [], f"Could not connect to Ollama daemon at {tags_url}. Ensure Ollama is running."
    except requests.exceptions.Timeout:
        return False, False, [], f"Connection to Ollama at {tags_url} timed out."
    except Exception as exc:
        return False, False, [], f"Connection error: {str(exc)}"


def validate_and_sanitize_mission(
    data: Dict[str, Any],
    activity: str,
    duration: str,
    difficulty: str,
    environment_type: str,
    mission_goal: Optional[str],
    source: str
) -> Dict[str, Any]:
    """Validates and enforces the required schema for outdoor missions."""
    title = str(data.get("title") or f"Outdoor Quest: {activity.title()}").strip()
    codename = str(data.get("codename") or f"Operation {activity.title()}").strip()
    objective = str(
        data.get("objective") or f"Step outside into {environment_type} for an engaging {activity} session."
    ).strip()
    why_outdoors = str(
        data.get("why_outdoors") or data.get("story") or 
        "Stepping outdoors relieves cognitive screen fatigue, grounds your senses, and restores mental focus."
    ).strip()

    # Validate 3-5 actionable steps
    raw_steps = data.get("steps")
    steps: List[str] = []
    if isinstance(raw_steps, list):
        steps = [str(s).strip() for s in raw_steps if str(s).strip()]
    if len(steps) < 3:
        fallback_steps = [
            f"Step outside to {environment_type} and silence non-essential notifications for the first 5 minutes.",
            f"Actively observe 3 distinct natural textures, leaf patterns, or wildlife sounds around you.",
            "Pause for 2 full minutes, take deep diaphragmatic breaths, and reflect on the open sky."
        ]
        for fs in fallback_steps:
            if fs not in steps and len(steps) < 3:
                steps.append(fs)
    elif len(steps) > 5:
        steps = steps[:5]

    # Validate items
    raw_items = data.get("items")
    items = [str(i).strip() for i in raw_items if str(i).strip()] if isinstance(raw_items, list) else []
    if not items:
        items = ["Water bottle", "Comfortable outdoor shoes", "Notepad or phone for notes"]

    # Validate safety tips
    raw_tips = data.get("safety_tips")
    safety_tips = [str(t).strip() for t in raw_tips if str(t).strip()] if isinstance(raw_tips, list) else []
    if not safety_tips:
        safety_tips = ["Stay aware of your surroundings and weather", "Respect local wildlife and practice Leave No Trace"]

    unique_seed = f"{title}_{activity}_{duration}_{datetime.datetime.now().isoformat()}"
    mission_id = f"quest_{hashlib.md5(unique_seed.encode()).hexdigest()[:10]}"

    return {
        "id": mission_id,
        "title": title,
        "codename": codename,
        "objective": objective,
        "why_outdoors": why_outdoors,
        "story": why_outdoors,
        "activity": activity,
        "duration": duration,
        "difficulty": difficulty,
        "environment": environment_type,
        "mission_goal": mission_goal or "Mindful Wind-Down & Stress Relief",
        "steps": steps,
        "items": items,
        "safety_tips": safety_tips,
        "source": source,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def generate_mission_with_ollama(
    host_url: str,
    model_name: str,
    activity: str,
    duration: str,
    difficulty: str,
    environment_type: str,
    mission_goal: Optional[str] = None,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Calls Ollama /api/generate endpoint to create a structured outdoor mission using the target model.
    Returns: (mission_dict, error_message)
    """
    endpoint = f"{host_url.rstrip('/')}/api/generate"

    system_instruction = (
        "You are NatureQuest-AI, an enthusiastic and inspiring outdoor guide for students participating in "
        "the Touch Grass challenge. Your mission is to provide an engaging, clear, and actionable outdoor adventure. "
        "You MUST respond ONLY with a single valid, raw JSON object matching the requested schema without markdown backticks or commentary."
    )

    goal_str = f"- Student Focus / Goal: {mission_goal}\n" if mission_goal else ""
    prompt = f"""Generate a personalized outdoor mission for a student with these parameters:
- Activity: {activity}
- Target Duration: {duration}
- Difficulty Level: {difficulty}
- Environment: {environment_type}
{goal_str}
Return ONLY a single valid JSON object following this EXACT schema:
{{
  "title": "Inspiring and catchy mission title",
  "codename": "Short cool codename e.g. Operation Forest Whisper",
  "objective": "A concise 1-2 sentence core outdoor objective for this quest.",
  "why_outdoors": "A 2-3 sentence motivating explanation of why this specific outdoor activity relieves screen fatigue and connects the student to nature.",
  "steps": [
    "Step 1: Specific actionable preparation or outdoor starting action",
    "Step 2: Core exploration or observation activity",
    "Step 3: Mindful or discovery task",
    "Step 4: Concluding grounding step"
  ],
  "items": [
    "Item 1",
    "Item 2",
    "Item 3"
  ],
  "safety_tips": [
    "Safety or environmental stewardship tip 1",
    "Safety or environmental stewardship tip 2"
  ]
}}"""

    payload = {
        "model": model_name,
        "prompt": prompt,
        "system": system_instruction,
        "format": "json",
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
        },
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=DEFAULT_TIMEOUT)
        if response.status_code != 200:
            err_msg = f"HTTP {response.status_code}"
            try:
                err_data = response.json()
                if "error" in err_data:
                    err_msg += f": {err_data['error']}"
            except Exception:
                err_msg += f": {response.text[:120]}"
            return None, f"Ollama error ({err_msg})"

        result = response.json()
        raw_text = result.get("response", "").strip()
        if not raw_text:
            return None, "Ollama returned an empty response."

        # Clean markdown code blocks if the model wrapped output in ```json
        clean_text = raw_text
        if "```json" in clean_text:
            clean_text = clean_text.split("```json")[1].split("```")[0].strip()
        elif "```" in clean_text:
            clean_text = clean_text.split("```")[1].split("```")[0].strip()

        data = json.loads(clean_text)
        mission = validate_and_sanitize_mission(
            data=data,
            activity=activity,
            duration=duration,
            difficulty=difficulty,
            environment_type=environment_type,
            mission_goal=mission_goal,
            source=f"Ollama Local AI ({model_name})"
        )
        return mission, None

    except requests.exceptions.Timeout:
        return None, f"Request to Ollama timed out after {DEFAULT_TIMEOUT}s."
    except requests.exceptions.ConnectionError:
        return None, f"Could not connect to Ollama at {endpoint}."
    except json.JSONDecodeError as jde:
        return None, f"Could not parse JSON response from model ({str(jde)})."
    except Exception as exc:
        return None, f"Unexpected error during generation: {str(exc)}"

# ---------------------------------------------------------------------------
# Curated High-Quality Fallback Missions Bank
# ---------------------------------------------------------------------------

FALLBACK_MISSIONS_BANK = {
    "walking": [
        {
            "title": "The Canopy & Moss Trail Audit",
            "codename": "Operation Greenwood Recon",
            "objective": "Identify 3 distinct tree leaf varieties and locate a living moss or lichen patch to recalibrate your senses.",
            "why_outdoors": "Walking away from digital notifications and calibrating your vision to natural green foliage breaks the continuous cycle of cognitive eye and mental fatigue.",
            "steps": [
                "Step 1: Step outside and walk at a calm, deliberate pace without headphones for the first 5 minutes.",
                "Step 2: Find 3 different varieties of tree leaves and gently examine their underside vein patterns.",
                "Step 3: Locate a patch of moss or lichen on a tree trunk or stone wall; observe how it anchors itself.",
                "Step 4: Stand motionless for 2 full minutes, breathe deeply through your nose, and feel the outdoor breeze."
            ],
            "items": ["Comfortable walking shoes", "Reusable water bottle", "Notebook or phone for quick notes"],
            "safety_tips": ["Stay on designated pedestrian paths", "Watch your step on damp roots or loose soil", "Practice Leave No Trace"]
        },
        {
            "title": "Perimeter Stride & Sensory Reset",
            "codename": "Operation Solitude Sprint",
            "objective": "Complete a brisk outdoor walking circuit to stimulate blood circulation and count 10 natural shades of earthy color.",
            "why_outdoors": "Brisk aerobic movement in outdoor air clears mental brain fog from prolonged desk sessions and stimulates cognitive renewal.",
            "steps": [
                "Step 1: Begin with a 5-minute warm-up stride around your campus green or neighborhood block.",
                "Step 2: Actively spot and count 10 distinct shades of green or brown in the vegetation along your route.",
                "Step 3: Find a clean grassy clearing, pause, and stand grounded on the grass for 3 minutes.",
                "Step 4: Briskly walk back taking rhythmic diaphragmatic breaths while looking at the distant horizon."
            ],
            "items": ["Walking shoes", "Weather-appropriate jacket", "Water bottle"],
            "safety_tips": ["Be mindful of pedestrian crossings and vehicular traffic", "Wear sun protection if outdoors in peak daylight", "Stay well hydrated"]
        }
    ],
    "birdwatching": [
        {
            "title": "Avian Songline & Perch Discovery",
            "codename": "Operation Skywatcher",
            "objective": "Isolate distinct bird vocalizations and track 2 wild birds foraging or perching in campus trees.",
            "why_outdoors": "Tuning into wildlife calls shifts brain activity from high-stress task focus to diffuse restorative attention, lowering cortisol levels.",
            "steps": [
                "Step 1: Find a quiet stationary vantage point near tree canopies with good sky visibility.",
                "Step 2: Close your eyes for 3 minutes and count how many distinct bird calls you can hear.",
                "Step 3: Spot at least two wild birds foraging on the ground or perching on upper branches; observe their head movements.",
                "Step 4: Note their silhouette, beak shape, and feather color patterns before returning indoors."
            ],
            "items": ["Field notepad and pencil", "Smartphone camera (optional)", "Muted clothing"],
            "safety_tips": ["Never disturb nesting areas or corner wild birds", "Do not feed processed food (bread, chips) to wildlife", "Watch overhead branches for loose twigs"]
        },
        {
            "title": "The High-Flyer Silhouette Survey",
            "codename": "Operation Wing & Wind",
            "objective": "Track thermal soaring patterns and flight silhouettes of birds gliding over open campus airspace.",
            "why_outdoors": "Looking up into expansive open skies reverses screen-induced myopia and delivers an immediate sense of scale and freedom.",
            "steps": [
                "Step 1: Head to an open courtyard, lakeside, or elevated campus clearing.",
                "Step 2: Track a soaring bird continuously across the sky until it leaves your field of vision.",
                "Step 3: Record whether the bird flaps continuously or rides rising thermal air currents.",
                "Step 4: Notice what species share the same airspace or tree branch without competition."
            ],
            "items": ["Field notebook", "Sun protection / sunglasses", "Water bottle"],
            "safety_tips": ["Never stare directly into midday sun", "Maintain respectful distance from wildlife", "Stay on marked walking trails"]
        }
    ],
    "gardening": [
        {
            "title": "Soil Moisture & Plant Health Doctor",
            "codename": "Operation Root Guard",
            "objective": "Inspect topsoil moisture and evaluate leaf health on 5 plants in a garden bed or potted collection.",
            "why_outdoors": "Touching real soil exposes the microbiome to beneficial earth microbes that naturally foster emotional grounding and stress resilience.",
            "steps": [
                "Step 1: Inspect the topsoil around a garden bed or potted plants; test dampness with your finger 2 inches deep.",
                "Step 2: Gently examine the undersides of 5 leaves for beneficial insects, aphids, or mildew.",
                "Step 3: Carefully remove dry or yellowed dead leaves to redirect plant energy toward fresh growth.",
                "Step 4: Water the root base thoroughly without splashing foliage, admiring the fresh petrichor scent."
            ],
            "items": ["Gardening gloves", "Small trowel or pruning shears", "Watering can"],
            "safety_tips": ["Wash hands thoroughly after handling compost or soil", "Wear gloves to avoid thorns or insect stings", "Lift heavy pots with your knees"]
        },
        {
            "title": "The Biodiversity Bed Stewardship",
            "codename": "Operation Bloom Keeper",
            "objective": "Aerate compacted topsoil and observe pollinator insect visits to open flowers.",
            "why_outdoors": "Caring for living flora cultivates patience and breaks the instant-gratification loop created by social media feeds.",
            "steps": [
                "Step 1: Identify any invasive weeds competing with budding flowers and gently extract them by root.",
                "Step 2: Loosen compacted topsoil with a hand cultivator to allow aeration and water penetration.",
                "Step 3: Spread a thin layer of dry mulch or leaves around stems to retain organic moisture.",
                "Step 4: Spend 2 quiet minutes watching pollinator visits (bees, butterflies, hoverflies) to open blossoms."
            ],
            "items": ["Gardener gloves", "Hand trowel or fork", "Mulch or dry leaves"],
            "safety_tips": ["Give pollinating insects space to work peacefully", "Wear a brimmed hat in direct sunlight", "Keep gardening tools pointed downward"]
        }
    ],
    "nature photography": [
        {
            "title": "Macro Textures & Micro Worlds",
            "codename": "Operation Golden Focal",
            "objective": "Capture 3 extreme macro perspectives of fractal leaf veins, tree bark textures, and water droplets.",
            "why_outdoors": "Photographing micro geometries trains deliberate observational acuity and shifts attention away from internal worries toward natural marvels.",
            "steps": [
                "Step 1: Switch your smartphone camera to 1x or macro mode with focus lock.",
                "Step 2: Capture 1 close-up photo of leaf veins highlighting natural fractal geometry.",
                "Step 3: Find contrasting bark texture on an older tree and photograph it emphasizing shadow and depth.",
                "Step 4: Look for dew droplets on grass blades and capture their optical reflection in sunlight."
            ],
            "items": ["Smartphone or camera with macro capability", "Lens cleaning microfiber cloth", "Comfortable clothes for crouching"],
            "safety_tips": ["Do not trample fragile understory flora while composing shots", "Watch out for thorns and poison ivy", "Secure your device firmly against drops"]
        },
        {
            "title": "Natural Light & Geometric Shadows",
            "codename": "Operation Shutter Grove",
            "objective": "Document natural sunlight filtering through leaves and architectural branches into geometric shadow patterns.",
            "why_outdoors": "Searching for natural light patterns cultivates mindfulness and creates visual records of your outdoor mental recharge.",
            "steps": [
                "Step 1: Identify a spot where sunlight cuts through tree branches creating dappled light patches.",
                "Step 2: Frame a subject (leaf, stone, or flower) illuminated by a single sunbeam.",
                "Step 3: Capture a composition using natural tree boughs or arching grasses to frame your horizon.",
                "Step 4: Take a low-angle shot looking directly up a tree trunk toward the sky canopy."
            ],
            "items": ["Camera or smartphone", "Power bank (optional)", "Walking footwear"],
            "safety_tips": ["Never look directly through a high-zoom lens at the midday sun", "Stay mindful of foot placement on uneven terrain", "Stay on designated paths"]
        }
    ]
}


def get_fallback_mission(
    activity: str,
    duration: str,
    difficulty: str,
    environment_type: str,
    mission_goal: Optional[str] = None
) -> Dict[str, Any]:
    """Retrieves and formats a rich, curated mission from the offline fallback bank."""
    activity_key = activity.lower().strip()
    missions = FALLBACK_MISSIONS_BANK.get(activity_key, FALLBACK_MISSIONS_BANK["walking"])
    chosen = random.choice(missions)
    
    unique_seed = f"{chosen['title']}_{activity}_{duration}_{datetime.datetime.now().isoformat()}"
    mission_id = f"fallback_{hashlib.md5(unique_seed.encode()).hexdigest()[:10]}"

    return {
        "id": mission_id,
        "title": chosen["title"],
        "codename": chosen["codename"],
        "objective": chosen["objective"],
        "why_outdoors": chosen["why_outdoors"],
        "story": chosen["why_outdoors"],
        "activity": activity,
        "duration": duration,
        "difficulty": difficulty,
        "environment": environment_type,
        "mission_goal": mission_goal or "Mindful Wind-Down & Stress Relief",
        "steps": chosen["steps"][:5],
        "items": chosen["items"],
        "safety_tips": chosen["safety_tips"],
        "source": "Curated Offline Fallback Mode",
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

# ---------------------------------------------------------------------------
# Sidebar: Setup, System Status & Gamification Profile
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("### 🌲 NatureQuest Engine")
    st.caption("Hacktoberfest 2026 Touch Grass Challenge")
    
    st.markdown("---")
    st.markdown("#### ⚡ AI Backend Status")
    
    # Allow user to customize host/model if needed
    ollama_host = st.text_input("Ollama Host", value=DEFAULT_OLLAMA_HOST, help="Default is http://localhost:11434")
    model_name = st.text_input("Target Model", value=DEFAULT_MODEL, help="Model: qwen2.5:0.5b")

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        if st.button("🔄 Check", help="Force refresh Ollama connection status"):
            st.cache_data.clear()
            st.rerun()

    is_online, has_model, available_models, status_msg = check_ollama_service(ollama_host, model_name)

    if is_online and has_model:
        st.success(f"🟢 **Ollama Connected**\n- Model `{model_name}` ready\n- Endpoint: `{ollama_host}/api/tags`")
        if available_models:
            st.caption(f"Detected: {', '.join(available_models)}")
        backend_mode = "ollama"
    elif is_online and not has_model:
        st.warning(f"🟡 **Ollama Online, Model Missing**\n`{model_name}` not found in Ollama.\nInstalled: {', '.join(available_models) if available_models else 'None'}")
        st.info(f"Run in terminal:\n```bash\nollama pull {model_name}\n```")
        backend_mode = "fallback"
    else:
        st.error(f"⚪ **Ollama Offline**\n{status_msg}")
        st.caption("Running in **Curated Fallback Mode**. Handcrafted missions remain fully accessible.")
        st.info("To start Ollama, run in terminal:\n```bash\nollama serve\n# or\nollama run qwen2.5:0.5b\n```")
        backend_mode = "fallback"

    # Gamification Mini-Card
    st.markdown("---")
    st.markdown("#### 🏆 Explorer Rank & XP")
    completed_list = st.session_state.completed_missions
    total_xp = sum(m.get("xp_earned", 0) for m in completed_list)
    lvl_num, lvl_title, _, next_xp, lvl_progress = calculate_level(total_xp)
    active_streak = calculate_streak(completed_list)

    st.markdown(
        f"""
        <div style="background-color: #f7faf8; border: 1px solid #d8e2dc; border-radius: 10px; padding: 0.9rem; margin-bottom: 0.8rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="badge-pill badge-level" style="margin: 0;">Lvl {lvl_num}: {lvl_title}</span>
                <span class="badge-pill badge-streak" style="margin: 0;">🔥 {active_streak}d Streak</span>
            </div>
            <div style="margin-top: 0.6rem; font-size: 0.88rem; color: #1b3322; font-weight: 600;">
                XP: {total_xp} / {next_xp}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.progress(lvl_progress)

    st.markdown("---")
    st.markdown("#### 📊 Student Totals")
    completed_count = len(completed_list)
    st.metric("Missions Completed", completed_count)
    if completed_count > 0:
        total_minutes = sum(
            int(m.get("duration", "30").split()[0]) 
            for m in completed_list 
            if m.get("duration", "30").split()[0].isdigit()
        )
        st.metric("Total Outdoor Air", f"{total_minutes} mins")

    st.markdown("---")
    st.markdown("#### 💡 Quick Setup Guide")
    with st.expander("How to enable local AI", expanded=False):
        st.markdown(
            f"""
            1. **Install Ollama** from [ollama.com](https://ollama.com).
            2. Open PowerShell or Terminal.
            3. Download and test the model:
               ```bash
               ollama run {DEFAULT_MODEL}
               ```
            4. Click **Check** above to refresh connection!
            """
        )

# ---------------------------------------------------------------------------
# Main Application Content
# ---------------------------------------------------------------------------

# Top Hero Section
st.markdown(
    """
    <div class="hero-banner">
        <span class="hero-badge">🌱 Hacktoberfest 2026 Touch Grass Challenge</span>
        <h1>NatureQuest-AI</h1>
        <p>
            Break free from screen fatigue. Generate actionable, personalized outdoor missions 
            tailored to your schedule, location, and curiosity. Step outside, touch grass, and recharge.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Tab Navigation
tab_mission, tab_journal, tab_progress, tab_offline, tab_about = st.tabs([
    "🎯 New Outdoor Mission",
    "📝 Nature Journal",
    "📊 Progress & Badges",
    "💾 Saved & Offline Quests",
    "📖 About Challenge"
])

# ---------------------------------------------------------------------------
# Tab 1: New Outdoor Mission
# ---------------------------------------------------------------------------

with tab_mission:
    col_input, col_display = st.columns([1, 1.4], gap="large")

    with col_input:
        st.markdown("### 🧭 Configure Your Quest")
        st.caption("Tell NatureQuest what kind of outdoor break fits your day.")

        # Activity Selection
        activity_options = {
            "walking": "🚶 Walking & Urban Trekking",
            "birdwatching": "🦅 Birdwatching & Wildlife Spotting",
            "gardening": "🌱 Gardening & Plant Care",
            "nature photography": "📸 Nature Photography & Macro Scouting"
        }
        
        selected_activity_key = st.selectbox(
            "Select Activity",
            options=list(activity_options.keys()),
            format_func=lambda x: activity_options[x],
            help="Choose how you want to interact with nature."
        )

        # Duration & Difficulty
        dur_col, diff_col = st.columns(2)
        with dur_col:
            selected_duration = st.select_slider(
                "Duration",
                options=["15 mins", "30 mins", "45 mins", "60 mins"],
                value="30 mins",
                help="How much time can you spend outdoors today?"
            )
        
        with diff_col:
            selected_difficulty = st.select_slider(
                "Difficulty",
                options=["Easy", "Medium", "Challenging"],
                value="Easy",
                help="Pace and complexity of observation."
            )

        # Environment Context (No GPS / precise location collected)
        environment_choice = st.selectbox(
            "Outdoor Setting",
            options=[
                "Campus Quad / College Grounds",
                "Neighborhood Park / Green Space",
                "Backyard / Balcony Garden",
                "Forest Trail / Nature Reserve",
                "Urban Street with Tree Canopy"
            ],
            help="Select the environment you have immediate access to."
        )

        # Student Mood / Goal
        mission_goal = st.radio(
            "Current Goal",
            options=[
                "Mindful Wind-Down & Stress Relief",
                "Active Exploration & Discovery",
                "Creative Focus & Scouting"
            ],
            horizontal=False
        )

        generate_clicked = st.button("🌿 Generate Outdoor Mission", use_container_width=True)

        if generate_clicked:
            with st.spinner("Scouting your outdoor quest..."):
                if backend_mode == "ollama":
                    mission, gen_error = generate_mission_with_ollama(
                        host_url=ollama_host,
                        model_name=model_name,
                        activity=selected_activity_key,
                        duration=selected_duration,
                        difficulty=selected_difficulty,
                        environment_type=environment_choice,
                        mission_goal=mission_goal,
                    )
                    if mission:
                        st.session_state.current_mission = mission
                        # Auto-stash for offline access
                        saved = [m for m in st.session_state.saved_missions if m.get("id") != mission.get("id")]
                        saved.insert(0, mission)
                        st.session_state.saved_missions = saved[:20]
                        save_saved_missions(st.session_state.saved_missions)
                        st.toast(f"Generated via Ollama ({model_name})!", icon="🌿")
                    else:
                        st.warning(f"⚠️ Ollama generation issue: {gen_error}. Switched to Curated Fallback Mode.")
                        mission = get_fallback_mission(
                            activity=selected_activity_key,
                            duration=selected_duration,
                            difficulty=selected_difficulty,
                            environment_type=environment_choice,
                            mission_goal=mission_goal,
                        )
                        st.session_state.current_mission = mission
                        saved = [m for m in st.session_state.saved_missions if m.get("id") != mission.get("id")]
                        saved.insert(0, mission)
                        st.session_state.saved_missions = saved[:20]
                        save_saved_missions(st.session_state.saved_missions)
                else:
                    mission = get_fallback_mission(
                        activity=selected_activity_key,
                        duration=selected_duration,
                        difficulty=selected_difficulty,
                        environment_type=environment_choice,
                        mission_goal=mission_goal,
                    )
                    st.session_state.current_mission = mission
                    saved = [m for m in st.session_state.saved_missions if m.get("id") != mission.get("id")]
                    saved.insert(0, mission)
                    st.session_state.saved_missions = saved[:20]
                    save_saved_missions(st.session_state.saved_missions)

    with col_display:
        st.markdown("### 📋 Active Mission Briefing")
        
        mission = st.session_state.current_mission

        if not mission:
            st.info("👈 Select your preferences on the left and click **Generate Outdoor Mission** to receive your personalized quest!")
            
            # Showcase preview cards
            st.markdown(
                """
                <div class="nature-card" style="border-style: dashed; text-align: center; color: #52796f; padding: 2.5rem 1.5rem;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🌿 ☀️ 🚶</div>
                    <h4 style="color: #2d6a4f; margin-bottom: 0.5rem;">Ready to Touch Grass?</h4>
                    <p style="font-size: 0.92rem; margin: 0;">
                        Whether you have 15 minutes between lectures or an hour to explore local parks,
                        NatureQuest-AI turns your break into a fun, rewarding field study.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            # Source Badge
            is_ai_source = "Ollama" in mission.get("source", "")
            source_badge_class = "badge-ollama" if is_ai_source else "badge-fallback"
            source_icon = "🤖" if is_ai_source else "🍂"
            
            # Potential XP calculation preview
            est_xp = calculate_mission_xp(mission.get("duration"), mission.get("difficulty"), mission.get("source"))

            # Render Mission Card Header
            st.markdown(
                f"""
                <div class="nature-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                        <div>
                            <span class="badge-pill {source_badge_class}">{source_icon} {mission.get('source')}</span>
                            <span class="badge-pill badge-green">⏱️ {mission.get('duration')}</span>
                            <span class="badge-pill badge-accent">🎯 {mission.get('difficulty')}</span>
                            <span class="badge-pill badge-xp">⭐ +{est_xp} XP</span>
                        </div>
                    </div>
                    <h2 style="color: #1b4332; margin-top: 0.6rem; margin-bottom: 0.2rem; font-weight: 700;">
                        {mission.get('title')}
                    </h2>
                    <p style="color: #40916c; font-weight: 600; font-size: 0.9rem; margin-bottom: 0.8rem;">
                        Codename: {mission.get('codename')}
                    </p>
                    <div class="objective-callout">
                        <strong>🎯 Mission Objective:</strong><br>
                        {mission.get('objective', 'Connect with the outdoors.')}
                    </div>
                    <div class="why-callout">
                        <strong>🌿 Why This Gets You Outdoors:</strong><br>
                        {mission.get('why_outdoors', mission.get('story', 'Recharge your cognitive battery.'))}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Interactive Mission Checklist
            st.markdown("#### 👟 Actionable Mission Steps")
            st.caption("Check off items on your phone or laptop as you complete them outside:")
            
            steps = mission.get("steps", [])
            for idx, step in enumerate(steps, 1):
                st.checkbox(f"{step}", key=f"step_{idx}_{mission.get('id', mission.get('codename'))}")

            # Required Gear & Safety Tips in 2 columns
            gear_col, safety_col = st.columns(2)
            
            with gear_col:
                st.markdown("#### 🎒 Items to Bring")
                items = mission.get("items", [])
                for item in items:
                    st.markdown(f"- 📦 {item}")

            with safety_col:
                st.markdown("#### 🛡️ Safety & Stewardship")
                tips = mission.get("safety_tips", [])
                for tip in tips:
                    st.markdown(f"- 🌿 {tip}")

            st.markdown("---")
            
            # Save to offline stash button
            col_stash, _ = st.columns([1, 1])
            with col_stash:
                if st.button("💾 Stash Quest for Offline Use", help="Save this mission to your offline cache"):
                    saved = [m for m in st.session_state.saved_missions if m.get("id") != mission.get("id")]
                    saved.insert(0, mission)
                    st.session_state.saved_missions = saved[:20]
                    save_saved_missions(st.session_state.saved_missions)
                    st.success("✅ Saved to your offline quests stash!")

            st.markdown("---")

            # Completion & Gamification Section
            st.markdown("#### 🏅 Field Log & Mission Completion")
            journal_note = st.text_input(
                "Quick Outdoor Reflection (Optional)",
                placeholder="e.g., Spotted a blue jay, smelled pine needles, felt 10x less stressed!",
                key=f"note_{mission.get('id', mission.get('codename'))}"
            )
            also_journal = st.checkbox("📓 Also add this observation to my Nature Journal", value=False)

            if st.button("🎉 Mark Quest as Completed & Claim XP", use_container_width=True):
                # Anti-duplicate reward check
                completed_ids = [m.get("id") for m in st.session_state.completed_missions if m.get("id")]
                completed_titles = [m.get("title") for m in st.session_state.completed_missions]

                is_already_completed = (
                    (mission.get("id") and mission.get("id") in completed_ids) or
                    (mission.get("title") in completed_titles)
                )

                if is_already_completed:
                    st.warning("⚠️ You already marked this specific quest as completed! Duplicate rewards and XP are prevented.")
                else:
                    # Calculate XP
                    awarded_xp = calculate_mission_xp(mission.get("duration"), mission.get("difficulty"), mission.get("source"))
                    completed_entry = {
                        **mission,
                        "completed_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "user_reflection": journal_note if journal_note else "Completed quest and recharged outdoors!",
                        "xp_earned": awarded_xp,
                    }
                    
                    st.session_state.completed_missions.append(completed_entry)
                    save_completed_missions(st.session_state.completed_missions)

                    # Auto-add to journal if user requested
                    if also_journal and journal_note:
                        m_title = mission.get("title", "Quest")
                        now_str = datetime.datetime.now().isoformat()
                        j_hash = hashlib.md5(f"{m_title}_{now_str}".encode()).hexdigest()[:8]
                        journal_item = {
                            "id": f"journal_{j_hash}",
                            "date": datetime.date.today().strftime("%Y-%m-%d"),
                            "title": f"Reflection: {mission.get('title')}",
                            "category": mission.get("environment", "Outdoor Setting"),
                            "notes": journal_note,
                            "photo_path": None,
                            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.session_state.journal_entries.append(journal_item)
                        save_journal_entries(st.session_state.journal_entries)

                    st.balloons()
                    st.success(f"🌟 Mission recorded! You earned **+{awarded_xp} XP**! Great job taking time to touch grass.")
                    st.rerun()

# ---------------------------------------------------------------------------
# Tab 2: Nature Journal
# ---------------------------------------------------------------------------

with tab_journal:
    st.markdown("### 📝 Nature Journal")
    st.caption("Record your mindful observations, sensory notes, and field photos. No precise GPS is collected.")

    col_j_form, col_j_view = st.columns([1, 1.3], gap="large")

    with col_j_form:
        st.markdown("#### 🌱 New Field Observation")
        with st.form("new_journal_entry_form", clear_on_submit=True):
            j_date = st.date_input("Observation Date", value=datetime.date.today())
            j_title = st.text_input("Observation Subject / Title", placeholder="e.g., Monarch Butterfly on Campus Quad")
            j_setting = st.selectbox(
                "General Outdoor Setting",
                options=[
                    "Campus Quad / College Grounds",
                    "Neighborhood Park / Green Space",
                    "Backyard / Balcony Garden",
                    "Forest Trail / Nature Reserve",
                    "Urban Street with Tree Canopy",
                    "Lakeside / Waterfront"
                ],
                help="No exact GPS location is gathered."
            )
            j_notes = st.text_area(
                "Sensory Notes & Reflections",
                placeholder="Describe what you observed: scents, textures, wildlife behavior, leaf colors, or your mental clarity...",
                height=120
            )
            j_photo = st.file_uploader("Attach Field Photo (Optional)", type=["jpg", "jpeg", "png", "webp"])

            submit_journal = st.form_submit_button("💾 Save Observation to Journal", use_container_width=True)

            if submit_journal:
                if not j_title.strip() or not j_notes.strip():
                    st.error("Please provide both a title and some observational notes.")
                else:
                    saved_photo_path = None
                    if j_photo is not None:
                        # Save photo locally
                        file_ext = os.path.splitext(j_photo.name)[1].lower() or ".jpg"
                        photo_filename = f"photo_{int(datetime.datetime.now().timestamp())}_{hashlib.md5(j_photo.name.encode()).hexdigest()[:6]}{file_ext}"
                        saved_photo_path = os.path.join(PHOTOS_DIR, photo_filename)
                        try:
                            with open(saved_photo_path, "wb") as pf:
                                pf.write(j_photo.getbuffer())
                        except Exception as e:
                            st.warning(f"Could not save photo file: {e}")
                            saved_photo_path = None

                    entry_id = f"journal_{int(datetime.datetime.now().timestamp())}"
                    new_entry = {
                        "id": entry_id,
                        "date": j_date.strftime("%Y-%m-%d"),
                        "title": j_title.strip(),
                        "category": j_setting,
                        "notes": j_notes.strip(),
                        "photo_path": saved_photo_path,
                        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state.journal_entries.insert(0, new_entry)
                    save_journal_entries(st.session_state.journal_entries)
                    st.success("🌿 Field observation saved to your Nature Journal!")
                    st.rerun()

    with col_j_view:
        st.markdown("#### 📖 Field Observations Log")
        journal_list = st.session_state.journal_entries

        if not journal_list:
            st.info("Your field journal is empty. Take a step outdoors, record what you notice, and add your first observation on the left!")
        else:
            for idx, entry in enumerate(journal_list):
                st.markdown(
                    f"""
                    <div class="journal-entry-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                            <span class="badge-pill badge-green">📅 {entry.get('date', 'Unknown')}</span>
                            <span class="badge-pill badge-accent">📍 {entry.get('category', 'Outdoors')}</span>
                        </div>
                        <h4 style="color: #1b4332; margin: 0.3rem 0; font-weight: 700;">{entry.get('title')}</h4>
                        <p style="color: #2d4a3e; font-size: 0.94rem; line-height: 1.5; margin-bottom: 0.6rem;">
                            {entry.get('notes')}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                photo_p = entry.get("photo_path")
                if photo_p and os.path.exists(photo_p):
                    st.image(photo_p, caption=f"Field Photo: {entry.get('title')}", use_container_width=True)

                col_del, _ = st.columns([1, 4])
                with col_del:
                    if st.button(f"🗑️ Delete Entry", key=f"del_j_{entry.get('id', idx)}"):
                        st.session_state.journal_entries = [e for e in st.session_state.journal_entries if e.get("id") != entry.get("id")]
                        save_journal_entries(st.session_state.journal_entries)
                        st.rerun()

# ---------------------------------------------------------------------------
# Tab 3: Progress Dashboard & Badges
# ---------------------------------------------------------------------------

with tab_progress:
    st.markdown("### 📊 Progress Dashboard & Achievements")
    st.caption("Track verified statistics, level progress, daily streak, and earned badges based on actual saved missions.")

    completed_list = st.session_state.completed_missions
    journal_list = st.session_state.journal_entries

    total_missions = len(completed_list)
    total_outdoor_minutes = sum(
        int(m.get("duration", "30").split()[0]) 
        for m in completed_list 
        if m.get("duration", "30").split()[0].isdigit()
    )
    total_xp = sum(m.get("xp_earned", 0) for m in completed_list)
    lvl_num, lvl_title, _, next_xp, lvl_progress = calculate_level(total_xp)
    active_streak = calculate_streak(completed_list)

    # Top Metric Boxes
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.markdown(
            f"""<div class="stat-box"><div class="stat-number">{total_missions}</div><div class="stat-label">Quests Completed</div></div>""",
            unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            f"""<div class="stat-box"><div class="stat-number">{total_outdoor_minutes} min</div><div class="stat-label">Outdoor Air Logged</div></div>""",
            unsafe_allow_html=True
        )
    with m3:
        st.markdown(
            f"""<div class="stat-box"><div class="stat-number">{total_xp}</div><div class="stat-label">Total XP Earned</div></div>""",
            unsafe_allow_html=True
        )
    with m4:
        st.markdown(
            f"""<div class="stat-box"><div class="stat-number">Lvl {lvl_num}</div><div class="stat-label">{lvl_title}</div></div>""",
            unsafe_allow_html=True
        )
    with m5:
        st.markdown(
            f"""<div class="stat-box"><div class="stat-number">🔥 {active_streak}d</div><div class="stat-label">Daily Streak</div></div>""",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Rank Progress Bar
    st.markdown(f"#### 🌲 Level Progression: **{lvl_title}** (Level {lvl_num})")
    st.caption(f"Progress to next rank: {total_xp} / {next_xp} XP")
    st.progress(lvl_progress)

    st.markdown("---")

    # Weekly Activity Breakdown (Calculated from actual completion timestamps)
    st.markdown("#### 📅 Weekly Activity (Past 7 Days)")
    today = datetime.date.today()
    day_labels = [(today - datetime.timedelta(days=i)).strftime("%a (%m/%d)") for i in range(6, -1, -1)]
    day_dates = [(today - datetime.timedelta(days=i)) for i in range(6, -1, -1)]
    
    weekly_mins = {d: 0 for d in day_dates}
    weekly_missions_count = 0
    for m in completed_list:
        c_at = m.get("completed_at")
        if c_at:
            try:
                c_date = datetime.datetime.strptime(c_at.split()[0], "%Y-%m-%d").date()
                if c_date in weekly_mins:
                    dur_tokens = m.get("duration", "30").split()[0]
                    mins_val = int(dur_tokens) if dur_tokens.isdigit() else 30
                    weekly_mins[c_date] += mins_val
                    weekly_missions_count += 1
            except Exception:
                pass

    chart_data = {label: weekly_mins[d] for label, d in zip(day_labels, day_dates)}
    st.bar_chart(chart_data)
    st.caption(f"Quests logged this week: **{weekly_missions_count}** | Outdoor minutes this week: **{sum(weekly_mins.values())} mins**")

    st.markdown("---")

    # Badges & Achievements Gallery
    st.markdown("#### 🏅 Badges & Achievements")
    st.caption("Earn badges by completing outdoor missions, keeping your daily streak, and writing journal entries.")
    
    badge_statuses = get_badges_status(completed_list, journal_list)
    
    badge_cols = st.columns(5)
    for idx, b in enumerate(badge_statuses):
        col = badge_cols[idx % 5]
        with col:
            status_badge = '<span class="badge-pill badge-green">✓ Unlocked</span>' if b["unlocked"] else '<span class="badge-pill badge-locked">Locked</span>'
            opacity = "1.0" if b["unlocked"] else "0.55"
            st.markdown(
                f"""
                <div class="badge-card" style="opacity: {opacity};">
                    <div style="font-size: 2.2rem; margin-bottom: 0.3rem;">{b['icon']}</div>
                    <div style="font-weight: 700; color: #1b4332; font-size: 0.95rem;">{b['name']}</div>
                    <div style="margin: 0.4rem 0;">{status_badge}</div>
                    <div style="font-size: 0.78rem; color: #52796f; line-height: 1.3;">{b['description']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # Activity Distribution & History
    st.markdown("#### 📜 Completed Quests Logbook")
    if not completed_list:
        st.info("No completed missions yet. Pick a quest in the first tab, step outside, and check off steps to start your record!")
    else:
        for idx, entry in enumerate(reversed(completed_list), 1):
            with st.expander(f"🌿 {entry.get('title')} ({entry.get('duration')}) — +{entry.get('xp_earned', 0)} XP — {entry.get('completed_at', 'Recently')}", expanded=(idx == 1)):
                st.markdown(f"**Codename:** `{entry.get('codename')}`")
                st.markdown(f"**Objective:** {entry.get('objective', 'Recharged outdoors.')}")
                st.markdown(f"**Activity:** {entry.get('activity', 'Walking').title()} | **Difficulty:** {entry.get('difficulty')} | **Setting:** {entry.get('environment')}")
                st.markdown(f"**Student Reflection:** *\"{entry.get('user_reflection', 'None')}\"*")
                st.caption(f"Generated via: {entry.get('source')}")

        col_clear1, _ = st.columns([1, 4])
        with col_clear1:
            if st.button("🗑️ Clear Logbook", help="Reset completed missions and XP"):
                st.session_state.completed_missions = []
                save_completed_missions([])
                st.rerun()

# ---------------------------------------------------------------------------
# Tab 4: Saved & Offline Quests
# ---------------------------------------------------------------------------

with tab_offline:
    st.markdown("### 💾 Saved & Offline Quests")
    st.caption("Access previously generated missions or pull from the offline bank even without an internet connection.")

    st.markdown(
        """
        <div class="tip-box">
            <strong>🌐 Offline Readiness Guide:</strong><br>
            • <strong>Local Ollama AI:</strong> Operates offline if Ollama is running locally with the <code>qwen2.5:0.5b</code> weights downloaded.<br>
            • <strong>Stashed Quests & Curated Missions:</strong> 100% offline with zero dependencies or network requirements.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📂 Your Stashed Missions")
    saved_list = st.session_state.saved_missions

    if not saved_list:
        st.info("No saved missions in your stash. When you generate a quest in the first tab, click **Stash Quest for Offline Use** to keep it accessible here!")
    else:
        for idx, s_mission in enumerate(saved_list):
            st.markdown(
                f"""
                <div class="nature-card" style="margin-bottom: 0.8rem; padding: 1.1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <div>
                            <span class="badge-pill badge-green">⏱️ {s_mission.get('duration')}</span>
                            <span class="badge-pill badge-accent">🎯 {s_mission.get('difficulty')}</span>
                            <span class="badge-pill badge-ollama">📍 {s_mission.get('activity', 'walking').title()}</span>
                        </div>
                        <span style="font-size: 0.82rem; color: #52796f;">{s_mission.get('created_at', 'Saved')}</span>
                    </div>
                    <h3 style="color: #1b4332; margin: 0.4rem 0 0.2rem 0;">{s_mission.get('title')}</h3>
                    <p style="color: #40916c; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.4rem;">
                        Codename: {s_mission.get('codename')}
                    </p>
                    <p style="color: #2d4a3e; font-size: 0.92rem; margin: 0;">
                        {s_mission.get('objective', s_mission.get('story', ''))}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            c_act, c_del, _ = st.columns([1.2, 1, 3])
            with c_act:
                if st.button("⚡ Set as Active Quest", key=f"activate_{s_mission.get('id', idx)}"):
                    st.session_state.current_mission = s_mission
                    st.success("Set as your active mission! Switch to the 'New Outdoor Mission' tab to view steps.")
            with c_del:
                if st.button("🗑️ Remove", key=f"del_saved_{s_mission.get('id', idx)}"):
                    st.session_state.saved_missions = [m for m in st.session_state.saved_missions if m.get("id") != s_mission.get("id")]
                    save_saved_missions(st.session_state.saved_missions)
                    st.rerun()

    st.markdown("---")
    st.markdown("#### 🎲 Instant Offline Mission Generator")
    st.caption("Generate a rich curated quest instantly from your local bank without contacting any AI service:")
    
    col_off_act, col_off_dur = st.columns(2)
    with col_off_act:
        off_activity = st.selectbox("Activity", ["walking", "birdwatching", "gardening", "nature photography"], key="off_act")
    with col_off_dur:
        off_duration = st.selectbox("Duration", ["15 mins", "30 mins", "45 mins", "60 mins"], key="off_dur")

    if st.button("🍂 Generate Instant Offline Quest"):
        off_m = get_fallback_mission(
            activity=off_activity,
            duration=off_duration,
            difficulty="Medium",
            environment_type="Neighborhood Park / Green Space"
        )
        st.session_state.current_mission = off_m
        st.session_state.saved_missions.insert(0, off_m)
        save_saved_missions(st.session_state.saved_missions[:20])
        st.success("Curated offline quest generated and loaded as your active quest!")

# ---------------------------------------------------------------------------
# Tab 5: About Challenge
# ---------------------------------------------------------------------------

with tab_about:
    st.markdown("### 🍂 Hacktoberfest 2026 Touch Grass Challenge")
    st.markdown(
        """
        **NatureQuest-AI** was built to address a growing issue among students and tech creators:
        hours of uninterrupted screen time, code marathons, and mental burnout.

        #### 🌟 Why 'Touch Grass'?
        - **Cognitive Restoration:** Studies in environmental psychology show that as little as 15 minutes of nature exposure restores attention spans and relieves mental fatigue.
        - **Local, Open-Weights AI:** Powered by **qwen2.5:0.5b** running locally through **Ollama**, ensuring complete offline privacy and ultra-fast inference without cloud API keys.
        - **Privacy by Design:** NatureQuest-AI does **not** collect precise GPS coordinates or track real-time location. Outdoor settings are broad categories selected by the user.
        - **Gamified Habit Formation:** Real XP rewards, level titles from *Sprout Scout* to *Master Naturalist*, and daily streaks help students build sustainable outdoor habits.
        - **Zero Barriers & Offline Friendly:** Curated offline fallback mode and stashed quests ensure that students on any laptop can immediately explore structured outdoor missions even without Ollama or network.
        - **Leave No Trace:** Every quest reminds participants of environmental stewardship and respectful observation of wildlife.
        """
    )
    
    st.markdown("---")
    st.caption("NatureQuest-AI | Open Source | Built for Hacktoberfest 2026 Touch Grass Challenge")
