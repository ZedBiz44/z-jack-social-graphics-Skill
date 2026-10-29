# Z Jack Social Graphics

This repository contains the public code and documentation source for `z-jack-social-graphics`, a ZedBiz skill for creating or revising graphics featuring Jack. It is **not** a complete private image package and contains no reference-image binaries.

[SKILL.md](SKILL.md) is the authoritative agent instruction file. This README, tests, and activity records are authoring material and are excluded from the installed package.

## When to use

Use for illustrations, avatars, banners, lifestyle scenes, promotional graphics, and other created graphics that need Jack in them. Preserve facial likeness and the approved illustrated style by default. Allow requested changes to pose, clothing, activity, setting, and an explicit style override.

Do not use merely to publish or work with an actual photograph Jack chooses to use. The skill does not authorize public posting, sharing changes, deleting or overwriting originals, new OAuth, new paid services, or agent deployment.

## Companion skills and operational sources

- `z-files-folders` governs current destination lookup, access boundaries, names, duplicates, uploads, and read-back checks.
- `z-agent-communication` governs human-facing wording.
- `z-ai-skill-developer` governs authorized development, validation, packaging, staged testing, and release approval.

See [the exact companion source records](references/companion-skills.md). The live [folder map](https://www.notion.so/386a3e33d58180ea96fbc50b60102fe2) and [Files & Folders Guide](https://www.notion.so/3a9a3e33d58180548f4af69e804dcdfc) determine file placement. The [Notion SOP](https://app.notion.com/p/407a3e33d58180ad8945dc54a67574aa) contains the human-readable procedure. The [overview](https://app.notion.com/p/407a3e33d5818178b80dc98f23fd5d8f) holds operational context.

## Reference images and safety

The repository is public and deliberately contains no identity or home reference images, secrets, credentials, account IDs, private Drive IDs, or private save receipts. A conforming private runtime payload contains exactly six active images:

- Four unchanged identity masters under `assets/identity/`.
- One and only one office image: `assets/environments/office/office-main.png`.
- One non-office character/style comparison: `assets/approved-scenes/jack-deck-bbq.png`.

`office-main.png` is the byte-identical private copy of the user-selected `CozyZedBizMountainLoftOffice.png` source. It is the sole office architecture, furniture, camera, and framing authority. No other office environment or occupied-office comparison belongs in the active runtime payload. Retired originals remain retained outside runtime rather than deleted and must never become public binaries.

The office-base rule applies only to office requests. BBQ and other settings use their own task-specific references and requirements. A downloaded code-only package is not generation-ready: supply the private payload through the approved private channel and verify it. Saving an output does not authorize changing an identity or environment master. Jack must approve master changes and wider installation.

## Validate and package

Run from the repository root:

```bash
python3 scripts/validate_skill.py --repository .
python3 -m unittest discover -s tests -v
python3 scripts/build_package.py --private-assets /approved/local/reference-payload --output-dir /approved/local/build-output
```

Only package a private payload that conforms to the six-image active-payload contract. Run the builder's `--help` for supported options. Omit `--private-assets` only to build a clearly labelled code-only package. The builder records the source commit, reference-manifest checksum, runtime file hashes, and ZIP checksum outside the installed skill folder.

Validate the built folder with the bundled validator and the target platform's current validator when available. The validator helper is reused from the recorded Z AI Skill Developer source. It requires a real YAML reader; do not replace that check with ad-hoc parsing.

## Real task testing and release

Use `assets/pilot-request.md` for a representative office desk test and the acceptance checks in `references/quality-checks.md`. Verify actual platform discovery, reference-image input, image generation, and upload/read-back through the executing agent's own connection. A local checker or package import alone is not a successful real task.

For an office test, use the documented ordered input sequence with `office-main.png` first, then the body and face references. Treat the task as placing Jack into the supplied office base: preserve the original wide 4:3 framing and required furniture relationships, but do not promise pixel-exact generative preservation. Make one actual-input-supported initial call and, only for one identified material defect, at most one focused correction. Include the executing agent's name in the internal output filename and retain its actual extension.

Keep changing rollout status in authoring activity records and Notion, not in runtime instructions. The offline helpers do not call image providers or Drive. Their successful checks cannot prove that an image was generated, visually inspected, uploaded, or accessible to another agent.
