"""Create drafts and posts, and publish drafts, for this Jekyll blog.

A post is _posts/YYYY-MM-DD-<slug>.md. Jekyll reads the publish date from the
file name and serves the post at /posts/<slug>/. A draft is _drafts/<slug>.md;
the deployed site never builds drafts, and `jekyll serve --drafts` previews
them. Images for a post go in assets/posts/<slug>/.

Usage:
    python tools/post.py new <slug> [--title TITLE] [--tags a,b] [--draft]
    python tools/post.py publish <slug>
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = Path(__file__).resolve().parent / "post-template.md"

# The slug becomes the URL path segment and the image folder name, so it is
# kept to lowercase ASCII words joined by single hyphens.
SLUG_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
DATE_LINE = re.compile(r"^date: .*$", re.MULTILINE)


class PostError(Exception):
    """A request that cannot be carried out; the message says why."""


def check_slug(slug: str) -> None:
    if not SLUG_PATTERN.fullmatch(slug):
        raise PostError(
            f"invalid slug {slug!r}: use lowercase letters, digits and single "
            "hyphens, for example 'example-post'"
        )


def find_existing(root: Path, slug: str) -> list[Path]:
    """Return every post or draft that already uses `slug`."""
    posts = [
        p for p in (root / "_posts").glob(f"*-{slug}.md")
        if p.name[11:-3] == slug
    ]
    draft = root / "_drafts" / f"{slug}.md"
    return posts + ([draft] if draft.exists() else [])


def format_date(now: datetime) -> str:
    return now.strftime("%Y-%m-%d %H:%M:%S %z")


def render(title: str, tags: list[str], now: datetime) -> str:
    # JSON strings and lists are valid YAML, so json.dumps quotes titles that
    # contain colons or quotation marks correctly.
    return Template(TEMPLATE.read_text(encoding="utf-8")).substitute(
        title=json.dumps(title, ensure_ascii=False),
        tags=json.dumps(tags, ensure_ascii=False),
        date=format_date(now),
    )


def create(root: Path, slug: str, title: str, tags: list[str],
           draft: bool, now: datetime) -> Path:
    check_slug(slug)
    existing = find_existing(root, slug)
    if existing:
        raise PostError(f"slug {slug!r} is already used by {existing[0]}")
    if draft:
        path = root / "_drafts" / f"{slug}.md"
    else:
        path = root / "_posts" / f"{now:%Y-%m-%d}-{slug}.md"
    path.parent.mkdir(exist_ok=True)
    path.write_text(render(title, tags, now), encoding="utf-8", newline="\n")
    return path


def publish(root: Path, slug: str, now: datetime) -> Path:
    check_slug(slug)
    draft = root / "_drafts" / f"{slug}.md"
    if not draft.exists():
        raise PostError(f"no draft at {draft}; list drafts with: ls _drafts")
    taken = [p for p in find_existing(root, slug) if p != draft]
    if taken:
        raise PostError(f"slug {slug!r} is already used by {taken[0]}")

    text = draft.read_text(encoding="utf-8")
    # The draft's date is when it was started; the post's date is today.
    text, count = DATE_LINE.subn(f"date: {format_date(now)}", text, count=1)
    if count == 0:
        raise PostError(f"{draft} has no 'date:' line in its front matter")

    path = root / "_posts" / f"{now:%Y-%m-%d}-{slug}.md"
    path.parent.mkdir(exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    draft.unlink()
    return path


def parse_tags(raw: str) -> list[str]:
    return [t.strip() for t in raw.split(",") if t.strip()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python tools/post.py",
        description="Create drafts and posts, and publish drafts.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    new = commands.add_parser(
        "new", help="create a post dated today, or a draft with --draft")
    new.add_argument("slug", help="URL name, e.g. example-post")
    new.add_argument("-t", "--title", help="post title (default: the slug)")
    new.add_argument("--tags", default="",
                     help="comma separated tags, e.g. tag1,tag2")
    new.add_argument("-d", "--draft", action="store_true",
                     help="create in _drafts/ instead of _posts/")

    pub = commands.add_parser(
        "publish", help="move a draft to _posts/ with today's date")
    pub.add_argument("slug", help="file name of the draft without .md")

    args = parser.parse_args(argv)
    now = datetime.now().astimezone()
    try:
        if args.command == "new":
            path = create(ROOT, args.slug, args.title or args.slug,
                          parse_tags(args.tags), args.draft, now)
        else:
            path = publish(ROOT, args.slug, now)
    except PostError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"wrote {path.relative_to(ROOT).as_posix()}")
    print(f"images go in assets/posts/{args.slug}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
