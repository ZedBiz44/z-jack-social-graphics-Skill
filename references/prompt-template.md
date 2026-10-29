# Reference-Based Prompt Template

Use actual supported image inputs. A filename written in a prompt is not an image reference. Build a compact prompt from the current request; do not turn process checks into a giant negative list.

## Choose the route

- **New scene (core route):** create the requested scene from separately supplied environment, body, and face references. This route is required for genuinely new scenes and must not be replaced by an edit-only workflow.
- **Compatible-scene edit (optional):** use one approved scene as the edit base only for a small requested change when the live tool confirms it can edit that image. It is not a prerequisite for new-scene work.
- Before either route, read current tool help. Confirm actual image-input handling, image generation or edit capability, input limit, and the engine used. Do not assume masks, reference strength, preservation controls, or model names.

## Reference plan before the call

Record the actual files passed, in their actual call order, and their roles. An ordered list is valid only when those exact image bytes are supplied in that same call.

1. Select **one primary layout view**. It controls viewpoint, camera, major geometry, and physical relationships.
2. Supply a full-body Jack reference for mature shoulder, torso, waist, and seated/standing proportions.
3. Supply a close facial Jack reference for face, head shape, apparent age, eyes, smile, and goatee.
4. Add only compatible supporting references within the real tool limit. Do not mix competing camera views into a blended layout.
5. Keep approved-scene comparison images out of new-scene layout control unless the tool call and request explicitly use one as an edit base.

If the tool cannot accept the needed actual inputs, stop and report the capability gap. Do not substitute a generic textual description of Jack.

## New-scene prompt

```text
Create a [FORMAT / ASPECT RATIO / DIMENSIONS] 2D digital colorful comic-book caricature of Jack: [OVERALL SCENE AND ACTIVITY].

INPUT ROLES — only if these exact images are attached in this order:
1. [ENVIRONMENT FILE] — primary layout, camera, architecture, and major object relationships.
2. [JACK BODY FILE] — mature Jack body build and natural proportions.
3. [JACK FACE FILE] — Jack's facial identity, apparent age, eyes, smile, and goatee.
[Add an actual compatible input only when supplied.]

LAYOUT: Use input 1 as the single camera/layout authority. [REQUEST-SPECIFIC PHYSICAL RELATIONSHIP OR COUNT.] Do not blend a conflicting camera view.

JACK: Keep the approved face and mature build shown in inputs 2–3. [ATTIRE.] [POSE / ACTIVITY / HANDS / GAZE.] The current request changes only the requested pose, clothing, activity, expression, framing, or props; it does not change his face or build.

STYLE: Bold, clean black ink outlines; vibrant cel shading; rich saturated colors; dynamic comic linework. [SCENE-APPROPRIATE LIGHTING.] Apply the coherent treatment to Jack and the scene.

[ONLY NECESSARY REQUEST-SPECIFIC PROP, TEXT, OR STRUCTURAL REQUIREMENT.] Return [FORMAT / DIMENSIONS].
```

Use sunlight, time of day, weather, and atmosphere appropriate to the requested scene; do not force office or timber lighting into pool, BBQ, deck, or other scenes.

## First Terry desk test: compact exemplar

Use this exact ordered list only if Terry's live tool has actually attached all three files: `office-main-desk.webp`, `jack-standing-pointing-front.png`, and `jack-portrait-pointing.jpg`.

```text
Create a 2D digital colorful comic-book caricature of Jack seated at his office desk, red collared golf shirt, looking toward the camera and naturally pointing toward the camera. Input 1, office-main-desk.webp, is the single primary layout view: use its desk, monitor arrangement, camera, and existing chair position. Input 2, jack-standing-pointing-front.png, controls Jack's mature shoulder, torso, waist, and body build. Input 3, jack-portrait-pointing.jpg, controls his face, apparent age, eyes, smile, and goatee.

Jack occupies the one existing chair at the working side of the desk; the chair supports him naturally. Keep exactly that occupied chair, no extra desk or chair, and keep the desk edge out of his torso and stomach. Use bold clean black ink outlines, vibrant cel shading, rich saturated colors, dynamic comic linework, and office-appropriate daylight. Keep the face/build from the Jack references, credible hand anatomy, and the requested camera view. Return [FORMAT / DIMENSIONS].
```

`jack-office-mouse-mug.png` or `jack-office-seated-mug.png` may be used afterward as visual comparison only; do not present either as a new-scene control image unless it was actually passed as one.

## Optional focused edit

```text
Edit the supplied compatible approved scene [BASE FILE]. Preserve the approved Jack face, mature build, camera, layout, and all unchanged parts. Change only [ONE REQUESTED SMALL CHANGE]: [EXACT CHANGE]. Keep [REQUEST-SPECIFIC RELATIONSHIP / ATTIRE / GAZE]. Return [FORMAT / DIMENSIONS].
```

Use one initial output and, only for one clearly identified material defect, one focused correction. If identity or layout is broadly wrong, stop rather than redesigning through repeated edits. Do not switch provider or image engine without Jack's explicit approval.
