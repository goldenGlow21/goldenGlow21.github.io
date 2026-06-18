---
title: "(템플릿) CTF write-up"
categories: [CTF]
tags: [template]
description: CTF 라이트업 작성 시 참고용 템플릿.
---

> 이 파일은 `_drafts/` 에 있어 빌드되지 않습니다.
> 새 라이트업을 쓸 땐 이 파일을 복사해 `_posts/YYYY-MM-DD-제목.md` 로 옮기세요.
{: .prompt-info }

## Challenge

- 대회: `<event name>`
- 카테고리: Forensic / Reversing / ...
- 난이도: ★★☆☆☆
- 포인트: 200

## Description

문제 설명 원문 또는 요약.

## Recon

처음 받은 파일/URL을 어떻게 살펴봤는지.

```bash
file challenge.bin
strings -n 8 challenge.bin | head
```

## Solution

풀이 흐름.

## Flag

```text
flag{...}
```

## Lessons

다음에 비슷한 문제 만났을 때 떠올릴 한 줄.
