# Submission Readiness Decision

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

The v4.1 continuation rerun re-executed the paper-specific workspace-topology benchmark on 2026-06-15. It includes strong baselines, ablations, stress tests, seed uncertainty, failure cases, generated figures, generated tables, and reproducible code. The local evidence still supports the mechanism against `topological_slam_tamp`.

Reproduced local gates:

- Success gate: proposed success `0.677 +/- 0.006` vs `0.564 +/- 0.005` for `topological_slam_tamp`.
- Safety gate: proposed invalid-plan `0.310`, collision/trap `0.188`, and support failure `0.093`, all below the strongest baseline.
- Diagnostic gate: proposed topology F1 `0.635` and detection latency `0.565` vs `0.493` and `0.685` for the strongest baseline.
- Pairwise gate: proposed beats `topological_slam_tamp` by `0.114 +/- 0.006`, winning `7/7` seeds.
- Ablation gate: best removed-component ablation is `minus_replan_hysteresis` at `0.622`, below full at `0.680`.
- Stress gate: at maximum topology stress, proposed success is `0.678` vs `0.549` for `topological_slam_tamp`.

The paper is not submission-ready because validation remains local. It still lacks real-robot deployment, accepted external benchmark comparison, calibrated topology-change logs, trained model checkpoints, videos, and a full manual related-work synthesis.

Honest terminal action: keep as STRONG_REVISE. Do not submit to ICLR main until external empirical validation exists.
