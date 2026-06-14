# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

Berkeley study spots — where to work on campus and nearby, and what each place is actually like (noise, outlets, WiFi, hours, crowding). Official channels (library homepages, campus maps) list locations and hours but not the practical details students care about: which room in Doe stays quiet, which café has outlets after 9pm, or which hidden spots empty out during finals. That knowledge lives in Reddit threads, student blogs, and one-off guides — scattered, inconsistent, and hard to search in one place.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | r/berkeley — study spots thread | Reddit thread | https://www.reddit.com/r/berkeley/comments/cnr8wb/study_spots_in_berkeley/ · `documents/01_reddit_study_spots.txt` |
| 2 | life.berkeley.edu — top 5 library study spots | Student blog | https://life.berkeley.edu/top-5-library-study-spots/ · `documents/02_life_top_5_libraries.txt` |
| 3 | life.berkeley.edu — library crawl | Student blog | https://life.berkeley.edu/library-crawl/ · `documents/03_life_library_crawl.txt` |
| 4 | visit.berkeley.edu — study spots that empty at night | Campus news | https://visit.berkeley.edu/news/study-spot-suggestions-campus · `documents/04_visit_night_study_spots.txt` |
| 5 | visit.berkeley.edu — underground spots | Campus news | https://visit.berkeley.edu/news/best-underground-spots-campus · `documents/05_visit_underground_spots.txt` |
| 6 | life.berkeley.edu — hidden study spots | Student blog | https://life.berkeley.edu/hidden-study-spots · `documents/06_life_hidden_spots.txt` |
| 7 | life.berkeley.edu — Northside study spots | Student blog | https://life.berkeley.edu/northside-study-spots · `documents/07_life_northside_cafes.txt` |
| 8 | life.berkeley.edu — Elmwood study spots | Student blog | https://life.berkeley.edu/best-elmwood-study-spots/ · `documents/08_life_elmwood_cafes.txt` |
| 9 | life.berkeley.edu — campus café list | Student blog | https://life.berkeley.edu/cal-campus-cafe-list · `documents/09_life_campus_cafe_list.txt` |
| 10 | visit.berkeley.edu — café ranking (outlets/WiFi) | Campus news | https://visit.berkeley.edu/node/603 · `documents/10_visit_cafe_ranking.txt` |
| 11 | visit.berkeley.edu — best coffee shops | Campus news | https://visit.berkeley.edu/news/best-coffee-shops-berkeley · `documents/11_visit_best_coffee_shops.txt` |
| 12 | visit.berkeley.edu — coffee cartographer | Campus news | https://visit.berkeley.edu/news/cals-coveted-caffeine-contributors · `documents/12_visit_coffee_cartographer.txt` |
| 13 | life.berkeley.edu — late night in Berkeley | Student blog | https://life.berkeley.edu/late-night-in-berkeley · `documents/13_life_late_night.txt` |
| 14 | Berkeley Law — mindfulness guide to peaceful spots | Text (extracted from PDF) | https://www.law.berkeley.edu/files/Mindfulness_Initiative_Guide_to_Peaceful_Campus_Spots(1).pdf · `documents/14_law_mindfulness_guide.txt` |
| 15 | Simons Institute — restaurant recommendations | Institute page | https://simons.berkeley.edu/berkeley-restaurant-recommendations · `documents/15_simons_restaurants.txt` |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
