# Model Card: VibeMatch 1.0

---

## 1. Model Name

**AuraPlay 1.0**

It matches songs to a listener's vibe — their preferred genre, mood, and audio feel — and returns the five closest options from a small catalog.

---

## 2. Goal / Task

The system takes a user's music preferences and suggests five songs they would probably enjoy.

It does not predict what songs a person will like based on history. It has no memory of past listens or skips. It only looks at what the user says they want right now and finds the closest matches in the catalog.

This is called **content-based filtering**: we compare song features directly to user preferences, one song at a time.

---

## 3. Data Used

The catalog has **18 songs** stored in a CSV file.

Each song has these features:
- **Genre** — a style label like lofi, pop, rock, or jazz
- **Mood** — an emotional label like happy, chill, intense, or sad
- **Energy** — a number from 0 to 1 (0 = very calm, 1 = very loud and intense)
- **Valence** — a number from 0 to 1 (0 = dark/sad sounding, 1 = bright/positive)
- **Danceability** — how easy it is to dance to (0 to 1)
- **Acousticness** — how organic or electronic it sounds (0 = electronic, 1 = acoustic)
- **Tempo** — beats per minute, like how fast the song moves

**Limits of this dataset:**
- 18 songs is very small. Real streaming services have millions.
- 13 out of 15 genres have only one song each. A jazz fan's top result is always the same song.
- No songs exist with energy between 0.45 and 0.65. Moderate-energy listeners have no close matches.
- All songs were made up for this simulation. They do not reflect real listener diversity.

---

## 4. Algorithm Summary

The system gives each song a score and returns the top five.

Here is how scoring works in plain language:

**Genre match:** If the song's genre matches the user's favorite genre, it gets 1 point. This is the biggest single bonus.

**Mood match:** If the song's mood matches, it gets 1 more point.

**Energy closeness:** The closer the song's energy is to what the user wants, the more points it earns. A perfect match is worth up to 3 points. A song far away from the target energy gets very few points here.

**Valence closeness:** Same idea — closer valence earns up to 1 point.

**Danceability closeness:** Up to 0.75 points for a good match.

**Acousticness closeness:** Up to 0.5 points.

**Tempo closeness:** Up to 0.5 points, based on how far the BPM is from the target.

The maximum possible score is **7.75 points**. Songs are ranked from highest to lowest and the top five are shown.

**One key thing to notice:** genre and mood are all-or-nothing. A song either matches the label exactly or gets zero for that category. There is no partial credit for being close — "indie pop" and "pop" are treated as completely different genres.

---

## 5. Observed Behavior / Biases

**The mood label trap.** The system picks Sunrise City (energy 0.82, labeled "happy") over Gym Hero (energy 0.93, labeled "intense") for the High-Energy Pop profile. Gym Hero is louder, faster, and more electronic — a better fit for someone who wants to work out. But the system sees the word "happy" on Sunrise City and sends it to the top. The label beats the actual audio numbers. This is a real problem: music moods are fuzzy in real life, but the system treats them like hard rules.

**The energy dead zone.** There are no songs in the catalog with energy between 0.45 and 0.65. A user who wants mid-energy background music — not sleepy, not intense — can never find a close match. Every recommendation will feel either too calm or too energetic. The system is blind to an entire range of listener taste.

**The single-song filter bubble.** Thirteen of the fifteen genres in the catalog have exactly one song. If you like jazz, your #1 result is always Coffee Shop Stories. Then the next four picks come from completely unrelated genres based on which songs happen to score well numerically. A jazz fan and a metal fan end up with almost identical bottom-four lists. The system cannot offer variety within a niche genre because there are no options.

**Storm Runner is everywhere.** The rock song Storm Runner (high energy, moderate valence) showed up in the top five for five out of six test profiles. It never matched anyone's genre except rock listeners, but its energy score pulled it into every energetic list. A small catalog amplifies this effect — there are not enough songs to push it out.

---

## 6. Evaluation Process

Six profiles were tested in total: three realistic listener types and three adversarial profiles designed to break the scoring logic.

| Profile | Genre | Mood | Energy | What it was testing |
|---|---|---|---|---|
| High-Energy Pop | pop | happy | 0.92 | Does a genre+mood match produce the right pick? |
| Chill Lofi | lofi | chill | 0.35 | Does the system work when multiple catalog entries exist? |
| Deep Intense Rock | rock | intense | 0.93 | Does a single-song genre still produce a confident top result? |
| Conflicting — High Energy + Sad | folk | sad | 0.90 | Does high energy override a sad mood label? |
| Conflicting — Metal + Max Acousticness | metal | aggressive | 0.97 | Can a genre bonus survive a completely wrong feature value? |
| All Extremes | edm | euphoric | 1.00 | What happens when every axis is maxed out? |

**What worked as expected:** Chill Lofi and Deep Intense Rock both returned the right song at the top with strong scores. These profiles had internally consistent preferences and at least one close catalog match.

**What was surprising:** The conflicting profiles showed that genre and mood labels dominate the score even when every other feature is a bad match. Iron Curtain (acousticness 0.08) ranked first for a user who said they wanted acousticness 0.95 — because the "metal" genre bonus was too strong to overcome.

A second experiment doubled the energy weight and halved the genre weight. The top picks stayed the same for most profiles, but the conflicting profiles became more honest — the gap between the best match and the second-best got smaller, showing the tension in the user's preferences rather than hiding it.

---

## 7. Intended Use and Non-Intended Use

**This system is for:**
- Learning how content-based filtering works
- Classroom exploration of scoring logic and bias
- Experimenting with how weights change recommendations

**This system is NOT for:**
- Making real music recommendations for real users
- Handling large catalogs (it was built and tested on 18 songs)
- Replacing tools like Spotify or Apple Music that use behavioral data, collaborative filtering, and millions of songs
- Making decisions about what music is "good" or what users "should" like

The catalog was made up for this simulation. It does not represent the full range of musical taste, culture, or genre. Using it as if it did would produce unfair and inaccurate results.

---

## 8. Ideas for Improvement

**1. Add partial mood matching.**
Right now "happy" and "intense" earn zero overlap even though they can describe the same song for different listeners. A simple fix would be to group moods into families (positive, dark, calm, energetic) and give partial credit for being in the same family.

**2. Add a diversity rule.**
Once a song appears in the top five, no other song from the same genre should be allowed to fill an adjacent slot unless the user explicitly requested that genre. This would prevent lofi from occupying three of five slots for lofi listeners and would help niche listeners see adjacent genres.

**3. Grow the catalog to at least 100 songs.**
Every single genre having one song means the system cannot distinguish between a light preference and a strong preference. With more songs per genre, the numeric scores would have more room to create meaningful separations.

---

## 9. Personal Reflection

**Biggest learning moment:** The mood label problem was the most surprising discovery. I expected the system to naturally favor the more energetically correct song for the High-Energy Pop profile. Instead, a single word — "happy" versus "intense" — decided the winner, even when all the audio numbers pointed the other way. It showed that a recommender is only as good as the labels in its data. If the labels are inconsistent or too simplistic, the algorithm will follow them faithfully and produce results that feel wrong to a real human.

**On using AI tools:** AI assistance helped quickly identify the structural biases — like the energy dead zone and the single-song filter bubble — by analyzing the dataset and scoring formula together. But the results still needed to be verified manually. When the agent said the new max score was 7.75, I confirmed it by adding up each weight myself. AI tools speed up the exploration, but they do not replace the need to understand what the numbers actually mean.

**What surprised me about simple algorithms:** At its core, this is just addition and subtraction. There are no neural networks, no deep learning, no complex statistics — just multiply a difference by a weight and sum everything up. Yet when the genre and mood line up, the output genuinely feels like a recommendation. Sunrise City feels right for a happy pop listener. Library Rain feels right for someone who wants chill lofi. The "intelligence" is mostly pattern matching on labels we attached ourselves. That made me realize how much of what feels smart in real apps might also be simpler than it looks on the surface.

**What I would try next:** I would add a behavioral layer — even a fake one. For example, if the same song appears in the top three for five runs in a row, the system should automatically lower its score for subsequent runs to force variety. Real recommenders call this "diversity injection." It would make the output feel less repetitive and more like something a DJ would actually play.
