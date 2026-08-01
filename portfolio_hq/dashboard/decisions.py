"""Governance Decision Explorer — data model, two-ledger resolution, and a
small, dependency-free Markdown-to-HTML renderer for committed governance
decision records (OPS-0013).

Every ``governance/decisions/*.md`` file is treated as **untrusted display
input** (OPS-0013 section 5): this module never emits raw HTML from decision
content, only HTML-escaped text passed through an explicit allow-list of
structural/inline transforms (see ``_inline`` and ``_block_to_html`` below).

Two ledgers are resolved, never conflated:
  * ``governance/decisions/*.md`` + ``governance/decisions.yaml`` — the
    current, substantive record (frontmatter controls on any mismatch with
    the generated index — see ``README.md`` in that directory).
  * ``decision_log.yaml`` — the historical, pre-``GOV-0001`` ledger for
    ``MARGIN-####``/``PI-0001``-``PI-0009``. Its own status vocabulary
    (``pending_evidence``/``active``/``accepted``) is never mapped onto the
    newer ``Proposed``/``Accepted``/``Superseded``/``Archived`` vocabulary.

``related_decisions`` is an untyped list (OPS-0013 section 4): this module
never infers ``implements``/``narrows``/``supersedes``/etc. Reverse
references are built only from that structured field and are always labeled
"References this decision" — never a stronger claim the source text does not
make. Supersession is never inferred from an ID or a date.

Purely additive: this module has no effect on ``model.DecisionRow`` or any
existing consumer of it.
"""

from __future__ import annotations

import hashlib
import html
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

DECISIONS_DIR_REL = "governance/decisions"
DECISIONS_INDEX_REL = "governance/decisions.yaml"
DECISION_LOG_REL = "decision_log.yaml"
README_NAME = "README.md"

# Hard-denied evidence path (OPS-0013 section 11, restated verbatim per this
# repository's "restate hard boundaries as standalone text" discipline) —
# never read, listed, hashed, or exposed by any dashboard path.
SEALED_DATA_PREFIX = "research/margin_target_study/data/untouched_sealed/"

SEVERITY_WARNING = "warning"
SEVERITY_ERROR = "error"

# governance/decisions/README.md's own documented status vocabulary.
KNOWN_STATUSES = frozenset({"Proposed", "Accepted", "Superseded", "Archived"})

_ID_TOKEN = re.compile(r"^[A-Z][A-Z0-9]*-\d{4}(?:-\d{2})?$")
_ID_MENTION_RE = re.compile(r"\b[A-Z][A-Z]{1,9}-\d{4}(?:-\d{2})?\b")
_FILENAME_ID_RE = re.compile(r"^([A-Z][A-Z0-9]*-\d{4}(?:-\d{2})?)-(.+)\.md$")
_FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?(.*)\Z", re.S)


# ── data records ─────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class LoadIssue:
    severity: str
    code: str
    message: str


@dataclass(frozen=True)
class DecisionSource:
    path: str  # repo-relative
    exists: bool
    sha256: str | None
    size_bytes: int | None


@dataclass(frozen=True)
class SupportingArtifact:
    declared_path: str
    safe: bool
    exists: bool
    sha256: str | None
    size_bytes: int | None
    warning: str | None


@dataclass(frozen=True)
class RelatedRef:
    decision_id: str
    kind: str  # "governance" | "legacy" | "unresolved"


@dataclass(frozen=True)
class LegacyDecision:
    """One decision_log.yaml entry — the historical, pre-GOV-0001 ledger.
    Status/category/vocabulary are preserved literally, never remapped."""

    decision_id: str
    date: str | None
    status: str | None
    category: str | None
    decision_text: str | None
    rationale: str | None
    supporting_artifact: str | None


@dataclass(frozen=True)
class DecisionDetail:
    decision_id: str
    title: str
    title_source: str  # "frontmatter" | "h1" | "filename" | "id"
    date: str | None
    status: str | None  # literal frontmatter value, displayed as-is
    category: str | None
    related: tuple[RelatedRef, ...]
    reverse_references: tuple[str, ...]
    supporting_artifact: SupportingArtifact | None
    source: DecisionSource
    body_html: str
    body_empty: bool
    issues: tuple[LoadIssue, ...]
    indexed: bool  # a governance/decisions.yaml row exists for this ID
    index_mismatches: tuple[str, ...]
    duplicate_id: bool
    orphan: bool  # file on disk, no index row
    source_missing: bool  # indexed, but the file it points to is absent


@dataclass(frozen=True)
class DecisionCatalog:
    decisions: tuple[DecisionDetail, ...]
    legacy: tuple[LegacyDecision, ...]
    valid_ids: frozenset  # governance decision IDs — the autolink/route allow-list
    legacy_ids: frozenset
    issues: tuple[LoadIssue, ...]  # catalog-level (malformed index, etc.)


# ── small filesystem/hash helpers ───────────────────────────────────────────

def _hash_file(path: Path) -> tuple[str | None, int | None]:
    try:
        data = path.read_bytes()
    except OSError:
        return None, None
    return hashlib.sha256(data).hexdigest()[:12], len(data)


def _safe_load_yaml_text(text: str) -> tuple[object, str | None]:
    try:
        return yaml.safe_load(text), None
    except yaml.YAMLError as exc:
        return None, str(exc)


# ── frontmatter / body split ────────────────────────────────────────────────

def _split_frontmatter(text: str) -> tuple[dict | None, str, str | None]:
    """Returns (frontmatter_dict_or_None, body, error). ``body`` is always the
    best-effort separable remainder — empty string if no delimiters were
    found at all (nothing was safe to separate)."""
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return None, "", "missing or malformed frontmatter delimiters (--- ... ---)"
    fm_text, body = m.group(1), m.group(2)
    data, err = _safe_load_yaml_text(fm_text)
    if err:
        return None, body, f"frontmatter YAML parse error: {err}"
    if not isinstance(data, dict):
        return None, body, "frontmatter is not a mapping"
    return data, body, None


# ── title derivation ─────────────────────────────────────────────────────────

def _slugify_title_word(word: str) -> str:
    return word[:1].upper() + word[1:] if word else word


def _title_from_filename(filename: str, decision_id: str) -> str | None:
    m = _FILENAME_ID_RE.match(filename)
    if not m:
        return None
    slug = m.group(2)
    words = [w for w in slug.split("-") if w]
    if not words:
        return None
    return " ".join(_slugify_title_word(w) for w in words)


_H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.M)


def _derive_title(*, frontmatter: dict | None, body: str, filename: str,
                   decision_id: str) -> tuple[str, str]:
    """Returns (title, title_source). Tier order per OPS-0013 implementation
    instructions: frontmatter title (future) -> first body H1 (future) ->
    filename slug (current corpus) -> decision ID alone."""
    if frontmatter:
        t = frontmatter.get("title")
        if isinstance(t, str) and t.strip():
            return t.strip(), "frontmatter"
    h1 = _H1_RE.search(body) if body else None
    if h1:
        candidate = h1.group(1).strip()
        if candidate:
            return candidate, "h1"
    from_name = _title_from_filename(filename, decision_id)
    if from_name:
        return from_name, "filename"
    return decision_id, "id"


# ── supporting-artifact resolution ──────────────────────────────────────────

def _resolve_artifact(repo_root: Path, declared: str) -> SupportingArtifact:
    raw = declared.strip()
    norm = raw.replace("\\", "/")
    if not norm or norm.startswith("/") or "://" in norm:
        return SupportingArtifact(raw, False, False, None, None,
                                   "absolute or external path rejected")
    parts = norm.split("/")
    if ".." in parts:
        return SupportingArtifact(raw, False, False, None, None,
                                   "path traversal rejected")
    if norm == SEALED_DATA_PREFIX.rstrip("/") or norm.startswith(SEALED_DATA_PREFIX):
        return SupportingArtifact(raw, False, False, None, None,
                                   "sealed evidence path — access denied by policy "
                                   "(OPS-0013 section 11)")
    root = repo_root.resolve()
    target = (root / norm).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        return SupportingArtifact(raw, False, False, None, None,
                                   "path escapes repository root — rejected")
    if not target.exists():
        return SupportingArtifact(raw, False, False, None, None, "artifact not found")
    if target.is_dir():
        return SupportingArtifact(raw, False, True, None, None,
                                   "directory reference — not enumerated")
    sha, size = _hash_file(target)
    if sha is None:
        return SupportingArtifact(raw, False, True, None, None, "hash unavailable")
    return SupportingArtifact(raw, True, True, sha, size, None)


# ── Markdown -> safe HTML renderer ──────────────────────────────────────────
#
# Order (matches OPS-0013's required conceptual order exactly):
#   1. frontmatter already separated by the caller.
#   2. block-level parse (line/state-machine).
#   3. fenced code blocks extracted as opaque content.
#   4. inline code spans extracted as opaque content (per inline text run).
#   5. code content HTML-escaped.
#   6. remaining raw text HTML-escaped.
#   7. allow-listed transforms applied to already-escaped non-code text.
#   8. escaped code spans restored.
#   9. wrapped with explicit structural HTML tags.

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
_UL_ITEM_RE = re.compile(r"^( *)[-*+]\s+(.*)$")
_OL_ITEM_RE = re.compile(r"^( *)\d+[.)]\s+(.*)$")
_HR_RE = re.compile(r"^ {0,3}(?:-{3,}|\*{3,}|_{3,})\s*$")
_FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})\s*([\w+-]*)\s*$")
_TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)*\|?\s*$")

_INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
_BOLD_RE = re.compile(r"(\*\*|__)(?!\s)(.+?)(?<!\s)\1")
_ITALIC_RE = re.compile(r"(?<!\*)\*(?!\*)(?!\s)([^*\n]+?)(?<!\s)\*(?!\*)")


def _split_table_row(line: str) -> list[str] | None:
    """Split a table row on unescaped pipes that are not inside a backtick
    code span. Returns None if the row has an unterminated code span
    (ambiguous — caller should fall back to literal rendering)."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells: list[str] = []
    buf: list[str] = []
    in_code = False
    i, n = 0, len(s)
    while i < n:
        ch = s[i]
        if ch == "`":
            in_code = not in_code
            buf.append(ch)
            i += 1
            continue
        if ch == "\\" and i + 1 < n and s[i + 1] == "|":
            buf.append("|")
            i += 2
            continue
        if ch == "|" and not in_code:
            cells.append("".join(buf).strip())
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    cells.append("".join(buf).strip())
    if in_code:
        return None
    return cells


def _try_build_table(header_line: str, sep_line: str, row_lines: list[str]):
    header = _split_table_row(header_line)
    sep = _split_table_row(sep_line)
    if header is None or sep is None:
        return None
    if len(header) != len(sep) or not all(re.match(r"^:?-+:?$", c) for c in sep):
        return None
    rows = []
    for rl in row_lines:
        cells = _split_table_row(rl)
        if cells is None:
            return None
        # Tolerate ragged rows (pad/truncate) rather than rejecting the whole
        # table — a single short/long data row is not the kind of ambiguity
        # this needs to fall back on; header/separator shape is what counts.
        if len(cells) < len(header):
            cells = cells + [""] * (len(header) - len(cells))
        elif len(cells) > len(header):
            cells = cells[: len(header)]
        rows.append(cells)
    return ("table", header, rows)


def _parse_list(lines: list[str], i: int, base_indent: int):
    n = len(lines)
    first = lines[i]
    ordered = bool(_OL_ITEM_RE.match(first))
    item_re = _OL_ITEM_RE if ordered else _UL_ITEM_RE
    items: list[tuple[str, tuple | None]] = []
    while i < n:
        line = lines[i]
        if line.strip() == "":
            # A single blank line inside a list is tolerated (loose list);
            # two in a row ends it.
            if i + 1 < n and lines[i + 1].strip() == "":
                break
            i += 1
            continue
        m = item_re.match(line)
        if not m or len(m.group(1)) != base_indent:
            break
        text = m.group(2)
        i += 1
        sub = None
        if i < n:
            nxt = lines[i]
            um2 = _UL_ITEM_RE.match(nxt)
            om2 = _OL_ITEM_RE.match(nxt)
            nm = um2 or om2
            if nm and len(nm.group(1)) > base_indent:
                sub, i = _parse_list(lines, i, len(nm.group(1)))
        items.append((text, sub))
    kind = "ol" if ordered else "ul"
    return (kind, items), i


def _looks_like_block_start(line: str) -> bool:
    if line.strip() == "":
        return True
    if _HEADING_RE.match(line):
        return True
    if _HR_RE.match(line):
        return True
    if line.startswith(">"):
        return True
    if _FENCE_OPEN_RE.match(line):
        return True
    if _UL_ITEM_RE.match(line) or _OL_ITEM_RE.match(line):
        return True
    return False


def _parse_blocks(body: str) -> list[tuple]:
    lines = body.splitlines()
    n = len(lines)
    blocks: list[tuple] = []
    i = 0
    while i < n:
        line = lines[i]
        if line.strip() == "":
            i += 1
            continue

        fm = _FENCE_OPEN_RE.match(line)
        if fm:
            fence_char, fence_len = fm.group(1)[0], len(fm.group(1))
            lang = fm.group(2)
            start = i
            i += 1
            content: list[str] = []
            closed = False
            close_re = re.compile(r"^ {0,3}(" + re.escape(fence_char) + r"{" +
                                   str(fence_len) + r",})\s*$")
            while i < n:
                if close_re.match(lines[i]):
                    closed = True
                    i += 1
                    break
                content.append(lines[i])
                i += 1
            if closed:
                blocks.append(("code", lang, "\n".join(content)))
            else:
                # Unmatched fence: literal fallback for everything from the
                # opening marker to end of body.
                blocks.append(("raw", "\n".join(lines[start:])))
                i = n
            continue

        hm = _HEADING_RE.match(line)
        if hm:
            blocks.append(("heading", len(hm.group(1)), hm.group(2)))
            i += 1
            continue

        if _HR_RE.match(line):
            blocks.append(("hr",))
            i += 1
            continue

        if line.startswith(">"):
            q_lines = []
            while i < n and lines[i].startswith(">"):
                q_lines.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            blocks.append(("quote", "\n".join(q_lines)))
            continue

        if "|" in line and i + 1 < n and _TABLE_SEP_RE.match(lines[i + 1]) \
                and "-" in lines[i + 1]:
            j = i + 2
            row_lines = []
            while j < n and lines[j].strip() != "" and not _looks_like_block_start(
                    lines[j]) and "|" in lines[j]:
                row_lines.append(lines[j])
                j += 1
            table = _try_build_table(line, lines[i + 1], row_lines)
            if table is not None:
                blocks.append(table)
                i = j
                continue
            # Ambiguous — literal fallback for exactly the candidate span.
            blocks.append(("raw", "\n".join(lines[i:j])))
            i = j
            continue

        if _UL_ITEM_RE.match(line) or _OL_ITEM_RE.match(line):
            indent = len(_UL_ITEM_RE.match(line).group(1)) if _UL_ITEM_RE.match(line) \
                else len(_OL_ITEM_RE.match(line).group(1))
            block, i = _parse_list(lines, i, indent)
            blocks.append(block)
            continue

        para_lines = []
        while i < n and not _looks_like_block_start(lines[i]):
            para_lines.append(lines[i].strip())
            i += 1
        if para_lines:
            blocks.append(("para", " ".join(para_lines)))
    return blocks


def _autolink_ids(text: str, valid_gov_ids: frozenset, legacy_ids: frozenset) -> str:
    def repl(m: re.Match) -> str:
        tok = m.group(0)
        if tok in valid_gov_ids:
            return (f'<a href="#/decision/{tok}" class="decision-link">{tok}</a>')
        if tok in legacy_ids:
            return (f'<span class="legacy-ref" title="Historical ledger entry '
                     f'(decision_log.yaml) — not a governance/decisions/ record">'
                     f'{tok}</span>')
        return tok
    return _ID_MENTION_RE.sub(repl, text)


def _inline(text: str, valid_gov_ids: frozenset, legacy_ids: frozenset) -> str:
    codes: list[str] = []

    def stash(m: re.Match) -> str:
        codes.append(m.group(1))
        return f"\x00CODE{len(codes) - 1}\x00"

    text = _INLINE_CODE_RE.sub(stash, text)
    text = html.escape(text)
    text = _BOLD_RE.sub(lambda m: f"<strong>{m.group(2)}</strong>", text)
    text = _ITALIC_RE.sub(lambda m: f"<em>{m.group(1)}</em>", text)
    text = _autolink_ids(text, valid_gov_ids, legacy_ids)

    def restore(m: re.Match) -> str:
        idx = int(m.group(1))
        return f"<code>{html.escape(codes[idx])}</code>"

    text = re.sub(r"\x00CODE(\d+)\x00", restore, text)
    return text


def _slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "section"


def _heading_id(decision_id: str, text: str, used: set[str]) -> str:
    base = f"{decision_id.lower()}-{_slugify(text)}"
    slug, n = base, 2
    while slug in used:
        slug = f"{base}-{n}"
        n += 1
    used.add(slug)
    return slug


def _list_item_html(item, decision_id, valid_gov_ids, legacy_ids, used) -> str:
    text, sub = item
    inner = _inline(text, valid_gov_ids, legacy_ids)
    sub_html = _block_to_html(sub, decision_id, valid_gov_ids, legacy_ids, used) \
        if sub else ""
    return f"<li>{inner}{sub_html}</li>"


def _table_html(block, valid_gov_ids, legacy_ids) -> str:
    _, header, rows = block
    thead = "".join(
        f'<th scope="col">{_inline(c, valid_gov_ids, legacy_ids)}</th>' for c in header
    )
    body_rows = []
    for row in rows:
        cells = "".join(
            f"<td>{_inline(c, valid_gov_ids, legacy_ids)}</td>" for c in row
        )
        body_rows.append(f"<tr>{cells}</tr>")
    return (
        '<div class="table-scroll"><table><thead><tr>' + thead + "</tr></thead>"
        "<tbody>" + "".join(body_rows) + "</tbody></table></div>"
    )


def _block_to_html(block, decision_id, valid_gov_ids, legacy_ids, used: set[str]) -> str:
    kind = block[0]
    if kind == "heading":
        level = min(block[1] + 2, 6)  # source h2..h4 -> detail h4..h6 (title is h3)
        text_html = _inline(block[2], valid_gov_ids, legacy_ids)
        slug = _heading_id(decision_id, block[2], used)
        return f'<h{level} id="{slug}">{text_html}</h{level}>'
    if kind == "para":
        return f"<p>{_inline(block[1], valid_gov_ids, legacy_ids)}</p>"
    if kind == "hr":
        return "<hr>"
    if kind == "quote":
        paras = "".join(
            f"<p>{_inline(ln, valid_gov_ids, legacy_ids)}</p>"
            for ln in block[1].split("\n") if ln.strip()
        )
        return f"<blockquote>{paras or '<p></p>'}</blockquote>"
    if kind == "code":
        lang = block[1]
        cls = f' class="language-{html.escape(lang)}"' if re.match(r"^[\w+-]+$", lang or "") else ""
        return f"<pre><code{cls}>{html.escape(block[2])}</code></pre>"
    if kind in ("ul", "ol"):
        items = "".join(
            _list_item_html(it, decision_id, valid_gov_ids, legacy_ids, used)
            for it in block[1]
        )
        return f"<{kind}>{items}</{kind}>"
    if kind == "table":
        return _table_html(block, valid_gov_ids, legacy_ids)
    if kind == "raw":
        return f'<pre class="literal-fallback">{html.escape(block[1])}</pre>'
    return ""


def render_decision_body(body: str, decision_id: str, valid_gov_ids: frozenset,
                          legacy_ids: frozenset) -> tuple[str, bool]:
    """Returns (safe_html, is_empty)."""
    if not body or not body.strip():
        return '<p class="unavailable">This decision record has no body content.</p>', True
    blocks = _parse_blocks(body)
    if not blocks:
        return '<p class="unavailable">This decision record has no body content.</p>', True
    used: set[str] = set()
    parts = [_block_to_html(b, decision_id, valid_gov_ids, legacy_ids, used) for b in blocks]
    return "".join(parts), False


# ── legacy ledger loading ───────────────────────────────────────────────────

def _load_legacy(repo_root: Path) -> tuple[list[LegacyDecision], list[LoadIssue]]:
    issues: list[LoadIssue] = []
    path = repo_root / DECISION_LOG_REL
    if not path.exists():
        issues.append(LoadIssue(SEVERITY_WARNING, "legacy-missing",
                                 f"{DECISION_LOG_REL} not found"))
        return [], issues
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        issues.append(LoadIssue(SEVERITY_ERROR, "legacy-unreadable",
                                 f"{DECISION_LOG_REL} could not be read: {exc}"))
        return [], issues
    data, err = _safe_load_yaml_text(text)
    if err:
        issues.append(LoadIssue(SEVERITY_ERROR, "legacy-malformed",
                                 f"{DECISION_LOG_REL} failed to parse: {err}"))
        return [], issues
    entries = (data or {}).get("decisions") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        issues.append(LoadIssue(SEVERITY_ERROR, "legacy-malformed",
                                 f"{DECISION_LOG_REL} has no 'decisions' list"))
        return [], issues
    out: list[LegacyDecision] = []
    for e in entries:
        if not isinstance(e, dict) or not e.get("decision_id"):
            issues.append(LoadIssue(SEVERITY_WARNING, "legacy-entry-malformed",
                                     f"skipped malformed {DECISION_LOG_REL} entry"))
            continue
        out.append(LegacyDecision(
            decision_id=str(e["decision_id"]),
            date=str(e.get("date")) if e.get("date") else None,
            status=(str(e.get("status")) if e.get("status") is not None else None),
            category=(str(e.get("category")) if e.get("category") is not None else None),
            decision_text=(str(e.get("decision")) if e.get("decision") is not None else None),
            rationale=(str(e.get("rationale")) if e.get("rationale") is not None else None),
            supporting_artifact=(
                str(e.get("supporting_artifact"))
                if e.get("supporting_artifact") is not None else None
            ),
        ))
    return out, issues


# ── governance index loading ────────────────────────────────────────────────

def _load_index(repo_root: Path) -> tuple[dict[str, dict], list[LoadIssue]]:
    """Returns (id -> index-entry dict, issues). On malformed index, returns
    an empty map with a prominent catalog-level issue — callers then fall
    back to pure filesystem discovery (every file becomes 'orphan')."""
    issues: list[LoadIssue] = []
    path = repo_root / DECISIONS_INDEX_REL
    if not path.exists():
        issues.append(LoadIssue(SEVERITY_ERROR, "index-missing",
                                 f"{DECISIONS_INDEX_REL} not found — generated-index "
                                 "failure, degrading to filesystem discovery only"))
        return {}, issues
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        issues.append(LoadIssue(SEVERITY_ERROR, "index-unreadable",
                                 f"{DECISIONS_INDEX_REL} could not be read: {exc} — "
                                 "generated-index failure, degrading to filesystem "
                                 "discovery only"))
        return {}, issues
    data, err = _safe_load_yaml_text(text)
    if err or not isinstance(data, dict):
        issues.append(LoadIssue(SEVERITY_ERROR, "index-malformed",
                                 f"{DECISIONS_INDEX_REL} failed to parse"
                                 + (f": {err}" if err else " (not a mapping)")
                                 + " — generated-index failure, degrading to "
                                   "filesystem discovery only"))
        return {}, issues
    entries = data.get("decisions")
    if not isinstance(entries, list):
        issues.append(LoadIssue(SEVERITY_ERROR, "index-malformed",
                                 f"{DECISIONS_INDEX_REL} has no 'decisions' list — "
                                 "generated-index failure, degrading to filesystem "
                                 "discovery only"))
        return {}, issues
    out: dict[str, dict] = {}
    for e in entries:
        if not isinstance(e, dict) or not e.get("decision_id"):
            issues.append(LoadIssue(SEVERITY_WARNING, "index-entry-malformed",
                                     f"skipped malformed index entry: {e!r}"))
            continue
        did = str(e["decision_id"])
        if did in out:
            issues.append(LoadIssue(SEVERITY_WARNING, "index-duplicate-id",
                                     f"{DECISIONS_INDEX_REL} lists decision_id "
                                     f"{did!r} more than once — keeping the first"))
            continue
        out[did] = e
    return out, issues


# ── directory scan / per-file parse ─────────────────────────────────────────

@dataclass
class _RawFile:
    filename: str
    path_rel: str
    decision_id: str | None
    frontmatter: dict | None
    body: str
    parse_error: str | None
    issues: list[LoadIssue]


def _scan_files(repo_root: Path) -> list[_RawFile]:
    d = repo_root / DECISIONS_DIR_REL
    out: list[_RawFile] = []
    if not d.is_dir():
        return out
    for p in sorted(d.glob("*.md")):
        if p.name == README_NAME:
            continue
        rel = f"{DECISIONS_DIR_REL}/{p.name}"
        issues: list[LoadIssue] = []
        def _fallback_id() -> str:
            # Used only when a real frontmatter decision_id can't be
            # recovered — a best-effort ID so the file still surfaces as a
            # visible, filename-identified degraded stub rather than being
            # silently dropped from the catalog.
            fname_m = _FILENAME_ID_RE.match(p.name)
            return fname_m.group(1) if fname_m else p.stem

        try:
            text = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            out.append(_RawFile(p.name, rel, _fallback_id(), None, "",
                                 f"could not be read: {exc}",
                                 [LoadIssue(SEVERITY_ERROR, "file-unreadable",
                                             f"{rel}: could not be read ({exc})")]))
            continue
        fm, body, err = _split_frontmatter(text)
        did = None
        if err:
            issues.append(LoadIssue(SEVERITY_ERROR, "frontmatter-malformed",
                                     f"{rel}: {err}"))
            did = _fallback_id()
        elif not isinstance(fm.get("decision_id"), str) or not fm["decision_id"].strip():
            issues.append(LoadIssue(SEVERITY_ERROR, "frontmatter-malformed",
                                     f"{rel}: frontmatter missing 'decision_id'"))
            err = err or "frontmatter missing decision_id"
            fm = None
            did = _fallback_id()
        else:
            did = fm["decision_id"].strip()
            fname_m = _FILENAME_ID_RE.match(p.name)
            if fname_m and fname_m.group(1) != did:
                issues.append(LoadIssue(
                    SEVERITY_WARNING, "filename-frontmatter-id-mismatch",
                    f"{rel}: filename implies decision_id {fname_m.group(1)!r}, "
                    f"frontmatter declares {did!r} — frontmatter controls"))
        out.append(_RawFile(p.name, rel, did, fm, body, err, issues))
    return out


# ── the builder ──────────────────────────────────────────────────────────────

def build_catalog(repo_root: Path | str) -> DecisionCatalog:
    """Assemble the DecisionCatalog. Pure read; never writes anything; never
    raises — every failure mode degrades to a visible warning/stub."""
    repo_root = Path(repo_root).resolve()
    catalog_issues: list[LoadIssue] = []

    legacy, legacy_issues = _load_legacy(repo_root)
    catalog_issues.extend(legacy_issues)
    legacy_ids = frozenset(l.decision_id for l in legacy)

    index_by_id, index_issues = _load_index(repo_root)
    catalog_issues.extend(index_issues)

    raw_files = _scan_files(repo_root)

    # Duplicate decision_id across files (frontmatter-declared), canonical =
    # the file whose path matches the index's registered `file:` value for
    # that ID, else the lexicographically first path — deterministic either way.
    by_id: dict[str, list[_RawFile]] = {}
    for rf in raw_files:
        if rf.decision_id:
            by_id.setdefault(rf.decision_id, []).append(rf)
    duplicate_paths: dict[str, set[str]] = {}
    for did, files in by_id.items():
        if len(files) > 1:
            duplicate_paths[did] = {f.path_rel for f in files}
            paths = sorted(f.path_rel for f in files)
            catalog_issues.append(LoadIssue(
                SEVERITY_WARNING, "duplicate-decision-id",
                f"decision_id {did!r} declared in more than one file: "
                f"{', '.join(paths)} — all render, canonical selection is "
                "deterministic (index-registered path, else lexicographically first)"
            ))

    def canonical_for(did: str) -> str | None:
        files = by_id.get(did)
        if not files:
            return None
        if len(files) == 1:
            return files[0].path_rel
        idx_entry = index_by_id.get(did)
        idx_file = idx_entry.get("file") if idx_entry else None
        paths = sorted(f.path_rel for f in files)
        return idx_file if idx_file in paths else paths[0]

    valid_gov_ids = frozenset(by_id.keys())

    # Phase 2: build full DecisionDetail for every discovered file.
    details: list[DecisionDetail] = []
    seen_ids: set[str] = set()

    # Order: index order first (matches the existing flat Governance table's
    # insertion order), then any orphan files not present in the index,
    # sorted by decision_id for determinism.
    ordered_ids: list[str] = list(index_by_id.keys())
    for did in sorted(by_id.keys()):
        if did not in index_by_id:
            ordered_ids.append(did)

    reverse_map: dict[str, list[str]] = {}

    def build_detail(did: str) -> DecisionDetail | None:
        files = by_id.get(did)
        idx_entry = index_by_id.get(did)
        indexed = idx_entry is not None
        if not files:
            if not idx_entry:
                return None
            # Index references an ID with no backing file on disk.
            idx_file = idx_entry.get("file") or f"{DECISIONS_DIR_REL}/{did}.md"
            title, title_source = _derive_title(
                frontmatter=None, body="", filename=Path(idx_file).name, decision_id=did)
            issues = (LoadIssue(
                SEVERITY_ERROR, "index-missing-file",
                f"{DECISIONS_INDEX_REL} lists {did!r} at {idx_file!r}, but that "
                "file does not exist on disk",
            ),)
            return DecisionDetail(
                decision_id=did, title=title, title_source=title_source,
                date=(str(idx_entry.get("date")) if idx_entry.get("date") else None),
                status=idx_entry.get("status"), category=idx_entry.get("category"),
                related=(), reverse_references=(), supporting_artifact=None,
                source=DecisionSource(idx_file, False, None, None),
                body_html='<p class="unavailable">Source file not found on disk.</p>',
                body_empty=True, issues=issues, indexed=True, index_mismatches=(),
                duplicate_id=False, orphan=False, source_missing=True,
            )

        canon_path = canonical_for(did)
        rf = next((f for f in files if f.path_rel == canon_path), files[0])
        issues: list[LoadIssue] = list(rf.issues)
        is_dup = did in duplicate_paths

        if rf.parse_error and rf.frontmatter is None:
            # Degraded stub: filename-identified, raw body shown only if we
            # actually managed to separate one.
            title, title_source = _derive_title(
                frontmatter=None, body=rf.body, filename=rf.filename, decision_id=did)
            source = DecisionSource(rf.path_rel, True, *_hash_file(repo_root / rf.path_rel))
            body_html, body_empty = render_decision_body(
                rf.body, did, valid_gov_ids, legacy_ids) if rf.body else (
                '<p class="unavailable">No content could be safely separated from '
                'this file.</p>', True)
            return DecisionDetail(
                decision_id=did, title=title, title_source=title_source,
                date=None, status=None, category=None, related=(),
                reverse_references=(), supporting_artifact=None, source=source,
                body_html=body_html, body_empty=body_empty, issues=tuple(issues),
                indexed=indexed, index_mismatches=(), duplicate_id=is_dup,
                orphan=not indexed, source_missing=False,
            )

        fm = rf.frontmatter or {}
        status = fm.get("status")
        if status is not None and status not in KNOWN_STATUSES:
            issues.append(LoadIssue(SEVERITY_WARNING, "unsupported-status",
                                     f"{rf.path_rel}: status {status!r} is outside "
                                     f"the documented vocabulary "
                                     f"{sorted(KNOWN_STATUSES)}"))

        mismatches: list[str] = []
        if idx_entry:
            for field, fm_key in (("date", "date"), ("status", "status"),
                                   ("category", "category")):
                fm_val = fm.get(fm_key)
                idx_val = idx_entry.get(fm_key)
                if str(fm_val) != str(idx_val) and not (fm_val is None and idx_val is None):
                    mismatches.append(
                        f"{field}: frontmatter={fm_val!r} vs index={idx_val!r} "
                        "(frontmatter controls)"
                    )
            idx_file = idx_entry.get("file")
            if idx_file and idx_file != rf.path_rel:
                mismatches.append(
                    f"file: frontmatter-derived path={rf.path_rel!r} vs "
                    f"index file={idx_file!r} (frontmatter/filesystem controls)"
                )
        if mismatches:
            issues.append(LoadIssue(SEVERITY_WARNING, "index-frontmatter-mismatch",
                                     f"{rf.path_rel}: " + "; ".join(mismatches)))

        title, title_source = _derive_title(
            frontmatter=fm, body=rf.body, filename=rf.filename, decision_id=did)

        raw_related = fm.get("related_decisions") or []
        if not isinstance(raw_related, list):
            raw_related = []
        related: list[RelatedRef] = []
        seen_related: set[str] = set()
        for r in raw_related:
            r = str(r)
            if r == did:
                issues.append(LoadIssue(SEVERITY_WARNING, "self-reference",
                                         f"{rf.path_rel}: related_decisions lists "
                                         "itself — omitted from the related list"))
                continue
            if r in seen_related:
                issues.append(LoadIssue(SEVERITY_WARNING, "duplicate-related-reference",
                                         f"{rf.path_rel}: related_decisions lists "
                                         f"{r!r} more than once — shown once"))
                continue
            seen_related.add(r)
            if r in valid_gov_ids:
                kind = "governance"
            elif r in legacy_ids:
                kind = "legacy"
            else:
                kind = "unresolved"
                issues.append(LoadIssue(SEVERITY_WARNING, "unresolved-related-reference",
                                         f"{rf.path_rel}: related_decisions references "
                                         f"{r!r}, found in neither governance/decisions "
                                         "nor decision_log.yaml"))
            related.append(RelatedRef(r, kind))
            if kind == "governance":
                reverse_map.setdefault(r, []).append(did)

        artifact = None
        sa = fm.get("supporting_artifact")
        if isinstance(sa, str) and sa.strip():
            artifact = _resolve_artifact(repo_root, sa)
            if not artifact.safe and artifact.warning:
                issues.append(LoadIssue(SEVERITY_WARNING, "supporting-artifact-issue",
                                         f"{rf.path_rel}: supporting_artifact "
                                         f"{sa!r} — {artifact.warning}"))

        source = DecisionSource(rf.path_rel, True, *_hash_file(repo_root / rf.path_rel))
        body_html, body_empty = render_decision_body(rf.body, did, valid_gov_ids, legacy_ids)

        if not indexed:
            issues.append(LoadIssue(SEVERITY_WARNING, "not-indexed",
                                     f"{rf.path_rel}: exists on disk but has no "
                                     f"{DECISIONS_INDEX_REL} entry"))

        return DecisionDetail(
            decision_id=did, title=title, title_source=title_source,
            date=(str(fm.get("date")) if fm.get("date") else None),
            status=status, category=fm.get("category"),
            related=tuple(related), reverse_references=(),  # filled in below
            supporting_artifact=artifact, source=source,
            body_html=body_html, body_empty=body_empty, issues=tuple(issues),
            indexed=indexed, index_mismatches=tuple(mismatches),
            duplicate_id=is_dup, orphan=not indexed, source_missing=False,
        )

    pending: list[DecisionDetail] = []
    for did in ordered_ids:
        if did in seen_ids:
            continue
        seen_ids.add(did)
        detail = build_detail(did)
        if detail is not None:
            pending.append(detail)

    # Fill in reverse references now that the full map is known.
    for d in pending:
        refs = tuple(sorted(set(reverse_map.get(d.decision_id, ()))))
        details.append(
            DecisionDetail(
                decision_id=d.decision_id, title=d.title, title_source=d.title_source,
                date=d.date, status=d.status, category=d.category, related=d.related,
                reverse_references=refs, supporting_artifact=d.supporting_artifact,
                source=d.source, body_html=d.body_html, body_empty=d.body_empty,
                issues=d.issues, indexed=d.indexed, index_mismatches=d.index_mismatches,
                duplicate_id=d.duplicate_id, orphan=d.orphan, source_missing=d.source_missing,
            )
        )

    return DecisionCatalog(
        decisions=tuple(details),
        legacy=tuple(legacy),
        valid_ids=valid_gov_ids,
        legacy_ids=legacy_ids,
        issues=tuple(catalog_issues),
    )
