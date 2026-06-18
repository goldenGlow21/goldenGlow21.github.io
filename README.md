# goldenGlow21.github.io

[Jekyll](https://jekyllrb.com/) + [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) 기반 개인 블로그.
보안 / 디지털 포렌식 학습 기록.

## 글 쓰는 법

새 글은 `_posts/` 에 다음 형식으로 만든다.

```
_posts/YYYY-MM-DD-제목.md
```

front matter 예시:

```yaml
---
title: "글 제목"
date: 2026-06-19 21:00:00 +0900
categories: [Forensic]      # 대분류(, 소분류) 최대 2단계
tags: [memory, volatility]  # 소문자, 자유롭게
description: 목록/SEO에 쓰일 한 줄 요약.
---
```

- **카테고리**는 사이드바의 *Categories* 탭에 자동 집계된다. 권장: `CTI`, `Forensic`, `CTF`, `Misc`.
- **태그**는 *Tags* 탭에 자동 집계된다.
- 초안은 `_drafts/` 에 두면 빌드되지 않는다. (`_drafts/ctf-writeup-template.md` 참고)
- 글을 push 하면 GitHub Actions 가 자동으로 빌드·배포한다.

## 로컬 미리보기 (선택)

Ruby 가 설치돼 있으면:

```bash
bundle install
bundle exec jekyll serve
# http://127.0.0.1:4000
```

Ruby 가 없어도 push 하면 Actions 가 빌드하므로 사이트는 정상 동작한다.

## 댓글 (giscus)

`_config.yml` 의 `comments.giscus` 에서 `repo_id` 와 `category_id` 를
[giscus.app](https://giscus.app) 에서 발급받아 채워야 활성화된다. (README 하단 설정 메모 참고)
