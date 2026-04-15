from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str        # e.g. "lofi", "rock", "pop"
    favorite_mood: str         # e.g. "chill", "intense", "happy"
    target_energy: float       # 0.0 (very calm) to 1.0 (very intense)
    target_valence: float      # 0.0 (dark/sad) to 1.0 (bright/positive)
    target_acousticness: float # 0.0 (electronic) to 1.0 (fully acoustic)
    target_tempo_bpm: float    # preferred beats per minute, e.g. 80.0
    target_danceability: float # 0.0 (not danceable) to 1.0 (very danceable)

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Parse songs.csv and return a list of dicts with numeric fields cast to float/int."""
    import csv

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":            int(row["id"]),
                "title":         row["title"],
                "artist":        row["artist"],
                "genre":         row["genre"],
                "mood":          row["mood"],
                "energy":        float(row["energy"]),
                "tempo_bpm":     float(row["tempo_bpm"]),
                "valence":       float(row["valence"]),
                "danceability":  float(row["danceability"]),
                "acousticness":  float(row["acousticness"]),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Return (total_score, reasons) for one song using the weighted recipe (max 7.25 pts)."""
    score = 0.0
    reasons: List[str] = []

    # --- Categorical: genre (binary, +2.0) ---
    if song["genre"] == user_prefs.get("genre", ""):
        score += 2.0
        reasons.append(f"genre match ({song['genre']}) +2.0")

    # --- Categorical: mood (binary, +1.0) ---
    if song["mood"] == user_prefs.get("mood", ""):
        score += 1.0
        reasons.append(f"mood match ({song['mood']}) +1.0")

    # --- Numeric: energy (up to +1.5) ---
    if "energy" in user_prefs:
        pts = 1.5 * (1 - abs(song["energy"] - user_prefs["energy"]))
        score += pts
        reasons.append(f"energy similarity +{pts:.2f}")

    # --- Numeric: valence (up to +1.0) ---
    if "valence" in user_prefs:
        pts = 1.0 * (1 - abs(song["valence"] - user_prefs["valence"]))
        score += pts
        reasons.append(f"valence similarity +{pts:.2f}")

    # --- Numeric: danceability (up to +0.75) ---
    if "danceability" in user_prefs:
        pts = 0.75 * (1 - abs(song["danceability"] - user_prefs["danceability"]))
        score += pts
        reasons.append(f"danceability similarity +{pts:.2f}")

    # --- Numeric: acousticness (up to +0.5) ---
    if "acousticness" in user_prefs:
        pts = 0.5 * (1 - abs(song["acousticness"] - user_prefs["acousticness"]))
        score += pts
        reasons.append(f"acousticness similarity +{pts:.2f}")

    # --- Numeric: tempo (up to +0.5, normalized over 120 BPM window) ---
    if "tempo_bpm" in user_prefs:
        raw_diff = abs(song["tempo_bpm"] - user_prefs["tempo_bpm"]) / 120
        pts = max(0.0, 0.5 * (1 - raw_diff))
        score += pts
        reasons.append(f"tempo similarity +{pts:.2f}")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by descending score, and return the top-k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        total_score, reasons = score_song(user_prefs, song)
        explanation = " · ".join(reasons)
        scored.append((song, total_score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
