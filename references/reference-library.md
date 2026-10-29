# Private Reference Library

The repository contains instructions and a checksum manifest, not public image payloads. Use approved files only through an authorized private task. Keep originals unchanged.

## Original eight references

The existing original names, roles, extensions, and manifest hashes remain unchanged.

### Jack identity

- `assets/identity/jack-portrait-arms-crossed.jpg` — close facial identity and illustrated treatment.
- `assets/identity/jack-portrait-pointing.jpg` — close facial identity and illustrated treatment.
- `assets/identity/jack-standing-pointing-front.png` — full-body mature Jack build and front-facing proportions.
- `assets/identity/jack-standing-pointing-relaxed.jpg` — full-body mature Jack build and relaxed proportions.

Use a close portrait and a full-body image together when the tool supports the needed input count. The current request controls only the requested attire, pose, activity, expression, gaze, scene, lighting, and framing; it never authorizes changing Jack's face or build. A portrait's pointing, crossed arms, plaid, or clothing is not a standing instruction.

### Office environment

- `assets/environments/office/office-main-desk.webp` — primary desk view; chair/workstation relationship and camera for seated desk requests.
- `assets/environments/office/office-wide-loft.png` — wide room layout and standing-scene context.
- `assets/environments/office/office-hallway-reverse.png` — reverse-view real layout reference.
- `assets/environments/office/office-desk-closeup.png` — workstation details.

Choose one layout authority. Do not combine these views into an invented camera or use stylized screen/exterior details as real geometry. For other scenes, use their relevant environment references; office geometry does not apply to a deck, pool, BBQ, or resort.

## Approved scene comparison examples

The following private paths are approved scene/style/build comparison examples. Their availability is tracked privately with the approved payload, manifest, and verifier process; they do not alter the original eight reference entries or hashes.

- `assets/approved-scenes/jack-office-mouse-mug.png` — approved seated office build, occupied-chair relationship, and hand-on-mouse reference.
- `assets/approved-scenes/jack-office-seated-mug.png` — approved seated office build and alternate natural hand placement.
- `assets/approved-scenes/jack-deck-bbq.png` — approved Jack build/style in a green Riders shirt at a BBQ.

These are not permanent identity masters, automatic generation inputs, or permission to promote later outputs. Use them for visual comparison after a new-scene attempt, or as a compatible edit base only when the request and verified edit tool support that route. Jack alone approves permanent-master changes.

## Required reference discipline

- Pass image bytes through the live tool's supported image inputs; written paths, filenames, and descriptions do not count.
- Record each call's exact input order and assigned role. Describe “environment first, character last” only when that is how the call was actually made.
- Use a single primary environment view for camera and structure. Supplemental inputs may supply a detail, not contradict the primary view.
- For a new Jack scene, use real environment, body, and face inputs. If the actual tool cannot receive the required inputs, stop instead of making a generic substitute.
- Use an approved scene as visual QA only unless it is explicitly the passed edit base. Do not feed multiple approved scenes as competing layout controls.

## First new-scene Terry test

Subject to live-tool support for all three supplied image inputs, use this order and no invented reorder:

1. `assets/environments/office/office-main-desk.webp` — primary layout; it includes the empty existing chair.
2. `assets/identity/jack-standing-pointing-front.png` — Jack's body build.
3. `assets/identity/jack-portrait-pointing.jpg` — Jack's facial identity.

Compare the result visually with the approved seated office examples after generation. Those comparison files do not become scene-control generation inputs for this test.

## Integrity and privacy

`assets/reference-manifest.json` and `scripts/verify_reference_assets.py` check locally supplied private files; they do not prove visual quality or tool attachment. Never place image binaries, base64 payloads, private download links, account details, or private folder IDs in the public repository or public status records. New outputs are outputs, not masters, and preserve their actual extension.
