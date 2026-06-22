# 101 Workspace Topology Change Detection

Submission-hardening version: v5 expanded.

Terminal decision: STRONG_REVISE for an ICLR-main-target project, not submission-ready.

Paper 101 was rebuilt into a CPU-only, RAM-light, hostile-review evidence package for action-conditioned workspace-topology belief under changing supports, passages, occlusions, reachability components, tool tunnels, and kinematic traps. The v5 audit keeps the paper alive because every frozen local empirical gate passed, but it still refuses ICLR-main readiness because the scope gate fails.

Public repository: `https://github.com/Jason-Wang313/101_workspace_topology_change_detection`

Canonical local PDF: `C:/Users/wangz/Downloads/101.pdf`

PDF SHA256: `23709308E051A0E8AE6707EB14136BFB03AE954816511854137ABDBBF7ECBB92`

Page count: 25.

## Key Evidence

- Frozen benchmark design: 6 tasks x 8 topology-change regimes x 8 splits x 15 methods x 10 seeds x 6 episodes per cell.
- Main evidence scale: 345,600 closed-loop rollout rows, 57,600 group rows, 150 seed rows, 120 method/split metric rows.
- Hard aggregate: `risk_calibrated_topology_belief_v5` success `0.80095 +/- 0.00707`, invalid-plan `0.14149`, collision/trap `0.03385`, support failure `0.01424`, topology F1 `0.74339`, ECE `0.18972`, regret `0.10391`, utility `0.43639`.
- Strongest non-oracle reference by success: `proposed_topology_change_detector_v4` success `0.67222 +/- 0.00988`, invalid-plan `0.21727`, collision/trap `0.08359`, support failure `0.02153`, topology F1 `0.64753`, ECE `0.32219`, utility `0.15822`.
- Topological SLAM/TAMP stress baseline: success `0.55191 +/- 0.01402`, invalid-plan `0.30095`, collision/trap `0.14280`, support failure `0.04922`, topology F1 `0.53063`, utility `-0.15426`.
- Oracle reference: success `0.90486 +/- 0.00460`, leaving an honest oracle gap of `0.10391`.
- Pairwise v5 success margins: `+0.12873` versus v4, `+0.24905` versus topological SLAM/TAMP, and positive against every non-oracle baseline.
- Ablation scale: 115,200 rollout rows. Full v5 success `0.79583`; best removed-component ablation `no_replan_hysteresis` success `0.73429`.
- Stress scale: 288,000 rollout rows. Fixed-risk scale: 276,480 rows. Strict fixed-risk v5 coverage `1.00000`, success `0.79427`, collision/trap `0.03351`, support failure `0.01215`, utility `0.43183`.
- Negative-case ledger: 24 curated failure cases.
- Local gates passed: success, invalid-plan, collision, support, diagnostic, latency, regret, utility, calibration, ablation, stress, and fixed-risk.
- Scope gate failed: no real robot validation, accepted high-fidelity simulator benchmark, external benchmark, calibrated external topology-change logs, trained checkpoint, or rollout videos.

## Reproduce Evidence

```powershell
python src\run_experiment.py
python scripts\generate_manuscript.py
python scripts\validate_submission_artifacts.py
```

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The manuscript uses boxed hyperlink citations so in-text citations route directly to the reference section.

## Honest Limitation

This is a rigorous local surrogate audit, not a submission-ready robotics deployment result. The paper should not be submitted to ICLR main until the same claims survive external robot or accepted benchmark validation, calibrated topology-change logs, trained-model release, videos, and deeper manual related-work synthesis.
