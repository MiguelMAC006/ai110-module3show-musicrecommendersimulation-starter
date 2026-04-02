# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

---

Real-world recommenders like Spotify and YouTube don't just find songs with the highest energy or most plays — they find songs that are closest to *what a specific user already loves*. They do this by building a profile of the user's taste (from listening history, skips, and likes) and then scoring every candidate song against that profile using a mix of behavioral signals and audio features. Our simulation prioritizes **content-based filtering**: we skip behavioral data entirely and score songs purely on how closely their audio attributes and categorical tags match a user's stated preferences. This makes the logic transparent and explainable — every recommendation can be traced back to a specific feature match — which is ideal for learning how the math behind these systems actually works.

### Song Features

Each `Song` object stores the following attributes drawn from `data/songs.csv`:

- `id` — unique identifier
- `title` — song name
- `artist` — artist name
- `genre` — categorical style label (e.g., lofi, pop, rock, ambient, jazz, synthwave, indie pop)
- `mood` — categorical emotional tone (e.g., happy, chill, intense, relaxed, focused, moody)
- `energy` — float 0–1, physical intensity of the track
- `tempo_bpm` — beats per minute, normalized for scoring
- `valence` — float 0–1, musical positiveness/brightness
- `danceability` — float 0–1, rhythmic groove strength
- `acousticness` — float 0–1, organic vs. electronic texture

### UserProfile Features

Each `UserProfile` object stores a preferred value for each scoreable feature:

- `preferred_genre` — the genre the user most wants to hear
- `preferred_mood` — the emotional tone the user is seeking
- `preferred_energy` — target energy level (float 0–1)
- `preferred_valence` — target valence (float 0–1)
- `preferred_acousticness` — target acousticness (float 0–1)
- `preferred_tempo_bpm` — target tempo (normalized before scoring)
- `preferred_danceability` — target danceability (float 0–1)

### Scoring & Ranking

The `Recommender` computes a weighted proximity score for each song:

- Categorical features (`genre`, `mood`) use exact/partial match scoring
- Numerical features use `1 - |user_preference - song_value|` to reward closeness
- Weights prioritize genre (0.30) and mood (0.25), with energy (0.20) as the top numerical signal
- Songs are ranked by descending score; the top-N are returned as recommendations

### Algorithm Recipe (Finalized)

The recommender computes a score for each song by summing these weighted components. Maximum possible score is **7.25**.

**Categorical matches (binary — full points or zero):**

| Signal | Points | Rule |
|--------|--------|------|
| Genre match | +2.00 | `song.genre == user.favorite_genre` |
| Mood match | +1.00 | `song.mood == user.favorite_mood` |

**Numeric similarity (continuous — partial credit via `1 - \|difference\|`):**

| Signal | Max Points | Formula |
|--------|-----------|---------|
| Energy | +1.50 | `1.5 × (1 - abs(song.energy - target_energy))` |
| Valence | +1.00 | `1.0 × (1 - abs(song.valence - target_valence))` |
| Danceability | +0.75 | `0.75 × (1 - abs(song.danceability - target_danceability))` |
| Acousticness | +0.50 | `0.5 × (1 - abs(song.acousticness - target_acousticness))` |
| Tempo | +0.50 | `0.5 × (1 - abs(song.tempo_bpm - target_tempo_bpm) / 120)` clamped to 0 |

Genre carries the most weight because it is the primary filter users apply consciously. Energy is the strongest continuous signal because a large energy mismatch feels jarring even when genre and mood match. Valence and danceability provide secondary texture. Acousticness and tempo are tie-breakers.

### Known Biases and Limitations

- **Genre over-prioritization:** A +2.0 genre bonus is large enough that a genre match with poor mood and energy alignment can outscore a near-perfect mood/energy match in a different genre. Users who enjoy cross-genre listening may receive a narrower list than they would prefer.
- **Exact string matching for categories:** `"indie pop" != "pop"`, so a user who likes pop will never receive a +2.0 bonus for an indie pop track even though many listeners enjoy both. The system cannot handle genre families or subgenres.
- **Mood label sparsity:** The catalog only covers 14 distinct moods across 17 songs. Several moods appear only once (e.g., "nostalgic", "euphoric", "peaceful"). A user targeting a rare mood will rarely earn the +1.0 mood bonus.
- **Small catalog ceiling:** With only 17 songs, top-K lists for K=5 include nearly a third of all available songs, which limits meaningful ranking.
- **No behavioral signal:** The system treats all users with the same stated preferences as identical. It cannot learn that a user consistently skips high-tempo recommendations even when tempo matches their stated target.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

