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
