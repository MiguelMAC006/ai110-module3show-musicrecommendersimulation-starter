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

    # Taste profile: a focused but not extreme listener — prefers upbeat indie pop,
    # moderately energetic, positive, slightly organic sound, danceable but not club-heavy.
    user_prefs = {
        "genre":        "indie pop",
        "mood":         "happy",
        "energy":       0.75,   # lively but not gym-intense
        "valence":      0.80,   # bright and positive
        "acousticness": 0.35,   # leans slightly organic, not fully electronic
        "tempo_bpm":    118.0,  # upbeat but not frantic
        "danceability": 0.78,   # groovy, not hardcore dance
    }

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
