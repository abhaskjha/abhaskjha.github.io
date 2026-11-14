# abhaskjha.github.io

Static GitHub Pages site for Abhas Jha.

## Files

- `index.html`: main site content
- `styles.css`: layout, typography, color system, and motion
- `script.js`: client-side rendering for the live newsletter feeds
- `assets/images/abhas-photo-dec-2025.jpg`: hero image sourced from the PARA folder
- `data/latest-writing.json`: generated feed data for Substack and India Decoded
- `scripts/update_writing_feeds.py`: refreshes the feed data
- `.github/workflows/update-writing-feeds.yml`: scheduled GitHub Action that keeps the feeds current

## Publish on GitHub Pages

1. Create or open the repository named `abhaskjha.github.io`.
2. Copy these files into the repository root.
3. Commit and push to the default branch.
4. GitHub Pages will serve the site automatically from the repository root.

## Content notes

- The homepage is intentionally structured as a thought-leader site rather than a CV.
- It links to `The Urban Stack`, `India Decoded`, LinkedIn, World Bank, and verified publication records available online.
- The design direction is contemporary and editorial, with Ethan Mollick's public-facing style used as the main reference point.
- The site now includes an auto-updating feed section for `The Urban Stack` and `India Decoded`, backed by a scheduled GitHub Action.

## Canonical housing book

The **14 November 2026** cumulative edition of **Housing the Next Billion: A Practitioner’s Handbook** is the author-designated canonical source for all subsequent book revisions. It contains 444 pages, 25 chapters and 86 editable tables. Use this edition rather than the earlier November 7 practitioner’s handbook. Earlier editions remain in Git history.

- PDF: `housing-the-next-billion-discussion-edition.pdf`
- Editable manuscript: `Housing_the_Next_Billion_Corrected_2026-11-05_Updated_2026-11-14.docx`
- Edition identity and SHA-256 file hashes: `data/housing-book.json`

The PDF restores the original illustrated cover with the 14 November date; all 443 interior pages are unchanged from the original download. The DOCX remains the original editable manuscript with its plain title page. Preserve the illustrated PDF cover when publishing subsequent revisions. Verify hashes before further revisions. The book remains a draft for comments; some original Masterclass sources remain unavailable for full reconciliation. Publication checks do not constitute a fresh empirical audit or institutional clearance.
