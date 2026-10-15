# Contributing

## Keep notes useful and easy to find

- Give each Markdown file one descriptive level-one heading.
- Use lowercase names with underscores for topic files and `README.md` for indexes.
- Link new topics from [the notes index](notes/README.md), or the relevant tool or
  walkthrough index. Update incoming links whenever a path changes.
- Explain concepts before commands. Distinguish a lab example from deployment
  guidance, and identify the relevant version or platform when behavior varies.
- Use descriptive relative links for repository content. Cite primary sources
  for security recommendations and check that they support the specific claim.
- Keep historical algorithms and protocols clearly labeled; do not present them
  as suitable choices for new systems.
- Use placeholders for secrets and personal data. Keep examples within authorized
  lab scope and state prerequisites and observable outcomes.

## Suggested note format

````markdown
# Topic

A short definition and why the topic matters.

## Core concepts

Explain the terms and important distinctions.

## Practical example

State the prerequisites, steps, expected result, and limitations.

## Related notes

- [Related topic](relative_path.md)

## Sources

- [Primary source title](https://example.org/documentation)
````

## Validate changes

From the repository root, with Python 3.10 or newer:

```bash
python scripts/check_notes.py
python -m unittest discover -s tests -v
```

The documentation check covers local links and heading anchors, a single document
title, and balanced code fences. External links need a separate source review;
the check deliberately runs offline. Tests cover the repaired Python examples.

Before submitting, review `git diff --check` and the rendered Markdown. For a
factual change, explain the corrected behavior and cite the supporting source.
