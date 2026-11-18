# The World Today — 18 November 2026 in one image

A classic newspaper front page that sums up Wednesday, 18 November 2026's
world news in a single 1024×1024 image (`entry.png`).

**On the page:**
- **Lead — "ASIA'S SUMMIT DAY":** APEC opens in Shenzhen, Trump joins Quad
  talks in Manila, and the first US–China–Russia trilateral follows tomorrow.
- **"UKRAINE HITS CRIMEAN BRIDGE AGAIN"** — a second day of strikes as Russia
  pounds Kyiv's bridges; UN: 372 civilians killed in October.
- **"GULF FLARE-UP"** — Iranian drones strike a US radar in Bahrain; Kuwait
  intercepts drones.
- **"MARKETS REEL"** — Dow –1,000 as tech sells off before Nvidia earnings;
  money runs to gold.
- **"ONE LIGHT-DAY AWAY"** — Voyager 1 nears a full light-day from Earth.
- **Also today:** Cyclone Akvan, the Gaza ceasefire warning, UK sanctions.

## How it was made

Four spot illustrations (`art_summit.png`, `art_bridge.png`, `art_gulf.png`,
`art_voyager.png`) were generated in an engraved newspaper style with no text
in the artwork. Everything else — masthead, headlines, the falling markets
chart, rules and layout — is rendered programmatically with Python PIL
(`compose.py`) so every word is crisp and legible.

## Run

```bash
python3 main.py   # copies entry.png to /output/entry.png
```

`main.py` uses only the Python 3 standard library and is deterministic:
the output is byte-identical on every run.

## License

MIT
