# goldenGlow21.github.io

Personal blog, built by Jekyll and deployed to GitHub Pages by GitHub Actions
on every push to `main`. The theme is the handful of templates in this
repository; there is no theme gem and no Jekyll plugin.

## Writing a post

```bash
python tools/post.py new example-post -t "Example post" --tags tag1,tag2
```

This writes `_posts/YYYY-MM-DD-example-post.md` dated now. Write the
body under the front matter, commit, and push. The post appears at
`/posts/example-post/`.

To work on something over several days without publishing it:

```bash
python tools/post.py new half-done-idea --draft
python tools/post.py publish half-done-idea
```

The first command writes `_drafts/half-done-idea.md`, which the live site never
builds. The second moves it to `_posts/` and sets its date to now.

The slug is the URL name and the image folder name, so it is limited to
lowercase ASCII letters, digits and hyphens, so a CVE id is written as
`cve-2025-12345`. The title can be anything.

### Front matter

| Field | Required | Meaning |
|---|---|---|
| `title` | yes | Post title. |
| `date` | yes | Publish time. Orders posts and is shown under the title. |
| `tags` | no | List of tags, for example `[tag1, tag2]`. Each tag gets a section on `/tags/`. |
| `description` | no | One line for search results and link previews. Empty means the first paragraph is used. |
| `updated` | no | Date of a later revision, for example `2026-12-01`. Shown next to the publish date. |
| `comments` | no | `false` hides the comment thread on this post. |

### Images

Put image files in `assets/posts/<slug>/`, then either use plain Markdown:

```markdown
![Diagram](/assets/posts/example-post/diagram.png)
```

or the figure include, which takes a bare file name and adds a caption:

```liquid
{% include figure.html src="diagram.png" alt="Diagram" caption="Caption text" %}
```

### Other Markdown features

Code blocks with a language name are highlighted and get a header with the
language name and a copy button:

````markdown
```python
print("hello")
```
````

A note or warning box is a blockquote with a class on the next line:

```markdown
> Note text.
{: .note}

> Warning text.
{: .warning}
```

A table of contents of the post's headings:

```markdown
* TOC
{:toc}
```

Footnotes use `text[^1]` and, anywhere below, `[^1]: The note.`

## Previewing locally

Pushing is enough to publish; a local preview is optional. It needs Ruby 3.4
and Bundler:

```bash
bundle install
bundle exec jekyll serve --drafts
```

Without a Ruby install, Docker runs the same thing:

```bash
docker run --rm -it -p 4000:4000 -v "${PWD}:/srv/site" -w /srv/site ruby:3.4 sh -c "bundle install && bundle exec jekyll serve --drafts --host 0.0.0.0 --force_polling"
```

The site is then at http://localhost:4000 and rebuilds when a file changes.
`--force_polling` is needed because a folder mounted from Windows does not
deliver file change events into the container. The container installs the
gems again on every start, which takes about a minute.

## Where things are

```
_config.yml           site title, description, author, comment settings
_data/navigation.yml  header menu
_data/links.yml       footer links
index.md              front page; text written here appears above the post list
about.md              About page
tags.html             tag index at /tags/
404.html              page for unknown URLs
feed.xml              Atom feed at /feed.xml
sitemap.xml           sitemap for search engines
robots.txt            crawler rules, points to the sitemap
_posts/               published posts, YYYY-MM-DD-<slug>.md
_drafts/              unpublished drafts, <slug>.md
assets/posts/<slug>/  images and files used by one post
assets/css/main.scss  stylesheet entry point; imports the partials in _sass/
assets/js/site.js     theme toggle, comment loader, code copy buttons, heading links
_layouts/             page shells: default (frame), home, post, page
_includes/            pieces used by the layouts, one file per piece
_sass/                styles: tokens (colors, fonts), base, layout, lists, prose, code, syntax
tools/post.py         creates posts and drafts, publishes drafts
.github/workflows/    build, link check, and deploy to GitHub Pages
```

Common changes:

- Colors and fonts: `_sass/_tokens.scss`, which holds a light and a dark
  palette. A page follows the reader's system setting until the reader picks
  a theme with the header toggle; the choice is stored in the browser.
- The typeface is Pretendard, loaded from the jsDelivr CDN in
  `_includes/head.html`.
- A new header menu entry: add a page with a `permalink`, then add it to
  `_data/navigation.yml`.
- Turning comments off everywhere: empty `giscus.repo` in `_config.yml`.

## Tests

The post tool has unit tests:

```bash
python -m unittest discover tools
```

The CI build runs `htmlproofer` over the generated site and fails on broken
internal links or missing images.
