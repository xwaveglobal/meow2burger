# Meow Fastfood — Claude Handoff

1. Read MEOW_TYCOON_ART_ANIMATION_SKILL_v4.md.
2. Locate the original approved Environment P1 and lock all station anchors against it. Do not use the rejected P1–P5 diagrams.
3. Review MANIFEST.json and match the supplied reference sheets to the approved conversation versions. The images are reference atlases, not ready-to-use cut transparent sprites.
4. Split character poses and modular object components into individual transparent PNGs at 2x runtime size, assign anchors/pivots and validate directional consistency. Do not bake carried items or dining furniture into cats.
5. Implement order/pay at cashier -> wait -> pickup -> self-carry -> eat/leave; takeaway leaves with food. Player can run food and clean trash; auto cooking and staff automation unlock over a 40-minute progression.
6. Storage supplies the stations and packaging. Keep separate station item IDs and interaction anchors to avoid wrong pickups.
7. QA pathfinding, original P1 alignment, 2-chair seating, all character directions, tablet manager, and frame consistency.
