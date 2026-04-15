import csv
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
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

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
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []

    with open(csv_path, mode="r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            }
            songs.append(song)

    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores one song against user preferences and returns:
    (score, reasons)
    """
    score = 0.0
    reasons: List[str] = []

    if song.get("genre") == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song.get("mood") == user_prefs.get("mood"):
        score += 1.0
        reasons.append("mood match (+1.0)")

    if "energy" in user_prefs:
        energy_similarity = max(0.0, 1.0 - abs(song["energy"] - float(user_prefs["energy"])))
        energy_points = 1.5 * energy_similarity
        score += energy_points
        reasons.append(f"energy closeness (+{energy_points:.2f})")

    if "tempo_bpm" in user_prefs:
        tempo_similarity = max(0.0, 1.0 - abs(song["tempo_bpm"] - float(user_prefs["tempo_bpm"])) / 100.0)
        tempo_points = 0.75 * tempo_similarity
        score += tempo_points
        reasons.append(f"tempo closeness (+{tempo_points:.2f})")

    if "valence" in user_prefs:
        valence_similarity = max(0.0, 1.0 - abs(song["valence"] - float(user_prefs["valence"])))
        valence_points = 0.5 * valence_similarity
        score += valence_points
        reasons.append(f"valence closeness (+{valence_points:.2f})")

    if "danceability" in user_prefs:
        dance_similarity = max(0.0, 1.0 - abs(song["danceability"] - float(user_prefs["danceability"])))
        dance_points = 0.5 * dance_similarity
        score += dance_points
        reasons.append(f"danceability closeness (+{dance_points:.2f})")

    if "likes_acoustic" in user_prefs:
        likes_acoustic = bool(user_prefs["likes_acoustic"])
        song_is_acoustic = song["acousticness"] >= 0.5
        if likes_acoustic == song_is_acoustic:
            score += 0.5
            reasons.append("acoustic preference match (+0.5)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored: List[Tuple[Dict, float, str]] = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "general similarity"
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
