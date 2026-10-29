# Quality and Test Checks

A generated image is not accepted merely because the tool returned a file. Compare it visually against the actual input references and request before saving it as a completed output. Report observed pass/fail facts, not self-congratulation.

## Capability and call record

Before the initial attempt, record privately:

- The executing agent, actual image engine, and separate conversation model when applicable.
- Current tool-help evidence for supported image inputs, generation or editing, input limit, and output handling.
- The exact image files actually attached, in actual order, with environment, body, face, prop, comparison, or edit-base role.
- The selected single primary layout view and any request-specific physical relationship that must hold.

A skill creator, package import, model name, file path, or another agent's working route does not prove this agent can pass images, generate a new scene, edit an image, or save a binary.

## General visual acceptance

Reject the initial image unless all applicable checks pass:

- Jack matches the approved face and mature body build: face/head shape, apparent age, eyes, smile, goatee, shoulder width, torso/waist, and natural proportions.
- The requested activity, attire, pose, gaze, props, text, framing, setting, and scene-specific lighting are correct. Reference-image clothing or poses do not survive unless requested.
- The chosen primary view controls the camera and major scene geometry. There is no contradictory blended camera or invented major layout.
- Jack's body is physically supported where the activity requires it. Hands, limbs, object contact, and occlusion are credible.
- No solid object visibly intersects Jack's torso, stomach, arms, or legs. Normal foreground occlusion is allowed; impossible intersection is not.
- The 2D colorful comic-book caricature treatment is coherent: bold clean black ink outlines, vibrant cel shading, rich saturated colors, and dynamic comic linework, unless Jack explicitly changed style.
- No unrequested people, furniture, props, signs, claims, labels, or brand marks appear. Format and dimensions are correct.

## Request-specific desk test

Apply these only to the Terry red-golf-shirt office test, not to non-office scenes:

- Compare identity/build with the passed body and face references and approved seated office comparisons.
- Confirm `office-main-desk.webp` supplied the requested camera, desk, monitor arrangement, and working side.
- Jack is in exactly one existing occupied chair at the actual working side of the desk; no extra empty chair or rebuilt desk is visible.
- The chair visibly supports a naturally seated Jack. The desk edge does not cut through his torso or stomach.
- He wears a solid red collared golf shirt, looks toward the camera, and points naturally toward the camera with credible anatomy.
- Reject a wrong working-side occupancy, wrong desk/layout, changed face/build, or any extra chair/desk even if other details look attractive.

## Correction boundary

Allow **one** initial output and, only if a single material defect is precisely identified, **one** focused correction. Recheck the entire acceptance list after that correction.

Stop rather than retrying when identity or scene layout is broadly wrong, the output uses the wrong primary view, the tool cannot provide required inputs, or the focused correction still fails. Do not quietly use a different provider or engine; that is a separate, unvalidated route requiring Jack's approval.

## Save acceptance

Only a visually accepted image proceeds to the approved save process. Verify the returned file ID and read back name, parent ancestry, Shared Drive, image type/size, intended dimensions, usable image content, and link through the executing agent's approved connection.

The filename must contain the executing agent's friendly name (for example, `Terry`), a clear topic, date, version, and the actual file extension. Preserve rejected attempts privately without calling them finished graphics or overwriting originals. If saving or read-back fails, report the local file as `not-saved`; do not claim completion.

Run only Jack-authorized tests. One Terry result, with the actual engine/reference record and visual findings, is required before any wider agent rollout.
