# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

Berkeley study spots — where to work on campus and nearby, and what each place is actually like (noise, outlets, WiFi, hours, crowding). Official channels (library homepages, campus maps) list locations and hours but not the practical details students care about: which room in Doe stays quiet, which café has outlets after 9pm, or which hidden spots empty out during finals. That knowledge lives in Reddit threads, student blogs, and one-off guides — scattered, inconsistent, and hard to search in one place.

**Example questions this system should handle:**

- What are the top-ranked library study spots at Berkeley, and why do students prefer them?
- Which libraries stay open past midnight during the semester?
- What Northside or Elmwood cafés do students recommend for studying, and what's the vibe?
- What hidden or lesser-known study spots exist on campus (e.g., Ishi Court, Women's Faculty Club Garden)?
- Where can I study late at night when main libraries are crowded?
- What do r/berkeley users recommend when someone asks for study spots?

---

## Documents

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | r/berkeley | Crowdsourced study spot recommendations and replies | https://www.reddit.com/r/berkeley/comments/cnr8wb/study_spots_in_berkeley/ → `documents/01_reddit_study_spots.txt` |
| 2 | life.berkeley.edu | Ranked top 5 libraries (hours, crowding, seat comfort) | https://life.berkeley.edu/top-5-library-study-spots/ → `documents/02_life_top_5_libraries.txt` |
| 3 | life.berkeley.edu | Library crawl walkthrough of specific rooms (Business, Doe NRR, Moffitt) | https://life.berkeley.edu/library-crawl/ → `documents/03_life_library_crawl.txt` |
| 4 | visit.berkeley.edu | Niche spots that empty out at night (Music Library, CAP Library, Stanley Hall, MLK Union) | https://visit.berkeley.edu/news/study-spot-suggestions-campus → `documents/04_visit_night_study_spots.txt` |
| 5 | visit.berkeley.edu | Lesser-trafficked underground spots (e.g., Ishi Court in Dwinelle) | https://visit.berkeley.edu/news/best-underground-spots-campus → `documents/05_visit_underground_spots.txt` |
| 6 | life.berkeley.edu | Hidden gems including Women's Faculty Club Garden | https://life.berkeley.edu/hidden-study-spots → `documents/06_life_hidden_spots.txt` |
| 7 | life.berkeley.edu | Northside cafés (Delah, Foothill Dining, V&A) with vibe and seating notes | https://life.berkeley.edu/northside-study-spots → `documents/07_life_northside_cafes.txt` |
| 8 | life.berkeley.edu | Elmwood/College Ave cafés (Baker & Commons, Souvenir, Timeless, Peet's/Philz) | https://life.berkeley.edu/best-elmwood-study-spots/ → `documents/08_life_elmwood_cafes.txt` |
| 9 | life.berkeley.edu | On-campus café directory with hours and food options | https://life.berkeley.edu/cal-campus-cafe-list → `documents/09_life_campus_cafe_list.txt` |
| 10 | visit.berkeley.edu | Student café ranking filtered for outlets, WiFi, bus access | https://visit.berkeley.edu/node/603 → `documents/10_visit_cafe_ranking.txt` |
| 11 | visit.berkeley.edu | Favorite coffee shops (Strada, Yali's, Brewed Awakening, Cafe Milano) | https://visit.berkeley.edu/news/best-coffee-shops-berkeley → `documents/11_visit_best_coffee_shops.txt` |
| 12 | visit.berkeley.edu | Campus coffee spots including closed "coffee ghosts" | https://visit.berkeley.edu/news/cals-coveted-caffeine-contributors → `documents/12_visit_coffee_cartographer.txt` |
| 13 | life.berkeley.edu | Library hours by closing time, late cafés, BearWalks safety info | https://life.berkeley.edu/late-night-in-berkeley → `documents/13_life_late_night.txt` |
| 14 | Berkeley Law (PDF) | Peaceful study spots guide (scene, distance, directions) | https://www.law.berkeley.edu/files/Mindfulness_Initiative_Guide_to_Peaceful_Campus_Spots(1).pdf → `documents/14_law_mindfulness_guide.pdf` |
| 15 | Simons Institute | Café/restaurant list by distance from campus with seating notes | https://simons.berkeley.edu/berkeley-restaurant-recommendations → `documents/15_simons_restaurants.txt` |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
