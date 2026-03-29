"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    # user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    # Change only this key to swap profiles quickly.
    ACTIVE_PROFILE = "high_energy_pop"  # Options: "high_energy_pop", "chill_lofi", "deep_intense_rock", "sad_but_max_energy", "genre_impossible_numeric_perfect"

    profiles = {
        "high_energy_pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.86,
            "target_tempo_bpm": 132,
            "target_valence": 0.78,
            "target_danceability": 0.84,
            "target_acousticness": 0.18,
        },
        "chill_lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.38,
            "target_tempo_bpm": 76,
            "target_valence": 0.58,
            "target_danceability": 0.60,
            "target_acousticness": 0.80,
        },
        "deep_intense_rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.89,
            "target_tempo_bpm": 148,
            "target_valence": 0.44,
            "target_danceability": 0.50,
            "target_acousticness": 0.10,
        },
        # Edge case: conflicting low valence + very high energy/tempo
        "sad_but_max_energy": {
            "favorite_genre": "lofi",
            "favorite_mood": "sad",
            "target_energy": 0.95,
            "target_tempo_bpm": 150,
            "target_valence": 0.15,
            "target_danceability": 0.85,
            "target_acousticness": 0.20,
        },
        # Edge case: genre likely absent from catalog
        "genre_impossible_numeric_perfect": {
            "favorite_genre": "classical",
            "favorite_mood": "chill",
            "target_energy": 0.38,
            "target_tempo_bpm": 76,
            "target_valence": 0.58,
            "target_danceability": 0.60,
            "target_acousticness": 0.80,
        },
    }

    user_prefs = profiles[ACTIVE_PROFILE]
    print(f"\nUsing profile: {ACTIVE_PROFILE}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
