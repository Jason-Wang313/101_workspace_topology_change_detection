# 101 Workspace Topology Change Detection

Submission-hardening version: v4

Terminal decision: STRONG_REVISE for an ICLR-main-target project, not submission-ready.

Paper 101 was rebuilt from a template archive into a topology-change benchmark for contact-rich and mobile manipulation. The v4 evidence supports the local mechanism: action-conditioned topology-change detection improves success, invalid-plan rate, collision/trap rate, support-failure rate, topology F1, and detection latency relative to the strongest non-oracle baseline, `topological_slam_tamp`.

## Key Evidence

- Benchmark design: 5 tasks x 7 topology-change families x 5 splits x 9 methods.
- Seeds: 7 independent seeds, 84 episodes per method/task/family/split/seed group.
- Strongest non-oracle baseline: `topological_slam_tamp`.
- Combined stress: proposed success `0.677 +/- 0.006`; strongest baseline success `0.564 +/- 0.005`.
- Safety: proposed invalid-plan `0.310`, collision/trap `0.188`, support failure `0.093`; all below the strongest baseline.
- Diagnostics: proposed topology F1 `0.635` and latency `0.565`; strongest baseline topology F1 `0.493` and latency `0.685`.
- Ablation gate: full method success `0.680`; best removed-component ablation `minus_replan_hysteresis` success `0.622`.

## Reproduce Evidence

```powershell
python src\run_experiment.py
```

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/101.pdf`

## Honest Limitation

This is a strong local audit, not a submission-ready robotics result. Revival requires real robot or accepted external benchmark validation, calibrated topology-change events, rollout videos, and deeper manual related work.
