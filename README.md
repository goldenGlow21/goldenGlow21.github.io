# goldenGlow21.github.io

Personal blog, built by Jekyll and deployed to GitHub Pages by GitHub Actions
on every push to `main`. The theme is the handful of templates in this
repository; there is no theme gem and no plugin.

## Writing a post

Create a Markdown file in `_posts/` named `YYYY-MM-DD-slug.md`, then commit
and push. The post is live once the Actions run finishes.

```markdown
---
title: CVE-2025-12345 heap overflow PoC
tags: [poc, linux]
---
Body in Markdown, pasted from Notion or written directly.
```

- The date in the file name is the publish date; the slug after it gives the
  URL, `/posts/<slug>/`.
- The first paragraph is the summary on the post lists and in link previews.
- Images go in `assets/img/` and are linked by site path:
  `![shot](/assets/img/cve-2025-12345/crash.png)`.
- `{{ }}` and `{% %}` inside a post are printed as written, so template
  injection payloads show up intact.

Optional front matter fields:

| Field | Meaning |
|---|---|
| `description` | Summary used instead of the first paragraph. |
| `updated` | Revision date shown next to the publish date, for example `2026-11-20`. |
| `comments` | `false` hides the comment thread on this post. |
| `published` | `false` keeps the post off the site. |

What the post body supports:

- Code blocks with a language name are highlighted and get a header with the
  language name and a copy button.
- On wide screens a post with two or more `##` / `###` headings gets an
  outline beside the text that follows the reader's position.
- `> text` followed by `{: .note}` or `{: .warning}` on the next line gives a
  note or warning box.
- `* TOC` followed by `{:toc}` inserts a table of contents in the body.

## Pages

| URL | Source | Content |
|---|---|---|
| `/` | `index.md`, `_layouts/home.html` | Banner with the site title and links, newest posts, tags, years. Text written in `index.md` appears under the title. |
| `/posts/` | `posts.html` | Every post, grouped by year. |
| `/tags/` | `tags.html` | Every tag with its posts. |
| `/about/` | `about.md` | Free text. |

## Previewing locally

Pushing is enough to publish; a local preview is optional. It needs Ruby 3.4
and Bundler:

```bash
bundle install
bundle exec jekyll serve
```

Without a Ruby install, Docker runs the same thing:

```bash
docker run --rm -it -p 4000:4000 -v "${PWD}:/srv/site" -w /srv/site ruby:3.4 sh -c "bundle install && bundle exec jekyll serve --host 0.0.0.0 --force_polling"
```

The site is then at http://localhost:4000 and rebuilds when a file changes.
`--force_polling` is needed because a folder mounted from Windows does not
deliver file change events into the container. The container installs the
gems again on every start, which takes about a minute.

## Where things are

```
_posts/               posts, one Markdown file each
assets/img/           images used by posts
_config.yml           site title, author, comment settings, post defaults
_data/navigation.yml  header menu
_data/links.yml       profile links on the front page and in the footer
index.md              front page; text written here appears under the title
posts.html            post archive at /posts/
tags.html             tag index at /tags/
about.md              About page
404.html              page for unknown URLs
feed.xml              Atom feed at /feed.xml
sitemap.xml           sitemap for search engines
robots.txt            crawler rules, points to the sitemap
_layouts/             page shells: default (frame), home, post, page
_includes/            pieces used by the layouts, one file per piece
_sass/                styles: tokens (colors, fonts, widths), base, layout,
                      lists, home, prose, code, syntax
assets/css/main.scss  stylesheet entry point; imports the partials in _sass/
assets/js/site.js     theme toggle, comments, code copy buttons, post outline,
                      heading links
.github/workflows/    build, link check, and deploy to GitHub Pages
```

Common changes:

- Colors, fonts and column widths: `_sass/_tokens.scss`, which holds a light
  and a dark palette. A page follows the reader's system setting until the
  reader picks a theme with the header toggle; the choice is stored in the
  browser.
- The typeface is Pretendard, loaded from the jsDelivr CDN in
  `_includes/head.html`.
- A new header menu entry: add a page with a `permalink`, then add it to
  `_data/navigation.yml`.
- A new profile link: add it to `_data/links.yml`; its `icon` must be one of
  the names in `_includes/icon.html`.
- Turning comments off everywhere: empty `giscus.repo` in `_config.yml`.

CI runs `htmlproofer` over the generated site and fails on broken internal
links or missing images.
