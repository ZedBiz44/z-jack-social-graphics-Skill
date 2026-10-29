# Reference-Based Prompt Template

Use actual supported image inputs. A filename written in a prompt is not a reference image. Build a compact prompt from the current request; do not turn process checks into a giant negative list.

## Choose the route

- **New scene:** use separately supplied environment, body, and face references for a genuinely new setting.
- **Office desk insertion:** use the supplied `office-main.png` as the sole base and layout authority; insert Jack into its existing chair rather than freely rebuilding or reframing the office.
- **Focused correction:** after one actual-input-supported attempt, make at most one correction for one precisely identified material defect through the same verified route.

Before a call, inspect current tool help and confirm actual image-input handling, input limit, generation or edit capability, output handling, and engine. If the tool cannot receive the required actual inputs, stop and report the gap. Do not promise pixel-exact generative preservation.

## Reference plan before the call

Resolve SKILL_ROOT to this agent's actual installed skill directory and expand these paths to real absolute files before the call.

Record the exact attached files, their actual order, and their roles. Select one layout authority; do not blend conflicting camera views. For the office desk test, attach only these three files in this order:

1. `{SKILL_ROOT}/assets/environments/office/office-main.png`: supplied office base and sole layout authority.
2. `{SKILL_ROOT}/assets/identity/jack-standing-pointing-front.png`: mature body build.
3. `{SKILL_ROOT}/assets/identity/jack-portrait-pointing.jpg`: facial identity.

Do not attach a retired office image, an occupied-office comparison, or an earlier generated office image. `jack-deck-bbq.png` is a task-specific non-office comparison only and is not an office control.

## Compact prompt pattern

```text
Create a [FORMAT / DIMENSIONS] 2D colorful comic-book caricature of Jack.

Environment: Input 1, [ENVIRONMENT FILE], is the single layout authority for the requested setting and camera.
Character: Inputs 2–3 preserve Jack's approved mature build, face, apparent age, eyes, smile, and goatee.
Attire: [REQUESTED ATTIRE.]
Pose: [REQUESTED ACTIVITY, HANDS, EXPRESSION, AND GAZE.]
ArtStyle: Bold clean black ink outlines, vibrant cel shading, rich saturated colors, and dynamic comic linework.
Lighting: [SCENE-APPROPRIATE LIGHTING.]
Layout requirements: [ONLY THE NECESSARY PHYSICAL RELATIONSHIPS, FRAMING, AND PROP COUNT.] Return [FORMAT / DIMENSIONS].
```

Use scene-appropriate sunlight, weather, and atmosphere. Do not force office lighting or architecture into BBQ, deck, pool, resort, or other scenes.

## Office desk test: compact exemplar

Use this only when the live tool has actually attached the three office desk-test files in the documented order.

```text
Edit Input 1, the supplied office base, by placing Jack in its existing chair. Return a 4:3 landscape 2D colorful comic-book caricature.

Environment: Input 1, office-main.png, is the supplied office base and sole camera/layout authority. Preserve its full original wide 4:3 view, desk shape, drawers, end panel, desk position, monitors, windows, railing, surrounding objects, and chair location.
Character: Inputs 2–3 preserve Jack's approved mature build, face, apparent age, eyes, smile, and goatee.
Attire: Solid black collared golf shirt and ZedBiz cap.
Pose: Jack is seated in the existing chair, faces and looks toward the camera, points naturally toward the camera with one hand, and places the other naturally on the mouse or desk.
ArtStyle: Draw Jack with bold clean black ink outlines, vibrant cel shading, rich saturated colors, and dynamic comic linework. Keep the office base rendering unchanged.
Lighting: Preserve the office's natural daytime lighting.
Layout requirements: Jack occupies the existing simple grey upholstered chair with pale curved arms and a pale five-spoke base. Do not replace it with a black mesh or modern metal chair; add no chair or desk; allow only natural body/hand occlusion and no body intersection with furniture. Return the full 4:3 landscape framing without crop or zoom.
```

Assess the actual output against the required relationships. A prompt cannot guarantee that every base-image pixel is preserved.

## Focused correction

```text
Correct only [ONE IDENTIFIED MATERIAL DEFECT] in the supplied first output. Preserve Jack's approved face and mature build, the requested attire and pose, the established camera/layout, and every unaffected element. Return [ACTUAL FORMAT / DIMENSIONS].
```

Do not use a prior generated red-shirt office image as a base. If identity or layout is broadly wrong, stop rather than redesigning the image through repeated edits or switching provider/engine without Jack's approval.
