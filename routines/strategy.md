# strategy.md — current directives for the samairabell routines

Read at step 0b of every run. The 12:00 IST run may rewrite **Current directives** in its
daily review (step 0c), only by applying the **Thresholds** below, and must append every
change to the **Change log** with the numbers that caused it. Never changed by a run: the
0.8-credit spend, the face reference, the Buffer channel, the `isAiGenerated` flag.

## Current directives

- look_variant: D (the @leaelui look, 2026-09-20 19:30 IST: posed for a friend's iPhone, bright
  and sharp, no grade to speak of; mini dress or mini + cropped top in one colour, heels, loose
  waves; slim hourglass; one of three frames at a street or gate with no landmark). Rows before
  that: candid / A / B / C as tagged. Evidence: @leaelui 10.09M followers, 12/12 latest posts are
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
