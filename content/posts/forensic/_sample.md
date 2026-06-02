---
title: "(template) Forensic 케이스 템플릿"
date: 2026-06-01
description: "포렌식 케이스/노트 작성 시 참고용 템플릿."
categories: ["forensic"]
tags: ["template"]
draft: true
---

> `draft: true` 상태이므로 빌드되지 않습니다.

## 1. 시나리오 / 가설

무엇을 찾으려 하는가, 어떤 가설을 검증하는가.

## 2. 환경 / 증거물

- 이미지: `disk.E01`, `memory.raw`
- 도구: Autopsy, Volatility 3, FTK Imager, ...

## 3. 타임라인

| 시각 (UTC)          | 출처            | 이벤트                    |
|--------------------|-----------------|--------------------------|
| 2026-06-01 12:00   | Prefetch        | `evil.exe` first exec    |
| 2026-06-01 12:01   | NTUSER UserAssist | ...                     |

## 4. 분석 / 발견

핵심 아티팩트, 도출 근거.

## 5. 결론

가설 확인/기각.
