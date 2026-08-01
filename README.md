# The Chancery — a Dúnedain Royal Archive

A data-driven chronicle of Tolkien's legendarium: 171 rulers across 8 royal lines
(Númenor, Arnor, Arthedain, the Chieftains, Gondor, the Ruling Stewards, Dol Amroth,
and Rohan for comparison), with every birth, reign, and death year traced to a source
in *The Lord of the Rings* (Appendix A & B), *The Silmarillion*, *Unfinished Tales*, and
*The Peoples of Middle-earth*.

**Live site:** `https://<your-username>.github.io/<repo-name>/` once Pages is enabled (see below).

## What's here

| File | What it is |
|---|---|
| `index.html` | Landing page linking the three pieces below |
| `dashboard.html` | Interactive dashboard — live filter/search/sort across all 171 rulers, an interactive genealogy-chain diagram for any realm, and a realm comparison tool |
| `kinstrife.html` | A full illustrated narrative account of the Kin-strife (Gondor's civil war, T.A. 1432–1448) and its 600-year aftermath |
| `notebook.html` | Static, pre-rendered view of the full analysis notebook — every chart and statistic, already executed, viewable with no setup |
| `tolkien_dynasties.ipynb` | The original Jupyter notebook, for anyone who wants to open and re-run it themselves (needs `pandas`, `numpy`, `matplotlib`, `ipywidgets`) |
| `data/rulers.csv` | The full underlying dataset as a spreadsheet |

Everything except the `.ipynb` is a static, self-contained HTML file — no build step,
no server, no dependencies beyond a browser. That's what makes GitHub Pages a clean fit.

## Hosting this on GitHub Pages

1. **Create the repo.** On GitHub, click **New repository**. Any name works (e.g. `chancery`).
   Leave it public — GitHub Pages is free for public repos on any plan.
2. **Add these files to the repo root**, keeping the folder structure above (`data/rulers.csv`
   needs to stay inside a `data` folder — the links in `index.html` and `dashboard.html`
   expect that path).
   - Easiest: on the repo's GitHub page, **Add file → Upload files**, drag everything in
     (including the `data` folder), commit.
   - Or from the command line, from inside this folder:
     ```
     git init
     git add .
     git commit -m "Initial commit"
     git branch -M main
     git remote add origin https://github.com/<your-username>/<repo-name>.git
     git push -u origin main
     ```
3. **Turn on Pages.** In the repo: **Settings → Pages**. Under "Build and deployment",
   set Source to **Deploy from a branch**, Branch to **main** and folder to **/ (root)**. Save.
4. Wait 1–2 minutes, then refresh — GitHub shows the live URL at the top of that same
   Pages settings screen. It will be `https://<your-username>.github.io/<repo-name>/`.
   That URL serves `index.html` automatically.

No further setup needed — everything is static HTML with the data already embedded in
each file, so there's nothing to configure, no API keys, no backend.

## Running the notebook locally instead

If you'd rather run `tolkien_dynasties.ipynb` yourself rather than just viewing the
static `notebook.html`:

```
pip install pandas numpy matplotlib ipywidgets jupyter
jupyter notebook tolkien_dynasties.ipynb
```

## Sourcing note

Data was compiled directly from the primary texts, cross-checked against Tolkien Gateway
and fan-maintained genealogical tables where the primary text didn't give exact dates.
Where sources disagreed or a date had to be inferred rather than stated outright, that's
flagged in the notebook's methodology notes and in the dataset itself — see the `source`
and `notes` columns in `data/rulers.csv`.

## License

© 2026 Zendevve. All rights reserved. Licensed for personal, non-commercial use only —
see the full terms in [LICENSE](LICENSE).
