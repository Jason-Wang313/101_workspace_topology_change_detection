# Submission Version Log

## v1

Generated draft and repository scaffold.

## v2

Initial hardening pass.

## v3

ICLR-main gate archive. Decision: KILL_ARCHIVE because evidence was synthetic/template-only.

## v4

Paper-specific topology-change evidence rebuild. Added deterministic NumPy benchmark, strong baselines, ablations, stress sweep, pairwise seed tests, generated figures, LaTeX tables, failure cases, rewritten docs, and a new manuscript. Decision changed to STRONG_REVISE because the local mechanism was supported, while submission readiness remained blocked by missing external robotics validation.

## v4.1

Added a pre-execution ICLR-main submission-readiness plan for Paper 101, reran the local benchmark on 2026-06-15, and reconfirmed STRONG_REVISE.

## v5 expanded

- Added a frozen hostile-review plan for a 25-page submission artifact.
- Expanded the benchmark to 6 tasks x 8 topology-change regimes x 8 splits x 15 methods x 10 seeds x 6 episodes per cell.
- Produced 345,600 main rollouts, 115,200 ablation rollouts, 288,000 stress rollouts, 276,480 fixed-risk rollouts, and 24 negative cases.
- Added v5 method `risk_calibrated_topology_belief_v5` with calibration, active topology probing, fixed-risk reporting, support-edge memory, passage homology, occlusion persistence, action conditioning, and replan hysteresis.
- Added strong baselines including conformal topology risk filtering, particle-filter topology belief MPC, dynamic scene-graph transformer proxy, neural TAMP replanning, active view topology probing, v4 detector, and oracle.
- Generated a 25-page PDF at `C:/Users/wangz/Downloads/101.pdf` with SHA256 `23709308E051A0E8AE6707EB14136BFB03AE954816511854137ABDBBF7ECBB92`.
- Added bright boxed citation hyperlinks and 230 bibliography entries selected from the local deep-read pool.
- Terminal decision: STRONG_REVISE, still not ICLR-main ready without external robot or accepted benchmark validation.
