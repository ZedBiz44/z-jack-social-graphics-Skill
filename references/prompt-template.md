# Reference-Based Prompt Template

Use actual image inputs. A filename in text is not a visual reference. Fill only the fields needed for the request; do not force the user to complete a form.

## Generation brief

```text
Create a [FORMAT / ASPECT RATIO / DIMENSIONS] graphic featuring the SAME Jack shown in the supplied CHARACTER REFERENCES.

SCENE: [ACTIVITY] at [SETTING]. Use the supplied ENVIRONMENT REFERENCES as ground truth for [ARCHITECTURE / LAYOUT / MAJOR OBJECT RELATIONSHIPS]. Render the environment in the requested illustration style; do not replace the real geometry with invented scenery.

IDENTITY: Preserve Jack's recognizable face/head shape, expressive bright blue eyes, mature late-50s appearance, warm smile, and short white/salt-and-pepper goatee. Use the portrait for facial identity and a full-body reference for natural proportions when relevant. Do not inflate muscles, smooth away age, or substitute a generic man.

STYLE: [Default: polished colorful 2D comic illustration, clean black ink outlines, vibrant refined cel shading, rich natural colors, warm light. Replace only if the user explicitly requested another style.] Apply one coherent treatment to Jack and the background while retaining facial likeness.

WARDROBE: [CAP, SHIRT, TROUSERS/SHORTS, FOOTWEAR]. Default grey cap with readable blue ZedBiz lettering unless overridden. POSE: [BODY POSITION, HANDS, GAZE]. PROPS: [OBJECTS AND HOW USED]. LIGHT: [TIME, SEASON, WEATHER, MOOD]. COMPOSITION: [VIEWPOINT, SUBJECT PLACEMENT, FRAMING]. TEXT: [Only exact requested wording or required brand marks].

The current pose and clothing override what the character references show. Do not carry over pointing, crossed arms, or plaid unless requested. Keep credible hands and object handling. Avoid unrelated people/props/signs, invented labels/claims, facial drift, and an unrequested style change.
```

## Reference priority

The current request controls activity, attire, pose, scene, and composition. Character images control likeness, portrait style anchors control default treatment, real environment photos control geometry, and prop photos control equipment. Select the relevant files within the provider's actual image-input limit.

## Focused revision

```text
Edit the supplied generated graphic to fix [ONE MATERIAL FAILURE]. Preserve Jack's approved facial identity and all already-correct [STYLE / COMPOSITION / CLOTHING / SCENE / TEXT]. Use the supplied relevant references for the correction. Do not redesign or change unrelated elements. Return [FORMAT / DIMENSIONS].
```

Verify required wording in the result. If critical branding remains wrong after the targeted correction, report that failure instead of claiming the graphic passed.
