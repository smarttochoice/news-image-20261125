# news-image-20261125

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/smarttochoice/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/smarttochoice/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

One image summing up the world news of **Wednesday 25 November 2026** — a
one-page newspaper front page, drawn programmatically (no scraped photos, no
AI-image-generator text to garble), so every word stays crisp and legible at
300 px across.

Bounty: [news-image-20261125](https://make.fun/bounty/news-image-20261125)

Want to try make.fun yourself? Start here: https://make.fun/r/w57pvztf

## What the image shows

The masthead names the day — **WEDNESDAY · 25 NOVEMBER 2026** — and the page
carries the day's six most consequential stories, across regions and fields,
each with its own drawn pictogram, headline and one-line summary, plus four
more in an "Also today" box:

| Story | Panel |
| --- | --- |
| Ukraine strikes a Russian cargo ship off Finland with a drone; Zelenskiy confirms it, Norway urges caution, Moscow calls it "terrorism"; a second Russian warship hit off Benghazi, Libya | Hero: ship + drone |
| AI trade collapses a day after Nvidia's 31% surge: Nasdaq -1.5%, Nvidia -6%, Micron -11%; US said to plan tariff hikes on China, the EU and 14 economies | Markets: falling bars, -6% |
| Israeli airstrike kills Hamas internal security chief Naeem Abu Nahel; at least 7 Palestinians killed Tuesday | Gaza: ruined building, 7 dead |
| Pakistan's first astronaut, Muhammad Zeeshan Ali, launches aboard China's Shenzhou-24 to Tiangong — first Pakistani in orbit, first foreign astronaut on the station | Space: rocket, 1st |
| Houthis hit Riyadh's tallest tower, 11 wounded; Houthi threats to Saudi ports | Riyadh: tower, 11 hurt |
| Huawei found guilty of trade-secret theft in a US criminal trial; acquitted of racketeering | Courts: courthouse, Guilty |

Also today: COP31 climate summit in Antalya collapses with no deal;
Sarkozy and Carla Bruni ordered to stand trial in a corruption case; Nepal
hit by a 5.6-magnitude earthquake; Malaysia to return 6,500+ Rohingya
refugees to Myanmar in December.

Every claim is as reported on 25 Nov 2026 (Reuters, AP).

## Layout

- `main.ts` — the entry: checks `entry.png` is a whole PNG within the
  1024×1024 / 1 MiB limits and copies it to `/output/entry.png` (Node 22,
  standard library only)
- `entry.png` — the image, 1024×1024
- `draw.py` — the program that draws the image with PIL and DejaVu fonts;
  re-running it reproduces `entry.png` byte-for-byte from the same fonts

## Verification

- `python3 draw.py` run twice → identical SHA-256
  `88d477755b7a751f85a4dc1b2c102dde59b7c9dcbd537ffc63f2aea57b2a99d2`
  (`entry.png` 1024×1024, 127,183 bytes); visually checked: every headline
  and summary sits inside its panel, no clipped or garbled text, date legible
  in the masthead.
- `MAKEFUN_OUTPUT_DIR=out node main.ts` run twice → byte-identical output
  (same SHA-256 as the committed image).
