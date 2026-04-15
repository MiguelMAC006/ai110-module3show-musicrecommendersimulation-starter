"""
Command line runner for the Music Recommender Simulation.

Runs the recommender for six user profiles:
  - Three "normal" taste profiles
  - Three adversarial / edge-case profiles designed to probe
    whether the scoring logic produces surprising results
"""

from recommender import load_songs, recommend_songs

# ---------------------------------------------------------------------------
# Standard taste profiles
# ---------------------------------------------------------------------------

HIGH_ENERGY_POP = {
    "name":         "High-Energy Pop",
    "genre":        "pop",
    "mood":         "happy",
    "energy":       0.92,   # club/gym-level intensity
    "valence":      0.88,   # very bright and positive
    "acousticness": 0.05,   # fully electronic / produced
    "tempo_bpm":    130.0,  # driving dance tempo
    "danceability": 0.90,   # made for the dance floor
}

CHILL_LOFI = {
    "name":         "Chill Lofi",
    "genre":        "lofi",
    "mood":         "chill",
    "energy":       0.35,   # very calm, background-music level
    "valence":      0.58,   # quietly pleasant, not ecstatic
    "acousticness": 0.80,   # warm, organic textures
    "tempo_bpm":    76.0,   # slow and relaxed
    "danceability": 0.58,   # gentle head-nod groove
}

DEEP_INTENSE_ROCK = {
    "name":         "Deep Intense Rock",
    "genre":        "rock",
    "mood":         "intense",
    "energy":       0.93,   # raw, aggressive power
    "valence":      0.38,   # dark undertones
    "acousticness": 0.07,   # fully amplified / distorted
    "tempo_bpm":    155.0,  # fast, driving rhythm
    "danceability": 0.62,   # headbang-capable but not club-oriented
}

# ---------------------------------------------------------------------------
# Adversarial / edge-case profiles
# (designed to expose surprising or contradictory scoring outcomes)
# ---------------------------------------------------------------------------

# Profile A: conflicting energy vs. mood
# energy=0.9 screams "hype" but mood="sad" screams "slow ballad".
# The scorer weights energy (+3.0 pts) more than mood (+1.0 pt), so
# high-energy songs should still win — is that the desired behaviour?
CONFLICTING_ENERGY_SAD = {
    "name":         "Conflicting — High Energy + Sad Mood",
    "genre":        "folk",
    "mood":         "sad",
    "energy":       0.90,   # high-energy contradicts the sad mood
    "valence":      0.10,   # very dark / negative
    "acousticness": 0.85,   # acoustic folk texture
    "tempo_bpm":    100.0,  # moderate tempo
    "danceability": 0.30,   # not danceable
}

# Profile B: genre-feature mismatch
# Asks for metal but with maximum acousticness (0.95).
# Metal songs in the dataset have acousticness ~0.08, so the genre
# bonus (+1.0) will fight against the acousticness penalty. Does metal
# still win, or do acoustic folk/classical songs outscore it?
METAL_BUT_ACOUSTIC = {
    "name":         "Conflicting — Metal Genre + Max Acousticness",
    "genre":        "metal",
    "mood":         "aggressive",
    "energy":       0.97,   # metal-level intensity
    "valence":      0.25,   # dark
    "acousticness": 0.95,   # contradicts typical metal production
    "tempo_bpm":    170.0,  # blast-beat territory
    "danceability": 0.50,
}

# Profile C: all-extremes stress test
# Every numeric parameter pushed to its absolute maximum.
# No song in the dataset will match all of these perfectly; the
# test reveals which weights dominate when every axis is saturated.
ALL_EXTREMES = {
    "name":         "Edge Case — All Parameters at Maximum",
    "genre":        "edm",
    "mood":         "euphoric",
    "energy":       1.00,
    "valence":      1.00,
    "acousticness": 0.00,
    "tempo_bpm":    200.0,  # far above any song in the dataset (max ~168)
    "danceability": 1.00,
}

# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

PROFILES = [
    HIGH_ENERGY_POP,
    CHILL_LOFI,
    DEEP_INTENSE_ROCK,
    CONFLICTING_ENERGY_SAD,
    METAL_BUT_ACOUSTIC,
    ALL_EXTREMES,
]


def print_recommendations(user_prefs: dict, recommendations: list) -> None:
    max_score = 7.75
    sep = "-" * 56

    print("\n" + "=" * 56)
    print(f"  PROFILE: {user_prefs['name']}")
    print("=" * 56)

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


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile in PROFILES:
        # recommend_songs doesn't use the "name" key — pass the dict as-is
        recommendations = recommend_songs(profile, songs, k=5)
        print_recommendations(profile, recommendations)


if __name__ == "__main__":
    main()
