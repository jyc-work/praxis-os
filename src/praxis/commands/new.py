"""praxis new — create a new entity from a template.

    praxis new value
    praxis new model --model-type philosophy
    praxis new principle --domain career --title "..."
    praxis new decision --domain career --title "..."
    praxis new experiment --title "..."
    praxis new review --type weekly

Pipeline: determine domain → generate ID → copy template → populate metadata
→ write file.  On invalid input nothing is written (no half-files).
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

from praxis.config import find_repo_root, load_config
from praxis.core.ids import IdError, next_id, validate_id

TODAY = datetime.date.today().isoformat()

#: which template file each entity type uses
TEMPLATE_BY_TYPE = {
    "value": "value.md",
    "model": "thinker.md",
    "principle": "principle.md",
    "decision": "decision.md",
    "experiment": "experiment.md",
    "review": "quarterly-review.md",
}

REVIEW_TEMPLATE_BY_TYPE = {
    "weekly": "weekly-review.md",
    "monthly": "quarterly-review.md",
    "quarterly": "quarterly-review.md",
    "annual": "quarterly-review.md",
    "decision": "quarterly-review.md",
}

VALID_REVIEW_TYPES = tuple(REVIEW_TEMPLATE_BY_TYPE)

MODEL_TYPES = ("thinker", "philosophy", "mental-model", "world-model")

#: model_type → plural directory name (matches Technical Design structure)
MODEL_DIR_PLURALS = {
    "thinker": "thinkers",
    "philosophy": "philosophies",
    "mental-model": "mental-models",
    "world-model": "world-models",
}

DOMAIN_RE = re.compile(r"^[a-z][a-z0-9-]*$")
ALLOWED_DOMAINS = (
    "career", "life", "finance", "relationships", "health",
    "decision-making", "emotion", "action", "investing", "learning", "other",
)

ENTITY_SUPPORTED = ("value", "model", "principle", "decision", "experiment", "review")


def slugify(title: str) -> str:
    """Turns a title into a filename slug (ASCII-ish, hyphenated)."""
    slug = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", "-", title.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug[:60] or "untitled"


def _domain_dir(domain: str) -> str:
    return domain.lower()


def _resolve_template(config, entity_type: str, review_type: str | None) -> Path:
    template_dir = config.root / "templates"
    name = TEMPLATE_BY_TYPE[entity_type]
    if entity_type == "review":
        name = REVIEW_TEMPLATE_BY_TYPE[review_type or "weekly"]
    path = template_dir / name
    if not path.is_file():
        raise FileNotFoundError(f"template not found: {path}")
    return path


def _populate(
    template_text: str,
    metadata: dict,
    title: str,
    domain: str | None,
) -> str:
    """Replace template placeholders with generated values."""
    text = template_text
    now = TODAY

    # ids always differ per file
    text = re.sub(r"^id: .*$", f"id: {metadata['id']}", text, flags=re.MULTILINE)
    text = re.sub(r"^title: .*$", f"title: {title}", text, flags=re.MULTILINE)
    text = re.sub(r"^created_at: .*$", f"created_at: {now}", text, flags=re.MULTILINE)
    text = re.sub(r"^updated_at: .*$", f"updated_at: {now}", text, flags=re.MULTILINE)

    if domain:
        # single-value form: `domain: career`
        if re.search(r"^domain: ", text, flags=re.MULTILINE):
            text = re.sub(
                r"^domain: .*$", f"domain: {domain}", text, flags=re.MULTILINE
            )
        # array form: `domains:\n  - career`
        if re.search(r"^domains:", text, flags=re.MULTILINE):
            text = re.sub(
                r"^domains:(?:\n\s+-[^\n]*)+",
                f"domains:\n  - {domain}",
                text,
                flags=re.MULTILINE,
            )

    if "model_type" in metadata:
        text = re.sub(
            r"^model_type: .*$",
            f"model_type: {metadata['model_type']}",
            text,
            flags=re.MULTILINE,
        )
    if "review_type" in metadata:
        text = re.sub(
            r"^review_type: .*$",
            f"review_type: {metadata['review_type']}",
            text,
            flags=re.MULTILINE,
        )

    # cosmetic title placeholders in the body
    text = text.replace("{name}", title).replace("{name_zh}", title)
    return text


def _write_entity(config, entity_type: str, metadata: dict, body: str) -> Path:
    entity_dir = config.dir_for(entity_type + "s")
    domain = str(metadata.get("domain") or "").lower()
    base_dir = entity_dir

    if entity_type == "principle":
        base_dir = entity_dir / _domain_dir(domain) if domain else entity_dir
    elif entity_type == "decision":
        base_dir = entity_dir / _domain_dir(domain) if domain else entity_dir
    elif entity_type == "model":
        model_type = str(metadata.get("model_type") or "mental-model")
        plural = MODEL_DIR_PLURALS.get(model_type, model_type + "s")
        base_dir = entity_dir / plural
    elif entity_type == "review":
        review_type = str(metadata.get("review_type") or "weekly")
        sub = "decisions" if review_type == "decision" else review_type
        base_dir = entity_dir / _domain_dir(sub)

    base_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{metadata['id']}-{slugify(str(metadata.get('title') or metadata.get('name') or entity_type))}.md"
    path = base_dir / filename

    if path.exists():
        raise IdError(f"target file already exists: {path}")
    path.write_text(body, encoding="utf-8")
    return path


def build_entity(
    config,
    entity_type: str,
    title: str,
    domain: str | None,
    review_type: str | None,
    model_type: str | None,
) -> Path:
    if entity_type not in ENTITY_SUPPORTED:
        raise ValueError(
            f"unsupported entity type {entity_type!r}; use one of {ENTITY_SUPPORTED}"
        )
    if domain and not DOMAIN_RE.match(domain):
        raise ValueError(
            f"invalid domain {domain!r}: only lowercase letters, digits and hyphens"
        )

    from praxis.core.index import Repository

    repo = Repository.load(config)
    existing = [e.id for e in repo.all_entities]
    if entity_type == "review":
        id_domain = (review_type or "weekly").upper()
    else:
        id_domain = (domain or "life").upper()
    new_id = next_id(existing, entity_type, id_domain)

    metadata = {
        "id": new_id,
        "type": entity_type,
        "title": title,
        "domain": domain or ("life" if entity_type in ("value", "model", "principle") else "career"),
    }
    if entity_type == "model":
        metadata["model_type"] = model_type or "mental-model"
    if entity_type == "review":
        metadata["review_type"] = review_type or "weekly"

    validate_id(entity_type, new_id)

    template = _resolve_template(config, entity_type, review_type)
    text = template.read_text(encoding="utf-8")
    body = _populate(text, metadata, title, metadata["domain"])

    return _write_entity(config, entity_type, metadata, body)


def run(args: argparse.Namespace) -> int:
    try:
        root = Path(args.root).resolve() if getattr(args, "root", None) else find_repo_root()
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    config = load_config(root)
    entity_type = args.entity_type
    try:
        path = build_entity(
            config,
            entity_type,
            title=args.title,
            domain=getattr(args, "domain", None),
            review_type=getattr(args, "type", None),
            model_type=getattr(args, "model_type", None),
        )
    except (ValueError, IdError, FileNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"created {path.relative_to(config.root)} ({entity_type})")
    return 0