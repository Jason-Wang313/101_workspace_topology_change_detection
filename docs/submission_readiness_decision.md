# Submission Readiness Decision

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

The v5 expanded rebuild executed a frozen, paper-specific workspace-topology benchmark. It includes strong baselines, ablations, stress tests, fixed-risk tests, seed uncertainty, pairwise comparisons, failure cases, generated figures, generated tables, a 25-page manuscript, and reproducible code. The local evidence supports the mechanism against every non-oracle baseline.

Reproduced local gates:

- Success gate: proposed v5 success `0.80095 +/- 0.00707` vs `0.67222 +/- 0.00988` for the strongest non-oracle reference and `0.55191 +/- 0.01402` for topological SLAM/TAMP.
- Safety gate: proposed invalid-plan `0.14149`, collision/trap `0.03385`, and support failure `0.01424`, all below the strongest non-oracle reference.
- Diagnostic gate: proposed topology F1 `0.74339`, missed-change false negative rate `0.36731`, false-alarm rate `0.14104`, and detection latency `0.61527`.
- Calibration gate: proposed ECE `0.18972`, below the strongest non-oracle reference ECE `0.32219`.
- Pairwise gate: proposed v5 beats all non-oracle baselines and trails only the oracle.
- Utility/regret gate: proposed utility `0.43639` and regret `0.10391`.
- Ablation gate: full v5 success `0.79583` vs best removed-component ablation `0.73429`.
- Fixed-risk gate: strict coverage `1.00000`, success `0.79427`, collision/trap `0.03351`, support failure `0.01215`, utility `0.43183`.
- Scope gate: failed.

The paper is not submission-ready because validation remains local. It still lacks real-robot deployment, accepted external benchmark comparison, calibrated topology-change logs, trained model checkpoints, videos, and a full manual related-work synthesis.

Honest terminal action: keep as STRONG_REVISE. Do not submit to ICLR main until external empirical validation exists.
