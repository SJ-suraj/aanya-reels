# strategy.md — current directives for the samairabell routines

Read at step 0b of every run. The 12:00 IST run may rewrite **Current directives** in its
daily review (step 0c), only by applying the **Thresholds** below, and must append every
change to the **Change log** with the numbers that caused it. Never changed by a run: the
0.8-credit spend, the face reference, the Buffer channel, the `isAiGenerated` flag.

## Current directives

- look_variant: B (model on location, real skin: pores, peach fuzz, asymmetry, Portra 400 grain, honest cloth). Started 2026-09-20 04:10 IST. Variant A (polished model look) produced only the Petra set of 20 Sep and reads as AI; it stays in the data for rule 3.
- caption_pattern: 1 = line 1 place name + hook inside 125 characters; line 2 one true
  detail; line 3 "send this to the friend who…"; five hashtags.
- hashtags: exactly five; place, country or region, trip type, one community tag, one
  format tag (#photodump or #traveldiaries). No generic tags with over 50M posts.
- post_mix: one carousel (automatic) + one Reel (reminder) per run.
- reel_note: "Toggle Trial Reel on. Add audio: …, then share."
- place_order: as the cards are listed (no override).
- this_week: "first week on a new account: the places she has already been, one a day,
  then Petra onward" (captions may nod to this; nothing new is generated for it).

## Thresholds (a rule fires only on judged rows, i.e. posts older than 24 h)

1. HOOK: median sends_per_reach of the last 6 judged Reels < 0.003 → caption_pattern moves
   to the next pattern (2 = a question in line 1 that the photo answers; 3 = a number in
   line 1, "3 things nobody tells you about <place>"; then back to 1). One change per week.
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
