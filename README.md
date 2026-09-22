# travel-reels

Video drop for the Aanya routines. Each run writes one silent 9:16 MP4 under `reels/<place>-<date>.mp4`,
cut from the three carousel photos with `tools/make_reel.sh`, and Buffer fetches it from the raw URL:

    https://raw.githubusercontent.com/hbk9sj/travel-reels/main/reels/<place>-<date>.mp4

Nothing else lives here. Files older than 30 days may be deleted.
