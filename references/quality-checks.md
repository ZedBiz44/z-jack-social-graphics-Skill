# Quality and Test Checks

A generated image is not accepted merely because a tool returned a file. Compare it visually against the actual input references and the request before saving it as a completed output. Report observed pass/fail facts and any remaining material limitation.

## Capability and call record

Before the initial attempt, record privately:

- The executing agent, actual image engine, and separate conversation model when applicable.
- Current tool-help evidence for supported image inputs, generation or editing, input limit, and output handling.
- The exact image files actually attached, in actual order, with their base, body, face, prop, comparison, or edit-base role.
- The selected sole layout authority and the request-specific physical relationships that must hold.

A file path, prompt, agent name, skill creator, package import, or model name does not prove that this agent can attach images, generate or edit an image, or save a binary.

## General visual acceptance

Reject the initial image unless all applicable checks pass:

- Jack matches the approved face and mature body build: face/head shape, apparent age, eyes, smile, goatee, shoulder width, torso/waist, and natural proportions.
- The requested activity, attire, pose, gaze, props, text, framing, setting, and scene-appropriate lighting are correct.
- The declared primary view controls camera and major scene geometry. There is no contradictory blended camera or invented major layout.
- Jack is physically supported where the activity requires it. Hands, limbs, object contact, and natural foreground occlusion are credible.
- No solid object visibly intersects Jack's torso, stomach, arms, or legs. Natural body/hand occlusion is allowed; impossible intersection is not.
- The 2D colorful comic-book caricature treatment is coherent: bold clean black ink outlines, vibrant cel shading, rich saturated colors, and dynamic comic linework, unless Jack explicitly changed the style.
- No unrequested people, furniture, props, signs, claims, labels, or brand marks appear. The returned format and dimensions are correct.

## Office desk test: request-specific acceptance

Apply these checks only when an office desk image is requested; use task-specific checks for BBQ and other non-office scenes.

- Confirm that the actual attached inputs were, in order, `office-main.png` as base, `jack-standing-pointing-front.png` as body build, and `jack-portrait-pointing.jpg` as facial identity. Reject a call that substituted a retired office image, occupied-office comparison, or prior generated office output.
- Confirm that `office-main.png` remains the sole authority for the full original wide 4:3 view, office camera, and framing.
- Confirm the desk shape, drawers, end panel, position, monitors, windows, railing, surrounding objects, and chair location remain as the supplied base presents them.
- Confirm Jack occupies the one existing simple grey upholstered chair with pale curved arms and a pale five-spoke base. Reject a black mesh/modern metal replacement, an empty retained chair, an added chair, or an added/rebuilt desk.
- Confirm that the chair visibly supports a naturally seated Jack and that the desk or other furniture does not intersect his torso, stomach, arms, or legs.
- Confirm the current request's attire, cap, gaze and pose. The black-shirt pilot uses a solid black collared golf shirt, ZedBiz cap, camera-facing gaze, a natural point toward camera, and the other hand on the mouse or desk; these pilot choices are not permanent wardrobe or pose defaults.
- Assess substantive visual preservation of the supplied base, but do not claim pixel-exact generative preservation.

Reject a wrong working-side occupancy, changed camera/framing, wrong desk/chair relationship, changed face/build, extra furniture, or material body intersection even if other details look attractive.

## Correction boundary

Allow one actual-input-supported initial output and, only if one material defect is precisely identified, at most one focused correction through the same verified route. Recheck the whole acceptance list after that correction.

Stop rather than retrying when identity or layout is broadly wrong, the output uses the wrong base, the tool cannot provide required inputs, or the focused correction still fails. Do not quietly use a different provider or engine; that is a separate route requiring Jack's approval.

## Save acceptance

Only a visually accepted image proceeds to the authorized save process. Verify the returned file identifier and read back the actual filename, parent/location where applicable, image type and size, intended dimensions, usable image content, and link through the executing agent's approved connection.

The filename must contain the executing agent's friendly name, a clear topic, date, version, and the actual file extension. For example, a PNG saved by Terry may be named `jack-desk-black-golf-pointing-terry-2026-10-28-v03.png`; use the actual returned format rather than forcing `.png`. Preserve rejected attempts privately without calling them finished graphics or overwriting originals. If saving or read-back fails, report the local file as `not-saved`; do not claim completion.
