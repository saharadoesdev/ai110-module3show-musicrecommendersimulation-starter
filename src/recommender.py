from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

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
    Converts numerical values to floats/ints for mathematical operations.
    Required by src/main.py
    
    Args:
        csv_path: Path to the songs.csv file
    
    Returns:
        List of dictionaries with song data (numeric columns as float/int)
    """
    print(f"Loading songs from {csv_path}...")
    songs = []
    
    # Define which columns should be converted to numeric types
    float_columns = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    int_columns = {"id"}
    
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Convert numeric columns
                for col in float_columns:
                    if col in row:
                        row[col] = float(row[col])
                
                for col in int_columns:
                    if col in row:
                        row[col] = int(row[col])
                
                songs.append(row)
        
        print(f"Successfully loaded {len(songs)} songs.")
        return songs
    
    except FileNotFoundError:
        print(f"Error: File not found at {csv_path}")
        return []
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using points-based algorithm.
    Returns total score (0-7) and list of scoring reasons for transparency.
    
    Scoring breakdown (sensitivity experiment):
    - Genre match: +1.0 points (binary)
    - Mood match: +1.5 points (binary)
    - Energy similarity: +2.0 × similarity (0-1)
    - Tempo similarity: +0.5 × similarity (0-1)
    - Valence similarity: +0.5 × similarity (0-1)
    - Danceability similarity: +0.4 × similarity (0-1)
    - Acousticness similarity: +0.3 × similarity (0-1)
    
    Args:
        user_prefs: Dict with target values (favorite_genre, favorite_mood, target_energy, etc.)
        song: Dict with song attributes (genre, mood, energy, tempo_bpm, etc.)
    
    Returns:
        Tuple of (total_score: float, reasons: List[str])
    """
    score = 0.0
    reasons = []
    
    # Active weights (energy-boost experiment)
    genre_weight = 1.0
    mood_weight = 1.5
    energy_weight = 2.0
    tempo_weight = 0.5
    valence_weight = 0.5
    danceability_weight = 0.4
    acousticness_weight = 0.3

    # Baseline weights (original recipe) for quick swap
    # genre_weight = 2.0
    # mood_weight = 1.5
    # energy_weight = 1.0
    # tempo_weight = 0.5
    # valence_weight = 0.5
    # danceability_weight = 0.4
    # acousticness_weight = 0.3

    # Genre match (binary)
    if song.get("genre", "").lower() == user_prefs.get("favorite_genre", "").lower():
        score += genre_weight
        reasons.append(f"Genre match (+{genre_weight:.1f})")
    
    # Mood match (binary)
    if song.get("mood", "").lower() == user_prefs.get("favorite_mood", "").lower():
        score += mood_weight
        reasons.append(f"Mood match (+{mood_weight:.1f})")
    
    # Helper function to calculate similarity for continuous features (0-1 normalized)
    def calculate_similarity(target: float, actual: float, range_val: float = 1.0) -> float:
        """Returns similarity score between 0 and 1 based on distance from target."""
        if range_val == 0:
            return 1.0 if target == actual else 0.0
        similarity = max(0.0, 1.0 - abs(target - actual) / range_val)
        return similarity
    
    # Energy similarity (range: 0-1)
    target_energy = user_prefs.get("target_energy", 0.5)
    actual_energy = float(song.get("energy", 0.5))
    energy_sim = calculate_similarity(target_energy, actual_energy, range_val=1.0)
    energy_points = energy_weight * energy_sim
    score += energy_points
    reasons.append(f"Energy similar ({energy_points:.2f})")
    
    # Tempo similarity (range: 60-170 BPM = 110)
    target_tempo = user_prefs.get("target_tempo_bpm", 100)
    actual_tempo = float(song.get("tempo_bpm", 100))
    tempo_sim = calculate_similarity(target_tempo, actual_tempo, range_val=110.0)
    tempo_points = tempo_weight * tempo_sim
    score += tempo_points
    reasons.append(f"Tempo similar ({tempo_points:.2f})")
    
    # Valence similarity (range: 0-1)
    target_valence = user_prefs.get("target_valence", 0.5)
    actual_valence = float(song.get("valence", 0.5))
    valence_sim = calculate_similarity(target_valence, actual_valence, range_val=1.0)
    valence_points = valence_weight * valence_sim
    score += valence_points
    reasons.append(f"Valence similar ({valence_points:.2f})")
    
    # Danceability similarity (range: 0-1)
    target_danceability = user_prefs.get("target_danceability", 0.5)
    actual_danceability = float(song.get("danceability", 0.5))
    danceability_sim = calculate_similarity(target_danceability, actual_danceability, range_val=1.0)
    danceability_points = danceability_weight * danceability_sim
    score += danceability_points
    reasons.append(f"Danceability similar ({danceability_points:.2f})")
    
    # Acousticness similarity (range: 0-1)
    target_acousticness = user_prefs.get("target_acousticness", 0.5)
    actual_acousticness = float(song.get("acousticness", 0.5))
    acousticness_sim = calculate_similarity(target_acousticness, actual_acousticness, range_val=1.0)
    acousticness_points = acousticness_weight * acousticness_sim
    score += acousticness_points
    reasons.append(f"Acousticness similar ({acousticness_points:.2f})")
    
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Scores all songs, ranks by score, applies diversity filtering, returns top-K.
    Required by src/main.py
    
    Args:
        user_prefs: User preference dictionary
        songs: List of song dictionaries
        k: Number of recommendations to return (default 5)
    
    Returns:
        List of (song_dict, score, explanation_str) tuples, ranked by score
    """
    # Score all songs and collect results
    scored_songs = []
    for song in songs:
        total_score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored_songs.append((song, total_score, explanation))
    
    # Sort by score in descending order
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    # Apply diversity filtering: max 1 song per artist
    seen_artists = set()
    diverse_recommendations = []
    
    for song, score, explanation in scored_songs:
        artist = song.get("artist", "Unknown")
        if artist not in seen_artists:
            diverse_recommendations.append((song, score, explanation))
            seen_artists.add(artist)
            if len(diverse_recommendations) >= k:
                break
    
    return diverse_recommendations
