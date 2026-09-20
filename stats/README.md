One file per run, `stats/<YYYY-MM-DD-HHMM>.json`, written by step 0b of the brief: a list of
rows, one per sent post on the channel, with `id, sentAt, type, place, first_line, look_variant,
views, reach, likes, comments, saves, shares, follows, sends_per_reach, saves_per_reach,
reel_format, judged`. Metrics come from Buffer (`includeMetrics: true`) and lag about a day; `judged` is
false for posts younger than 24 hours. The daily review in step 0c reads every file here.
