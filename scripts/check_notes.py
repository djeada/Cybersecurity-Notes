"""Check repository Markdown offline, using the standard library only."""

from collections import Counter
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
HEADING = re.compile(r"^ {0,3}(#{1,6})\s+(.+?)\s*#*\s*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
INLINE_LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)")
REFERENCE = re.compile(r"^ {0,3}\[[^\]]+\]:\s*(<[^>]+>|\S+)")


def prose_lines(content):
    """Return lines outside fenced code, and any unclosed fence line number."""
    lines = []
    fence = None
    for number, line in enumerate(content.splitlines(), 1):
        marker = FENCE.match(line)
        if fence:
            if (marker and marker[1][0] == fence[0]
                    and len(marker[1]) >= fence[1] and not marker[2].strip()):
                fence = None
            continue
        if marker:
            fence = (marker[1][0], len(marker[1]), number)
        else:
            lines.append((number, line))
    return lines, fence[2] if fence else None


def heading_anchors(lines):
    """Generate GitHub-style anchors, including repeated heading suffixes."""
    anchors = set()
    counts = Counter()
    for _, line in lines:
        heading = HEADING.match(line)
        if not heading:
            continue
        label = re.sub(r"!?\[([^]]+)\]\([^)]*\)", r"\1", heading[2])
        label = re.sub(r"<[^>]*>", "", label).lower()
        slug = re.sub(r"[^\w\- ]", "", label).replace(" ", "-")
        anchor = slug
        while anchor in anchors:
            counts[slug] += 1
            anchor = f"{slug}-{counts[slug]}"
        anchors.add(anchor)
    return anchors


def check_repository(root=ROOT):
    root = Path(root).resolve()
    documents = {}
    errors = []
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if any(part.startswith(".") or part == "__pycache__" for part in relative.parts):
            continue
        lines, unclosed = prose_lines(path.read_text(encoding="utf-8"))
        documents[path] = (lines, heading_anchors(lines))
        titles = [line for _, line in lines if re.match(r"^#\s+", line)]
        if len(titles) != 1:
            errors.append(f"{relative}: expected one level-one title, found {len(titles)}")
        if unclosed:
            errors.append(f"{relative}:{unclosed}: unclosed code fence")

    checked_links = 0
    for path, (lines, _) in documents.items():
        for number, line in lines:
            # Inline code can contain literal Markdown syntax or example paths.
            line = re.sub(r"(`+).*?\1", "", line)
            destinations = [m[1] for m in INLINE_LINK.finditer(line)]
            definition = REFERENCE.match(line)
            if definition:
                destinations.append(definition[1])
            for destination in destinations:
                destination = destination.strip("<>")
                parts = urlsplit(destination)
                if parts.scheme or parts.netloc:
                    continue
                checked_links += 1
                target = ((root if parts.path.startswith("/") else path.parent)
                          / unquote(parts.path).lstrip("/")).resolve() if parts.path else path
                location = f"{path.relative_to(root)}:{number}"
                if not target.is_relative_to(root):
                    errors.append(f"{location}: link leaves repository: {destination}")
                    continue
                if not target.exists():
                    errors.append(f"{location}: missing target: {destination}")
                    continue
                if target.is_dir():
                    target = target / "README.md"
                if parts.fragment and target.suffix.lower() == ".md":
                    if target not in documents:
                        errors.append(f"{location}: cannot check Markdown anchor: {destination}")
                    elif unquote(parts.fragment) not in documents[target][1]:
                        errors.append(f"{location}: missing heading anchor: {destination}")
    return errors, len(documents), checked_links


def main():
    errors, count, links = check_repository()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Checked {count} Markdown files and {links} local links: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
