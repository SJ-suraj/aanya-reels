One file per reel: `jobs/<name>.json` = `{"name": "<place>-<date>", "urls": ["<photo 01>", "<photo 02>", "<photo 03>"]}`.
Pushing it to main runs `.github/workflows/render.yml`, which writes `reels/<name>.mp4` within a couple of minutes.
