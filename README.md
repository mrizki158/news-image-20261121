# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/mrizki158/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/mrizki158/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One image that sums up the world news of **Saturday 21 November 2026** in **45 sourced stories**: four illustrated leads (Iran saying it struck two US bases in Bahrain, the AI rout pushing the S&P 500 and the Dow into correction, a Russian ballistic missile hitting Zelensky's hometown Kryvyi Rih, and Mexico capturing FBI most-wanted cartel boss "Chapo Isidro" in Sinaloa), ten illustrated tiles (COP31 deadlocked in overtime in Antalya, France taking the ICJ Myanmar ruling to the UN Security Council, Zelensky calling Putin "a killer" as Trump defends his Putin ties, drones setting the Russian cargo ship Sparta II ablaze in the Gulf of Finland, an Israeli strike killing three in a Gaza food vehicle, Houthi and Saudi-led forces trading strikes, a mathematician's claimed AI-assisted proof of the Riemann hypothesis — drawn as a claim, as reported — a reported hack of the FBI's NCIC database, BepiColombo entering Mercury orbit, and England's record 37–12 rout of the All Blacks), and a 31-item world index beside a pinned dot-matrix world map — plus a markets strip, a "Saturday in five acts" strip and a date check. Every story was cross-checked against at least two independent reports dated 21 November 2026; the market figures were verified against WSJ and Reuters. The image is composed by `build_image.py` (Pillow; the lead scenes and every pictogram are drawn in code, and all page text is typeset so nothing can garble); `main.py` copies it to `/output/entry.png`.

No clock times appear anywhere on the page: precise event times for the day could not be verified, so the day is told in five acts rather than on an invented timeline.

## Run it

```sh
python3 build_image.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=qe91xxve&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
