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

    max_score = 7.25  # theoretical maximum from the algorithm recipe
    sep = "-" * 52

    print("\n" + "=" * 52)
    print("  MUSIC RECOMMENDER — TOP RECOMMENDATIONS")
    print("=" * 52)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        bar_filled = round((score / max_score) * 20)
        bar = "#" * bar_filled + "." * (20 - bar_filled)

        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}")
        print(f"       Score: {score:.2f} / {max_score:.2f}  [{bar}]")
        print(f"       Why:")
        for reason in explanation.split(" · "):
            print(f"         • {reason}")
        print(sep)


if __name__ == "__main__":
    main()
