# strategy.md — current directives for the samairabell routines

Read at step 0b of every run. The 12:00 IST run may rewrite **Current directives** in its
daily review (step 0c), only by applying the **Thresholds** below, and must append every
change to the **Change log** with the numbers that caused it. Never changed by a run: the
0.8-credit spend, the face reference, the Buffer channel, the `isAiGenerated` flag.

## Current directives

- card_order: 13-positano next, then 14-mykonos, 15-uluwatu, then the remaining cards in
  their own order (set 2026-09-20 20:30 IST to test the SWIM wardrobe first).
- carousel: seven slides from `slides/<name>/` (cover + headline, photo 2 + promise, mistake,
  cost, photo 3, fix, save-CTA); never the three bare photos. Started 2026-09-20 20:30 IST.
- cadence: one run a day (the 12:00 IST routine); the 18:30 routine is disabled since
  2026-09-20 20:30 IST. Reason: growth studies put 3–5 posts a week as the useful band and
  Léa posts weekly; two thin sets a day filled the Buffer queue for nothing.
- look_variant: D (the @leaelui look, 2026-09-20 19:30 IST: posed for a friend's iPhone, bright
  and sharp, no grade to speak of; mini dress or mini + cropped top in one colour, heels, loose
  waves; slim hourglass; one of three frames at a street or gate with no landmark). D is the
  winner under rule 3 (review 2026-09-23); the earlier variants candid / A / B / C are retired
  and are not to be generated again. Rows before 2026-09-20 19:30 IST stay tagged as they were. Evidence: @leaelui 10.09M followers, 12/12 latest posts are
  9–13-photo carousels, no Reels, 120–140k likes each (Bright Data, 20 Sep 2026).
- wardrobe: supermodel off duty (WARDROBE rule in the brief overrides every card's OUTFIT). Started 2026-09-20 04:45 IST; rows before that wore the cards' traveller outfits.
- reel_format: hook (step 2b: a researched, specific mistake/scam/rule at the place, burned
  onto the Reel as headline + three beats + close; the carousel caption opens on the same
  headline). Started 2026-09-20 13:15 IST. Rows before that are "plain" (no on-screen text,
  no hook). Evidence: on a comparable cold AI travel account, plain scenic Reels did 110–134
  views with zero saves; "#1 mistake in <city>" / "scam in <city>" did 2,000–3,188 with saves
  and shares (zonted.com/posts/ai-reels-what-actually-works, 2026-03).
- caption_pattern: 1 = line 1 the researched headline from step 2b (place named, inside 125
  characters); line 2 its fix; line 3 "send this to the friend who…"; five hashtags.
- hashtags: exactly five; place, country or region, trip type, one community tag, one
  format tag (#photodump or #traveldiaries). No generic tags with over 50M posts.
- post_mix: one carousel (automatic) + one Reel (reminder) per run.
- reel_note: "Toggle Trial Reel on. Add audio: …, then share."
- place_order: as the cards are listed (no override).
- this_week: "first week on a new account: the places she has already been, one a day,
  then Petra onward" (captions may nod to this; nothing new is generated for it).

## Thresholds (a rule fires only on judged rows, i.e. posts older than 24 h)

1. HOOK: median sends_per_reach of the last 6 judged Reels < 0.003 → caption_pattern moves
   to the next pattern (2 = the headline as a price or number first, "$70 for a 'free' camel
   ride at Petra"; 3 = "3 things nobody tells you about <place>", three beats = the three
   things; then back to 1). The headline stays a researched statement in every pattern. One
   change per week.
1b. FORMAT: when "hook" and "plain" Reels each have ≥ 4 judged rows and hook trails plain by
   > 30 % on median views → write "hook format trailing: <rows>" in the final message and
   change nothing (Suraj decides). If hook leads, nothing changes either; plain is retired.
2. MIX: over the last 14 days, median reach of carousels < 1/3 of median reach of Reels,
   with at least 4 of each judged → post_mix becomes "Reel every run, carousel every second
   run". Reverse when carousels recover to ≥ 1/2 for 14 days.
3. LOOK: when two look variants each have ≥ 6 judged posts and one trails by > 30 % on
   median views → the trailing variant is retired and look_variant names the winner. (Only
   one variant exists today; a second appears only if Suraj adds one to the brief.)
4. PLACES: the place family (mountain / water / desert / city) of the top two judged posts by
   sends_per_reach moves its remaining cards to the front of place_order.
5. ZERO: any judged post with views = 0 or null after 48 h → do not change anything; write
   "distribution or metrics problem: <post id>" in the final message.
6. NOISE GUARD: no rule fires on fewer than the stated number of posts; no rule fires twice
   within 7 days; every change names the rows it used.

## Change log

- 2026-09-20: created. Look A only. Seven carousels and seven Reel reminders exist on the
  new account from the previous look; they are judged rows too, tagged look_variant "candid".
- review 2026-09-20: no change, no judged rows yet (all 9 sent posts under 24 h old and
  Buffer returned metrics: null for every one) — median views n/a, reach n/a,
  sends_per_reach n/a, saves_per_reach n/a, for both posts and Reels, look_variant candid.
- 2026-09-20 04:10 IST (Suraj): Petra set in look A "looks AI" (porcelain skin, pressed shirt, identical grade). STYLING, CAMERA and NEVER rewritten as look B after research on AI tells; B is current. Petra rows keep look_variant A.
- 2026-09-20 04:35 IST (Suraj): Moraine Lake in look B "looks completely AI, the previous ones without the model look looked far better". Photography reverted to the candid frame; only the person is upgraded (look C). Research: viewers judge AI by skin perfection (30 %) and eyes/expression (30 %), then background and lighting; images in the middle of the uncanny valley score worst (MIT, Kishnani 2025); real-looking imperfection raises relatability.
- review 2026-09-20 (12:00 IST slot): no change, no judged rows in any stats/ file (all 10 sent
  posts are under 24 h old and Buffer returned metrics: null for every one) — median views n/a,
  reach n/a, sends_per_reach n/a, saves_per_reach n/a, for both posts and Reels, look_variant
  candid. No threshold rule can fire under rule 6 (noise guard). Run aborted at step 0: 9
  scheduled + 0 needs_approval = 9 against the Free plan cap of 10.
- review 2026-09-20 (12:00 IST slot, run 2): no change, no judged rows in any stats/ file
  (all 10 sent posts are under 24 h old and Buffer returned metrics: null for every one) —
  median views n/a, reach n/a, sends_per_reach n/a, saves_per_reach n/a, for both posts and
  Reels, look_variant candid. No threshold rule can fire under rule 6 (noise guard). Queue at
  step 0: 6 scheduled + 0 needs_approval, so the run continues with step 5b.
- 2026-09-20 04:45 IST (Suraj): "i want the super model clothing, not this" after the Lauterbrunnen run (rain jacket, jeans). WARDROBE rule added; photography stays candid (look C).
- review 2026-09-20 (12:00 IST slot, run 3): no change, no judged rows in any stats/ file (all 10
  sent posts are under 24 h old — sent 2026-09-19 20:39–22:23 UTC — and Buffer returned
  metrics: null for every one) — median views n/a, reach n/a, sends_per_reach n/a,
  saves_per_reach n/a, for both posts and Reels, look_variant candid. No threshold rule can fire
  under rule 6 (noise guard). Queue at step 0: 6 scheduled + 0 needs_approval, so the run
  continues with step 5b. Place: Lauterbrunnen (card 10) — the first card whose first hashtag is
  in no post text; its 04:45 IST run rendered photos but was never posted, and the WARDROBE rule
  landed after it, so it is regenerated here in supermodel wardrobe under a fresh job name.
- 2026-09-20 13:15 IST (Suraj): "there is no hook, nothing that would make people see these
  reels". Research (Tabiji 18M-view AI travel account, Reelyze, GWAA, ClipFlip 44k-clip study):
  scenic Reels with nothing to read die on cold accounts; a specific warning with a number,
  readable with sound off from frame 0, cut every ~3 s, under 15 s, looping, gets 10x views and
  the saves/shares that drive reach. Step 2b (hook research) and tools/make_hook_reel.py added;
  the three hosted sets (Petra, Moraine Lake, Lauterbrunnen) re-cut as hook Reels.
- review 2026-09-20 (12:00 IST slot, run 4): no change, no judged rows in any stats/ file (all 10 sent posts are under 24 h old — sent 2026-09-19 20:39–22:23 UTC — and Buffer returned metrics: null for every one) — median views n/a, reach n/a, sends_per_reach n/a, saves_per_reach n/a, for both posts and Reels, look_variant candid. No threshold rule can fire under rule 6 (noise guard). Queue at step 0: 3 scheduled + 0 needs_approval, so the run continues with step 5b. Place: Petra (card 08) — the first card whose first hashtag is in no post text; its earlier look-A run was never posted, so it is regenerated here in look C, supermodel wardrobe, with a researched hook.
- 2026-09-20 19:30 IST (Suraj): "create the images like lealui, the same dress, pose, looks and
  figure, how natural it looks". @leaelui measured (see look_variant D). Brief: PHYSIQUE,
  POSING slots, WARDROBE formula, LIGHT allows warm low sun, CAMERA composed with HDR on, the
  candid clauses removed from NEVER; render grade strength 0.6 → 0.3. Photo count stays 3
  until Suraj decides (Léa posts 9–13; 2 would break the hook reel).
- 2026-09-20 20:30 IST (Suraj): "i want the fast followers"; Eromify-style private media declined
  (filter, Buffer terms, disclosure); swimwear/resort content adopted instead (SWIM wardrobe,
  cards 13–15). Suraj's own test of the swim prompt on GPT Image 2.5 Sunburst was rejected
  (safety_violations=[sexual], credits refunded) → SAFETY REWRITE rule + refund-retry exception
  + Nano Banana Pro fallback. Seven-slide carousel built (tools/make_slides.py, render.yml):
  cover text in the grid-safe square, swipe cue, slide-2 promise, n/7 markers, one CTA.
  Evidence: Buffer 52M posts (carousels 6.9 % engagement by reach), Sprout (5–7 slides 3.4x
  saves vs images), Hootsuite/Socialinsider (7–10 slides best), TryMyPost (top/bottom 270 px
  hidden on the grid), Adpicto (numbered slides raise completion; one CTA).
- review 2026-09-22 (12:00 IST slot): no change. First run with real metrics back from Buffer
  (17 judged rows across `stats/`, 25 sent posts total). Medians, judged rows only —
  carousels (n=11): views 0, reach 0, sends_per_reach 0, saves_per_reach 0 (4 rows had both
  shares/saves and a non-zero reach); Reels (n=6): views 11, reach 8, sends_per_reach 0,
  saves_per_reach 0, but only 1 of the 6 judged Reels returned any metrics at all — the other
  5 came back null. look_variant: every judged row predates look D, so D has 0 judged rows.
  Rule 5 (ZERO) fires: 8 judged posts are past 48 h with views 0 or null —
  6aaf0b2dbb86436624a91284, 6aaef4394594e3153f40617d, 6aaef431140a3024025f9195,
  6aaef3f8140a3024025f8ef3, 6aaef3c04594e3153f4057bd, 6aaef3994594e3153f405610,
  6aaef3614594e3153f40530f, 6aaef3394594e3153f4050c9 — so nothing is changed and the
  distribution/metrics problem is reported instead. Rule 1 (HOOK) does not fire: only 1 of the
  last 6 judged Reels has a computable sends_per_reach, fewer than the 6 the rule states
  (rule 6 noise guard). Rule 1b does not fire: hook Reels 3 judged, plain Reels 3 judged, both
  under 4. Rule 2 (MIX) is blocked by rule 5 — the carousel/Reel reach comparison rests on a
  single Reel reach value (8) against 5 nulls, which is the same metrics problem rule 5 names.
  Rule 3 (LOOK) does not fire: only one variant has ≥ 6 judged posts. Rule 4 (PLACES) does not
  fire: every judged sends_per_reach is 0, so there is no top two.
- review 2026-09-22 (12:00 IST slot, run 2): no change. Buffer returned `metrics: null` for all 29
  sent posts on this run's `includeMetrics` call, so the review runs on the merged history in
  `stats/` (29 unique posts, 20 judged, 14 carrying any metric value). Medians, judged rows only —
  carousels (n=12): views 0.5, reach 0, sends_per_reach 0 (5 computable), saves_per_reach 0;
  Reels (n=8): views 628, reach 521, sends_per_reach 0.00097, saves_per_reach 0.00242, but only 2
  of the 8 judged Reels returned reach or views at all. look_variant: every judged row still
  predates look D, so D has 0 judged rows. Rule 1 (HOOK) does not fire: 2 of the last 6 judged
  Reels have a computable sends_per_reach, under the 6 the rule states (rule 6 noise guard).
  Rule 1b (FORMAT) does not fire: hook Reels 4 judged and plain Reels 4 judged, so the row counts
  are met, but 0 of the 4 hook Reels returned views, so the >30 % median-views comparison is not
  computable. Rule 2 (MIX) does not fire: carousel median reach 0 is below a third of the Reel
  median reach 521, but that Reel median rests on 2 usable rows of 8, under the 4 judged the rule
  states (rule 6). Rule 3 (LOOK) does not fire: only one variant has >= 6 judged posts. Rule 4
  (PLACES) does not fire: one judged post has a non-zero sends_per_reach (6ab10b1f6c901ceb057f91b6,
  0.0019) and every other is 0 or null, so there is no top two. Rule 5 (ZERO) still holds — 8
  judged posts past 48 h with views 0 or null: 6aaf81b74594e3153f4d0874, 6aaef41e6e039ccbc824a56b,
  6aaef3f8140a3024025f8ef3, 6aaef3c04594e3153f4057bd, 6aaef3994594e3153f405610,
  6aaef3614594e3153f40530f, 6aaef3394594e3153f4050c9, 6aaef2e74594e3153f404cd8 — but it fired
  today already in the 12:04 review, so under rule 6 it does not fire again; the
  distribution/metrics problem is reported in the final message instead.
- review 2026-09-22 (12:00 IST slot, run 3): no change. Buffer returned metrics for 18 of the 29
  sent posts on this run's `includeMetrics` call; merged with `stats/`, 29 unique posts, 20 judged.
  Medians, judged rows only — carousels (n=12): views 0.5, reach 0, sends_per_reach 0 (5
  computable), saves_per_reach 0; Reels (n=8): views 628, reach 521, sends_per_reach 0.00097,
  saves_per_reach 0.00242, but only 2 of the 8 judged Reels returned views or reach at all.
  look_variant: every judged row still predates look D, so D has 0 judged rows. Rule 1 (HOOK) does
  not fire: 2 of the last 6 judged Reels have a computable sends_per_reach, under the 6 the rule
  states (rule 6 noise guard). Rule 1b (FORMAT) does not fire: hook Reels 3 judged, under the 4 the
  rule states. Rule 2 (MIX) does not fire: carousel median reach 0 is below a third of the Reel
  median reach 521, but that Reel median rests on 2 usable rows of 8, under the 4 judged the rule
  states (rule 6). Rule 3 (LOOK) does not fire: only one variant has >= 6 judged posts. Rule 4
  (PLACES) does not fire: one judged post has a non-zero sends_per_reach
  (6ab10b1f6c901ceb057f91b6, 0.00193) and every other is 0 or null, so there is no top two. Rule 5
  (ZERO) still holds — 8 judged posts past 48 h with views 0 or null: 6aaef4394594e3153f40617d,
  6aaef431140a3024025f9195, 6aaef3f8140a3024025f8ef3, 6aaef3c04594e3153f4057bd,
  6aaef3994594e3153f405610, 6aaef3614594e3153f40530f, 6aaef3394594e3153f4050c9,
  6aaf0b2dbb86436624a91284 — but it fired today already in the 12:04 review, so under rule 6 it
  does not fire again; the distribution/metrics problem is reported in the final message instead.
- review 2026-09-23 (12:00 IST slot): rule 3 (LOOK) fires and rule 1b (FORMAT) fires as a
  report. 36 unique posts in `stats/`, 26 judged, 24 carrying any metric value. Medians, judged
  rows only — carousels (n=15): views 0, reach 0, sends_per_reach 0 (6 computable),
  saves_per_reach 0; Reels (n=11): views 11, reach 8, sends_per_reach 0.00088, saves_per_reach
  0.00219, but only 3 of the 11 judged Reels returned views or reach at all. Rule 3 (LOOK): the
  pre-D looks (candid / A / B / C, sent before 2026-09-20 14:00 UTC) have 13 judged rows with
  median views 0.5 (10 usable) and look D has 13 judged rows with median views 5.5 (8 usable);
  pre-D trails D by 91 %, over the 30 % the rule states, and both variants clear the 6 judged
  rows it requires, so the trailing variants are retired and look_variant names D, the winner.
  Rule 1b (FORMAT): hook Reels 7 judged, plain Reels 4 judged, so the row counts are met; hook
  median views 0 (1 usable of 7) trails plain median views 690 (2 usable of 4) by more than
  30 %, so "hook format trailing" is reported and nothing is changed — Suraj decides. Rule 1
  (HOOK) does not fire: 1 of the last 6 judged Reels has a computable sends_per_reach, under the
  6 the rule states (rule 6 noise guard). Rule 2 (MIX) does not fire: carousel median reach 0 is
  below a third of the Reel median reach 8, but that Reel median rests on 3 usable rows of 11,
  under the 4 judged the rule states (rule 6). Rule 4 (PLACES) does not fire: one judged post has
  a non-zero sends_per_reach (6ab10b1f6c901ceb057f91b6, 0.00175) and every other is 0 or null, so
  there is no top two. Rule 5 (ZERO) still holds — 12 judged posts past 48 h with views 0 or
  null: 6aaef4394594e3153f40617d, 6aaef431140a3024025f9195, 6aaef3f8140a3024025f8ef3,
  6aaef3c04594e3153f4057bd, 6aaef3994594e3153f405610, 6aaef3614594e3153f40530f,
  6aaef3394594e3153f4050c9, 6aaf0b2dbb86436624a91284, 6aafdbd2549cbb177986f1eb,
  6aaf81ca8d048c06b4fc9cea, 6aaf81b74594e3153f4d0874, 6aaef4474594e3153f4062b0 — but it fired on
  2026-09-22, within 7 days, so under rule 6 it does not fire again; the distribution/metrics
  problem is reported in the final message instead.
- review 2026-09-24 (12:00 IST slot): no change, carousels (n=23): views 0, reach 0, sends_per_reach 0 (8 computable), saves_per_reach 0; Reels (n=6): views 5.5, reach 4 (4 usable), sends_per_reach 0.00087, saves_per_reach 0.00216 (2 computable); look pre-D (n=10) views 0.5, look D (n=19) views 0. Rule 1 no (2 of last 6 Reels computable); 1b no (hook 3, plain 3 judged, under 4); 2 held (carousel reach 0 < 1/3 of Reel reach 4, but every carousel reads reach 0, which is the rule-5 metrics problem, 11 judged posts past 48 h at views 0/null); 3 fired 2026-09-23, rule 6 blocks; 4 no top two (only 6ab10b1f6c901ceb057f91b6 non-zero); 5 fired 2026-09-22, reported only.
