# CSA08-192525205-Assignment5

| | |
|---|---|
| Name | Saai Vardhan D |
| Register number | 192525205 |
| Course | 0826 – Python Programming (CO5: data acquisition, cleaning, SQLite, pandas, charts, simple AI) |
| Python | 3.13 |
| Libraries | pandas 3.0.5, numpy 2.5.3, matplotlib 3.11.2 (see `requirements.txt`); `csv`, `sqlite3`, `statistics`, `re`, `cProfile`, `tracemalloc`, `logging` from the standard library |

`pip install -r requirements.txt`

**Data note:** the 12 station files are *synthetic* (made by `common/datagen.py` with a fixed seed, with the faults of the case study injected on purpose). The 60 citizen complaints in `B4/complaints.py` were written by me. No real board data was used.

Part A (design, pseudocode) is in the report only. Part B code is below. Run every command from the folder named, with `python` = Python 3.13.

## Run commands and one-line result per task

### B1 – cleaning pipeline (`cd B1`)
| Program | Command | Result |
|---|---|---|
| Data before/after on a 13-row file with every problem | `python b1_cleaning_demo.py` | 13 rows → 11; every hand-derived check passed |
| Whole network → SQLite (`executemany`) + 3 queries | `python b1_pipeline.py` | 9,044 rows read, 116 duplicates removed, 8,928 stored; Adyar October mean 43.06 (87.3 from the raw CSV) |
| Four charts (run after b1_pipeline.py: reads air_quality.db) | `python b1_charts.py` | trend +0.26 µg/m³ per day; Ennore median 2.5× Adyar; worst hour 21:00 |
| Complete the Code | `python given_b1_completed.py` and `python given_b1_extended.py` | output equals the expected output; the extension rejects 5000 |
| Edge cases of the code | `python b1_edge_cases.py` | equal values / empty list crashed the first version; guards added |
| pandas versus loops | `python b1_pandas_compare.py` | 0 differing cells; 2.6–3.7× faster at 100,000+ rows, slower at 1,000 |
| A2 alternative (drop / forward fill / median) | `python b1_fill_alternatives.py` | forward fill most accurate for scattered gaps, median for long outages |
| A4 alternative (print versus logging) | `python b1_debug_overhead.py` | 100,000 enabled logging calls cost 0.64 s; disabled 0.007 s |

`raw_data/` holds the 12 generated CSV files. To regenerate them: `python ../common/datagen.py` (writes `raw_data/` in the current folder). `air_quality.db` is created by `b1_pipeline.py`.

### B2 – adversarial inputs (`cd B2`)
| Program | Command | Result |
|---|---|---|
| Complete the Code (executemany, parameterised query) | `python given_b2_completed.py` | `54.0 108.0` and `None` |
| Quote in a name, SQL injection | `python b2_injection.py` | `+` and f-string break or leak; `?` is safe |
| Seven bad files, naive and defensive loader | `python b2_robust_loader.py` | naive: 2 KeyError, 2 UnicodeDecodeError, 2 silent empty results; defensive: clear message or fixed |
| Sentiment on tricky text | `python b2_sentiment_adversarial.py` | 10 of 15 right; sarcasm, double negative, spelling, punctuation fail silently |
| executemany versus loop | `python b2_executemany_timing.py` | commit per row 6.8 s for 10,000 rows; executemany 0.007 s |

### B3 – three methods, one answer (`cd B3`)
`python b3_compare.py` (creates test data in /tmp/b3) – loops, pandas and SQL agree on the small data; at 120 stations (1,051,200 rows) loops 1.56 s, pandas 0.43 s, SQL 1.47 s; cProfile shows `csv.DictReader` and `statistics.mean` dominate; one pass with running sums uses 17.9 MB instead of 50.2 MB.

### B4 – AI and index (`cd B4`)
| Program | Command | Result |
|---|---|---|
| Complete the Code (score) | `python given_b4_completed.py` | positive / negative / negative / positive, as expected |
| Sentiment and summariser on 60 complaints | `python b4_ai.py` | scorer agrees with my labels on 50 of 60 (83%); first-sentence summary beats frequency summary on my set (56 v 51), with a bias caveat |
| Index on (station, day), 3.9 million rows | `python b4_index.py` (about 1 minute; creates a 130 MB temporary database in /tmp) | station-day lookup 14,052× faster, one station 42×, all-stations-one-day no gain, inserts 2.6× slower |

## Commits (one per task, run from the repository folder)
```
git init
git add README.md requirements.txt common
git commit -m "Setup: README, requirements, shared modules (data generator, cleaning, sentiment)"
git add B1 && git commit -m "B1: cleaning pipeline, SQLite load, charts, complete-the-code, pandas comparison"
git add B2 && git commit -m "B2: adversarial files, SQL injection, sentiment stress test, executemany timing"
git add B3 && git commit -m "B3: loops vs pandas vs SQL, profiling, memory"
git add B4 && git commit -m "B4: sentiment and summariser on 60 complaints, index experiment"
git branch -M main
git remote add origin https://github.com/<your-username>/CSA08-192525205-Assignment5.git
git push -u origin main
```
The repository has fewer than 100 files, so it can be uploaded to GitHub in one drag-and-drop (GitHub's web upload accepts up to 100 files at a time).
