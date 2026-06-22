# Paper 101 Terminal Audit 2026-06-22

Paper: 101 workspace_topology_change_detection

Version: v5 expanded

Terminal decision: STRONG_REVISE

ICLR-main readiness: no

GitHub: `https://github.com/Jason-Wang313/101_workspace_topology_change_detection`

Canonical PDF: `C:/Users/wangz/Downloads/101.pdf`

PDF SHA256: `23709308E051A0E8AE6707EB14136BFB03AE954816511854137ABDBBF7ECBB92`

Pages: 25

## Verification Summary

- The v5 runner completed and wrote all expected CSV, table, figure, and manuscript artifacts.
- The manuscript compiled to a 25-page PDF.
- Citation links use visible boxed borders and route to the reference section.
- The canonical numbered PDF is in Downloads only.
- No Desktop PDF is part of the artifact.
- No repo-local `101.pdf` is required or retained.

## Evidence Summary

- Main closed-loop rollouts: 345,600.
- Ablation rollouts: 115,200.
- Stress-sweep rollouts: 288,000.
- Fixed-risk rollouts: 276,480.
- Negative cases: 24.
- v5 hard success: `0.80095`.
- strongest non-oracle hard success: `0.67222`.
- topological SLAM/TAMP hard success: `0.55191`.
- oracle hard success: `0.90486`.
- v5 fixed-risk strict coverage: `1.00000`.

## Honest Scope Decision

The artifact is a strong local submission package, not a main-conference-ready robotics paper. The scope gate fails because the repository contains no real robot validation, accepted external benchmark validation, calibrated topology-change logs, trained checkpoint, videos, or complete manual related-work synthesis.
