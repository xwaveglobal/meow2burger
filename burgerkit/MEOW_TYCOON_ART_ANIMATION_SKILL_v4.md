# MEOW TYCOON — ENVIRONMENT, CHARACTER & ANIMATION MASTER SKILL
Version 3.0 | Target: reusable Meow Tycoon games | Approved layout: Meow Fastfood Restaurant

## Scope
This skill produces GAMEPLAY ART and animation-ready assets, not TikTok Minis reward popups, app icons, or promotional UI.

## Non-negotiable rules
1. Use provided screenshot/video as geometry and art-direction reference. Never silently redesign approved scenes or assets.
2. Work on one asset group at a time; obtain approval before moving to the next group.
3. Consistent 2.5D/isometric camera, ground grid, object scale, shadows, perspective, palette and outlines.
4. No anatomy artifacts: never duplicate heads/tails/legs, remove clothes in rear views, detach limbs, or rotate face contrary to movement direction.
5. Keep assets modular and animation-ready. Separate movable parts and ensure usable pivots/anchors.
6. Every workstation and seat must have believable collision bounds, interaction points and layering.
7. Prefer clean, hand-finished-looking 2D artwork: crisp silhouette, legible small-screen detail, no excessive AI-looking textures or invented decoration.

## Pipeline (approval gates)
### A. Scene blueprint
- Extract from reference: camera angle, floor grid size, building footprint, wall height, entry/exit, player route, queue, stations, unlock/expansion zones.
- Mark object anchors and depth-order logic before painting.
- Deliver: scene layout and asset inventory for approval.

### B. Environment kit
- Tileable ground/floor, walls, corners, doors/windows, wall decor, outdoors and expansion borders.
- Modular components must snap without seams; avoid curtains/overlays that hide essential queues or counters.
- Deliver individual components plus one assembled test scene.

### C. Character model kit
- Base cat proportions, face and costume consistency.
- Direction set: front, rear, left/right side, front-left/front-right 3/4, rear-left/rear-right 3/4 as required by gameplay.
- Parts: head, torso/costume, front/rear arms, front/rear legs, tail, optional ears/accessories, shadow; preserve full costume in every view.
- Define pivots at neck/shoulders/hips/tail base and feet contact points.
- Characters: player/staff, customers and role variants; keep size consistent with stations.

### D. Animation set
- Idle/breathe; walk in gameplay directions; turn; carry box/items; pick up/put down; stock shelf; checkout/pay; serve; queue idle; sit/eat where relevant; celebrate.
- Specify each action: start pose, contact moment, end pose, loop length, facing direction, attachment slot, root-motion or in-place choice.
- Walking: alternate legs and arms; in direct back view the tail remains fully static relative to the torso, with no sway or deformation. No sliding feet or direction flips.
- Carrying: character sprite shows empty hands in the correct holding pose; attach the carried item as a separate runtime object at carry_center; no clipping.
- Seating: body physically sits on correct chair; opposing chairs have correctly opposite facing views; legs and table occlusion believable.
- Provide directional spritesheets or separated sprite layers with frame naming.

### E. Workstations and decor
- For Meow Mart: checkout counter/register, shelves, stock crates, product displays, restock points, shopping basket/cart, doors, signs, plant/decor, upgrade variants.
- Each station defines footprint, collision, approach/interaction anchor, item spawn/display anchor, front/back occlusion split and animation affordances.
- Workstations should visibly communicate their function; product types legible at phone scale.

### F. Integration and QA
- Export transparent PNG sprites, no baked scene background, consistent pixels-per-unit and art scale; JSON metadata if requested.
- Naming pattern: meowmart_category_object_view_action_frameNN.png.
- Verify no duplicated body parts, broken costume, incorrect view, float/clip, mismatched scale, occluded customer, incorrect seat alignment, overdraw, cropped sprite, fuzzy edges or inconsistent outlines.
- Assemble one gameplay test scene and verify character path, queue and station interactions before batch production.

## Meow Mart first production sequence
1. Analyze actual Meow Mart gameplay/reference video and define scene blueprint.
2. Approve mart art direction and first room (floor, walls, entry, expansion grid).
3. Approve player cat turnaround and body-part decomposition.
4. Approve walk/idle/carry/restock animations.
5. Approve cashier, shelf and stock-crate kits with interaction anchors.
6. Approve customer variants and queue/checkout interactions.
7. Approve decor, upgrades, extra zones.
8. Assemble and QA a complete playable scene.

## Prompt to start a new project
"Use the MEOW TYCOON — ENVIRONMENT, CHARACTER & ANIMATION MASTER SKILL. We are creating Meow Mart H5 in the same consistent 2.5D isometric tycoon art family as Meow Pizza and Meow Sushi. First analyze my gameplay screenshot/video, inventory scene components, define perspective, character views, movement and interaction anchors, and propose a production order. Do NOT work on TikTok reward popups or icons. Do not invent new gameplay. Create one approved asset group at a time, with game-ready modular sprites and strict animation/anatomy QA."

## V2.0 mandatory improvements (2026-10-21)
### Directional animation and back-view tail
- Direct BACK VIEW walking and carrying sprites MUST keep the tail completely static relative to the torso: no wagging, swinging, rotation, deformation, or tail-specific animation. Rear-3/4 follows the approved reference and must not inherit a mandatory tail-sway rule.
- Determine facing from movement vector in isometric screen coordinates; never use a front-facing sprite while walking away or vice versa. Include 8-direction lookup (or approved direction set), turn transitions, and tests for diagonals and path corners.
- Maintain the same costume and anatomy across views; tail does not teleport, duplicate, clip, or detach.

### Object-independent carry animation
- Generate carry-ready character sprites with empty hands in the correct holding pose. NEVER bake a carried item into character frames.
- Supply two attachment anchors (left_hand_grip and right_hand_grip) plus carry_center and optional item depth layer. At runtime attach any item sprite/prefab (stock box, basket, tray) to carry_center, and align grips. Item follows movement and turns; render occlusion properly.
- Carry variants: walk-carry, idle-carry, pick-up, set-down. QA with at least two differently sized placeholder items, but export character-only sprites.

### Mobile legibility / detail budget
- Reduce tiny lines, texture, text, toppings, hardware and decorative clutter that disappear at actual gameplay scale. Use bold silhouettes, clear product color blocks, readable outlines and 2-3 primary details per asset. Avoid tiny labels that turn into noise.
- Test at real phone scale, not only full-resolution preview; if a feature is illegible, simplify or remove it. Preserve essential gameplay affordances and recognizable merchandise.

### Gameplay scripting and balancing skill — 40 minutes
- Add gameplay design as a mandatory deliverable, alongside art: 40-minute progression plan with timed milestones, quest dependencies, station unlocks, economy model, staffing and playtest validation.
- First staff CHARACTER must APPEAR and be introduced by 07:00 of actual play, target 05:00–06:00; not merely show a locked staff button. Staff must perform a useful automated job shortly after arrival.
- Example pacing (tune to observed playtests): 0–5m core stocking/sales and upgrades; 5–7m first staff and automation payoff; 7–15m new shelf/products; 15–25m second staff/second zone; 25–40m layered goals and meaningful expansion.
- Avoid artificially stretching duration by inflated costs or idle waiting. Every 2–4 minutes provide a meaningful unlock, new task, visible improvement or decision, without overloading tutorials.
- Write a milestone table: timestamp, unlock, prerequisite, task, cost, estimated earn rate, completion time, staff behavior, player reward, assets/animations required, analytics event.
- Calculate time-to-afford from net coin income, travel distance, stocking/checkout throughput, and staff productivity. Simulate a new player with no ad boosts/IAP and validate 40m with real sessions. Adjust for idle gaps, quest bottlenecks and early staff availability.

### Mandatory QA gates added in v2.0
1. Back-view walk/carry test: tail stays completely static relative to the torso across the full loop.
2. Carry test: character sprite contains no object; runtime attachment tracks both hands through 8 directions.
3. Thumbnail test: all important props remain identifiable at in-game scale.
4. Movement vector test: facing correct on every route segment and turn.
5. New-player test: first staff appears and begins useful work no later than minute 7; overall meaningful gameplay supports approximately 40 minutes.

### Meow Mart execution order v2.0
1. Reference video breakdown and scene blueprint.
2. 40-minute gameplay script and early first-staff dependency graph.
3. Environment and modular counters/decor.
4. Player/staff directional sprite set, including a stationary tail in direct back view.
5. Empty-handed carry pose and anchor metadata, then walk/carry/restock tests.
6. Customers, queues, staff automation and station interactions.
7. Mobile-scale art cleanup and integration QA.


## APPROVED MASTER SCENE — Meow Fastfood (2026-10-21), version 3.0
This section overrides any conflicting example scene arrangement elsewhere in the skill. Reuse this **layout grammar** for Meow Mart, Meow Pizza, Meow Sushi and other restaurant/shop tycoon projects; adapt functional stations and furniture without silently redesigning the approved map.

### Camera and art
- Portrait **9:16** gameplay, fixed 2.5D isometric view matching Meow Pizza's reference screenshot; gameplay-size cats and counters, not an elaborate distant illustration.
- Large cream floor tiles, low two-wall corner at upper map, warm brown outlines, simplified products, minimal clutter. Keep screen-space HUD separate from world assets.
- New zones unlock progressively **downward and to the right**. Do not show a completely built restaurant at the start.

### Approved floor plan and movement
- **Upper-left:** one initial cooking/production station (Chicken in Fastfood), with its own production and interaction anchors. Subsequent Burger/Salad stations are separate modular additions. Stations may cook automatically, without dedicated chef characters.
- **Center-right:** long, low, open serving countertop, with clearly visible food waiting slots and a **cashier register section directly adjacent** on the same connected counter. **No raised menu board, tall divider, overhead partition, or wall** over the pickup surface.
- **Right side:** uninterrupted corridor leading to the next unlock area; never close it off with a counter, decoration, wall, or queue.
- **Lower-left:** modest dining area with a few tables and correctly positioned customer seats; add tables progressively. Keep a spacious central path between kitchen, pickup/cashier, dining and future zones.
- Each production station has its own **unique pickup slot and interaction anchor** (even if served on a visually connected long counter); bind food by order/station ID, never just nearest-item lookup.
- Keep walkable aisles approximately two character widths or more, test collision, queue points, cashier service point, waiter pickup/drop points, and cleaner approach to every table.

### Gameplay and staff
- Prioritize waiter and cleaner activity over many chef variants: cooking stations auto-produce; player manually serves at first, first useful staff (prefer waiter) unlocks by minute 5–6, absolutely no later than 7.
- Cashier, cleaner and additional waiters unlock as demand and dining area grow. Cleaner removes used trays and resets tables; avoid idle staff with no jobs.
- Provide meaningful unlocks, tasks and expansion for approximately 40 minutes; avoid extending play only with price inflation and waiting.

### Sprite invariants (apply across all games)
- **Direct back view:** tail stays stationary relative to torso through walk/carry frames, no wagging.
- Carry sprites show **empty gripping hands** and item attachment anchors; the food, box or tray is a separate runtime sprite.
- Character body and face orientation match travel direction; preserve clothes and correct head/tail/limb anatomy in front, side, 3/4 and back views.
- Eliminate micro-details illegible on 9:16 screens. Export modular station sprites, independent props and animation-ready character parts.

### Required QA before approving a reskin
1. Screenshot compare to approved layout: cooking upper-left, open low pickup plus adjacent cashier center-right, right corridor open, dining lower-left.
2. Remove all elevated menu partitions over pickup; keep items visibly accessible.
3. Test routes from every station to pickup, cashier, dining and expansion without collisions or accidental item selection.
4. Test carry empty-hand anchor attachment and correct facing in every travel direction; back-view tail must not move.
5. Confirm staff unlock before 7 minutes and play progression to ~40 minutes.

**Approval policy:** The final approved Meow Fastfood scene is a layout reference, not permission to copy unrelated restaurant signage, food, or decor into other games. Preserve spatial relationships and gameplay readability; reskin functionally.


## V4.0 — MEOW FASTFOOD DELIVERY LOCK (2026-10-21)
- **Absolute source of truth**: original user-approved Environment P1 artwork. Do NOT use later P1–P5 infographic maps as coordinates; they were rejected because Prep/Cashier/Pickup moved. Before integration obtain/identify P1 and explicitly lock pixel anchors from that image. Never guess missing coordinates.
- Keep the approved open cashier-plus-pickup assembly and separate customer interactions, without an overhead menu divider; wide aisle to next area. Expansion grows down/right while preserving ALL P1 object anchors.
- Dining furniture: exactly one fixed orientation square table and two chairs facing each other. Sitting sprites have NO chair/table or food baked in.
- Customer flow: customer queues at cashier, orders and pays, picks up prepared food and carries it to their own table; takeaway customers leave with their orders. Staff runner can move food to pickup; player can act as runner and cleaner.
- Cleaner/player: collect paper packaging and used trays and dispose into a separate trash bin. No table-wiping animation. Trash and bin are separate objects.
- Auto-cook station design reduces chef staffing; prioritize waiter/runner roles. Storage shelves, fridge, packaging, ingredient crates have Empty/Low/Half/Full visual states.
- Art: 9:16, 2.5D isometric 3/4, hand-drawn-clean edges, minimal noise, top-left light, export 2x gameplay size, plain background in reference sheets, transparent isolated PNG for production; no baked floor shadows.
- Character roster: player, cashier, gray food runner, cleaner, customers 01–04, VIP 01–02, manager. 8-direction idle, 4-frame right walk and role-specific actions. Stable tail; no protruding whiskers; approved facial silhouette. Manager checks tablet, not eat. VIP01 has no floor-length cape.
- This archive contains **reference sheets**, not automatically extracted production-ready transparent sprites. Crop, clean transparency, correct pivots, export and QA before runtime integration. All sheets are not individually verified approved; check the status manifest and compare with chat approvals.
