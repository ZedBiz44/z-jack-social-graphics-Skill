# Z Jack Social Graphics

This repository contains the authoritative technical source for `z-jack-social-graphics`, a ZedBiz skill that creates or revises any graphic featuring Jack and automatically saves completed results to the approved Shared Drive home.

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

The repository is public and deliberately contains no identity or home reference images, secrets, credentials, account IDs, private Drive IDs, or private save receipts. A private package adds the eight approved images listed in [the reference-library contract](references/reference-library.md) and `assets/reference-manifest.json`.

A downloaded code-only package is not generation-ready. Supply the private payload through the approved private channel and verify it. Saving an output does not authorize changing a reference master. Jack must approve master changes and wider installation.

## Validate and package

Run from the repository root:

```bash
python3 scripts/validate_skill.py --repository .
python3 -m unittest discover -s tests -v
python3 scripts/build_package.py --private-assets /approved/local/reference-payload --output-dir /approved/local/build-output
```

The private payload directory contains the `assets/identity/` and `assets/environments/office/` paths expected by the manifest. Run the builder's `--help` for supported options. Omit `--private-assets` only to build a clearly labelled code-only package. The builder records the source commit, reference-manifest checksum, runtime file hashes, and ZIP checksum outside the installed skill folder.

Validate the built folder with the bundled validator and the target platform's current validator when available. The validator helper is reused from the recorded Z AI Skill Developer source. It requires a real YAML reader; do not replace that check with ad-hoc parsing.

## Real task testing and release

Use `assets/pilot-request.md` for a representative test and the acceptance checks in `references/quality-checks.md`. Verify actual platform discovery, reference-image input, image generation, and upload/read-back through that agent's own connection. A local checker or package import alone is not a successful real task.

Test one agent, present the result to Jack, and obtain approval before wider installation. Install only the exact tested source-linked package. Keep changing rollout status in authoring activity records and Notion, not in runtime instructions.

The offline helpers do not call image providers or Drive. Their successful checks cannot prove that an image was generated, visually inspected, uploaded, or accessible to another agent.
