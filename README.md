# The Unofficial Guide — Project 1

A RAG system that makes Berkeley study-spot knowledge searchable: libraries, cafés, hidden corners, and late-night options, grounded in student blogs and guides.

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

**Chunk size:** ~400–600 characters (~80–120 tokens), hard max ~700 characters before forcing a split within a section.

**Overlap:** ~80–100 characters (~15–20%), implemented by carrying the last paragraph of the previous chunk into the next when a section is split.

**Why these choices fit your documents:**

My corpus mixes location-based guides, short café blurbs, directory lists, and a Reddit thread. A single fixed character split would either break a library section mid-thought or merge unrelated spots. I used **structure-aware chunking**: split on document structure first (numbered headings, `---` separators, spot/café headers, Reddit replies), then apply the character size cap.

Preprocessing before chunking: strip Reddit UI tokens (`Upvote`, `Reply`, etc.), remove image-caption boilerplate (`A collage of…`, `decorative image`), collapse extra blank lines, and parse `Source:` headers into metadata (excluded from chunk body).

**Final chunk count:** 123 chunks across 15 documents (within the 80–150 target from `planning.md`).

### Sample chunks

**Chunk 1 — `05_visit_underground_spots.txt` (chunk 1)**
> 1. Ishi Court — Hidden in the bowels of Dwinelle Hall, Ishi Court is a beautiful courtyard… I'd recommend entering Dwinelle through the North entrance and going straight into Ishi Court.

**Chunk 2 — `02_life_top_5_libraries.txt` (chunk 12)**
> 1. Moffitt Library — Open 8 a.m. to 10 p.m.… Popularity well-deserved. Are you shocked to see Moffitt as the number one study spot?

**Chunk 3 — `07_life_northside_cafes.txt` (chunk 1)**
> Delah Coffee: Eye-catching and bougie… Arabian coffee for less than $5… barstool seating between outlets… 10/10 for studious vibes!

**Chunk 4 — `13_life_late_night.txt` (chunk 1)**
> Open until 2 a.m.: Main Stacks. 24 hours: Moffitt (Note: Moffitt Library is closed for renovations starting in January 2025.)

**Chunk 5 — `10_visit_cafe_ranking.txt` (chunk 4)**
> 4. Delah Coffee — Close to Northside of campus on Euclid Avenue… perfect place for an impromptu study session with friends.

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`, embedded into ChromaDB with cosine distance. Runs locally with no API key.

**Production tradeoff reflection:**

If cost were not a constraint, I would test stronger models like `bge-small-en-v1.5` or `e5-base-v2` for better matching on short opinion text and campus nicknames ("Main Stacks", "Soda"). Longer-context embeddings would help if I kept whole library sections unsplit. Multilingual embeddings would matter for non-English reviews. MiniLM's advantage is zero API cost and low latency locally; hosted models add billing and network latency but scale better for concurrent users. Embeddings cannot fix stale facts — Moffitt's renovation closure appears inconsistently across sources, which is a corpus freshness problem.

---

## Retrieval Tests

Tested with `python test_retrieval.py` (top-k=5). Below are three evaluation queries with top results and why they are relevant.

### Query: "Which libraries stay open until 2 a.m.?" (distance 0.28)

**Top chunk:** `13_life_late_night.txt` — lists library hours by closing time, including "Open until 2 a.m.: Main Stacks."

**Why relevant:** The query asks about late-night library hours; this chunk directly answers with a structured hours list from the late-night guide.

### Query: "Where is Ishi Court and how do students recommend finding it?" (distance 0.29)

**Top chunk:** `06_life_hidden_spots.txt` — describes Ishi Court as a hidden courtyard inside Dwinelle Hall.

**Second chunk:** `05_visit_underground_spots.txt` — recommends entering Dwinelle through the North entrance.

**Why relevant:** Together these chunks cover location (Dwinelle) and navigation advice (North entrance), matching both parts of the question.

### Query: "What do students say about Delah Coffee as a Northside study spot?" (distance 0.30)

**Top chunk:** `10_visit_cafe_ranking.txt` — ranks Delah on Euclid as a staple for impromptu study sessions.

**Second chunk:** `07_life_northside_cafes.txt` — describes Delah's vibe, outlets, quiet music, and Arabian coffee under $5.

**Why relevant:** Both chunks are student-written descriptions of Delah specifically as a Northside study café.

---

## Grounded Generation

**System prompt grounding instruction:**

The system prompt in `query.py` instructs the model to:
1. Answer ONLY from provided document excerpts
2. Respond with exactly *"I don't have enough information on that."* if excerpts are insufficient
3. Cite source filenames when stating facts
4. Not invent study spots, hours, or opinions

Additionally, if the best retrieved chunk has cosine distance > 0.65, the pipeline returns the refusal message without calling the LLM.

**How source attribution is surfaced in the response:**

- Retrieved chunks are labeled `[Source: filename | chunk N]` in the prompt context
- The system prompt requires the model to cite filenames in the answer text
- If the model omits citations, `ask()` appends `Sources: filename1, filename2, ...` programmatically
- The Gradio UI shows a separate **Retrieved from** field listing all source files used

---

## Example Responses

**Query:** Where is Ishi Court and how do students recommend finding it?

**Answer:** Ishi Court is located in Dwinelle Hall [06_life_hidden_spots.txt, 05_visit_underground_spots.txt]. To find it, students recommend entering Dwinelle through the North entrance and going straight into Ishi Court… [05_visit_underground_spots.txt]

**Retrieved from:** `05_visit_underground_spots.txt`, `06_life_hidden_spots.txt`

---

**Query:** Which libraries stay open until 2 a.m.?

**Answer:** The Main Stacks library stays open until 2 a.m. [13_life_late_night.txt]

**Retrieved from:** `13_life_late_night.txt`, `02_life_top_5_libraries.txt`, `04_visit_night_study_spots.txt`

---

**Out-of-scope query:** What is the best study spot at Stanford?

**Answer:** I don't have enough information on that.

---

## Query Interface

**Interface:** Gradio web UI (`python app.py`), opens at `http://localhost:7860`

**Input:** Text box labeled "Your question" — plain-language questions about Berkeley study spots.

**Output:**
- **Answer** — grounded response with inline source citations
- **Retrieved from** — bullet list of source filenames used

**Sample interaction:**

| Field | Content |
|-------|---------|
| **Question** | What do students say about Delah Coffee as a Northside study spot? |
| **Answer** | Delah Coffee is described as a staple for impromptu study sessions [10_visit_cafe_ranking.txt] and a 10/10 for studious vibes with quiet music and comfy seating [07_life_northside_cafes.txt]. |
| **Retrieved from** | • 07_life_northside_cafes.txt • 10_visit_cafe_ranking.txt • 12_visit_coffee_cartographer.txt |

---

## Evaluation Report

Run with `python run_evaluation.py`. Results saved to `data/evaluation_results.json`.

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which library is ranked #1 for study spots and why? | Moffitt — longest hours, variety of spaces, outlets; renovation note | "I don't have enough information on that." Top retrieval was generic library intro from `04_visit_night_study_spots.txt` (dist 0.37); Moffitt #1 chunk not in top 5 | Partially relevant | Partially accurate |
| 2 | Which libraries stay open until 2 a.m.? | Main Stacks until 2 a.m.; Moffitt 24h with renovation note | Correctly states Main Stacks until 2 a.m. [13_life_late_night.txt]. Does not mention Moffitt 24h note | Relevant | Partially accurate |
| 3 | Where is Ishi Court and how do students recommend finding it? | Courtyard in Dwinelle; enter via North entrance | Correct location in Dwinelle and North entrance directions with citations | Relevant | Accurate |
| 4 | What do students say about Delah Coffee as a Northside study spot? | Euclid, outlets, quiet music, Arabian coffee <$5, bougie vibe | Mentions studious vibes, quiet music, impromptu study sessions; omits Euclid, outlets, and $5 detail | Relevant | Partially accurate |
| 5 | What non-library spots do r/berkeley users recommend? | Brewed Awakening, Cafe Milano upstairs, Dwinelle classrooms, MLK, Boalt cafe, Soda labs | "I don't have enough information on that." Reddit doc empty; retrieval returned library/blog chunks | Off-target | Inaccurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:** Which library is ranked #1 for study spots and why?

**What the system returned:** "I don't have enough information on that." — technically correct given retrieved context, but unhelpful because the answer exists in the corpus.

**Root cause (tied to a specific pipeline stage):** **Retrieval + chunking.** The Moffitt #1 chunk (`02_life_top_5_libraries.txt`, chunk 12) contains "Moffitt as the number one study spot" but ranked **#21** for this query (distance 0.52). Generic introductory chunks about "discovering the ultimate study spot" from `02` and `04` scored higher (distance ~0.37) because they share vocabulary with the question without containing the actual ranking. The Moffitt section was also split across chunks 12–14, so the "why" (hours, pods, outlets) was separated from the "#1" label.

**What you would change to fix it:** Keep each ranked library entry as a single chunk when under ~900 characters, or prepend a searchable prefix like "Ranked #1 study library: Moffitt" to the embedding text. Could also boost retrieval for `02_life_top_5_libraries.txt` when the query mentions "ranked" or "#1".

**Secondary failure (Q5):** `01_reddit_study_spots.txt` was never populated with thread content, so the corpus has zero Reddit chunks. Retrieval cannot surface Brewed Awakening, Cafe Milano, etc. Fix: paste the Reddit thread and rebuild chunks/index.

---

## Spec Reflection

**One way the spec helped you during implementation:**

The structure-aware chunking plan in `planning.md` prevented me from using a naive 500-character split. Specifying split rules per document type (numbered spots, `---` separators, Reddit replies) led directly to `chunking.py` functions like `_split_on_pattern()` and `_split_late_night()`. The evaluation plan's five specific questions gave concrete targets for retrieval testing before adding generation.

**One way your implementation diverged from the spec, and why:**

The spec targeted 80–150 chunks and I landed at 123, but the Reddit file (`01_reddit_study_spots.txt`) remained a placeholder, so the Reddit-specific cleaning and one-chunk-per-reply rule was implemented but never exercised on real data. I also added a distance-based refusal gate (distance > 0.65) in `query.py`, which was not in the original spec but prevents the LLM from hallucinating when retrieval confidence is low.

---

## AI Usage

**Instance 1 — Document pipeline (Milestone 3)**

- *What I gave the AI:* `planning.md` Documents table, Chunking Strategy section, Architecture diagram, and sample excerpts from `02_life_top_5_libraries.txt` and `01_reddit_study_spots.txt`
- *What it produced:* Initial `ingest.py` and `chunking.py` with `load_documents()`, `clean_text()`, and structure-aware `chunk_documents()`
- *What I changed or overrode:* Fixed curly-apostrophe handling in spot-header regex (`Women's` vs `Women's`), switched overlap from raw character tails to last-paragraph overlap after seeing mid-word fragments, and corrected section boundaries so Ishi Court chunks did not include the next spot's header

**Instance 2 — Embedding, retrieval, and generation (Milestones 4–5)**

- *What I gave the AI:* Retrieval Approach from `planning.md`, pipeline diagram, chunk JSON format, Groq grounding requirements, and Gradio skeleton from assignment instructions
- *What it produced:* `vector_store.py` (ChromaDB + `all-MiniLM-L6-v2`), `test_retrieval.py`, `query.py` with grounded system prompt, and `app.py` Gradio UI
- *What I changed or overrode:* Added `NotFoundError` handling when resetting Chroma collections, programmatic source citation fallback when the LLM omits filenames, and distance-based refusal before LLM calls; verified retrieval on eval queries before wiring generation

---

## How to Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # or create .env with GROQ_API_KEY=your_key
python build_chunks.py
python build_index.py
python app.py            # Gradio UI at http://localhost:7860
```
