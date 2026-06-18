---
type: Watchlist
title: Stage 4 Monitor
description: Elements and architectural decisions to keep an eye on from Stage 4.
tags: [watchlist, valuation, caching, stage4]
timestamp: 2026-06-17
---

# Stage 4 Monitor

This document tracks alternative options and potential performance bottlenecks that were accepted for the Stage 4 implementation but should be monitored over time.

## 1. Valuation Formula
- **Current Approach:** We rank targets by efficiency/ROI (`production / cost`), while filtering out targets where the cost exceeds our available ships.
- **Alternative to Monitor:** Absolute Net Value (`production - cost`). If the ROI approach leads to ignoring high-cost, high-reward planets that are strategically necessary, we may need to pivot to absolute net value or a hybrid score.

## 2. Reachable Cache
- **Current Approach:** `reachable()` calculates the reachability race. Since calculating this for both players on every planet per turn is an $O(P^2 \times T)$ operation, we have opted to **cache** the `reachable` results to avoid performance regressions during target valuation.
- **To Monitor:** The memory overhead and cache invalidation complexity of this cache. If memory becomes an issue or if the cache is constantly invalidated by hypothetical timeline perturbations, we may need to fall back to a simplified heuristic for hold probability rather than running the full exact `reachable` check.
