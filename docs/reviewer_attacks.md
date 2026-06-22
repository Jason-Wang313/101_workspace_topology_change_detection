# Reviewer Attacks

1. The topology-change regimes are hand-designed and not calibrated from real robot logs.
2. The proposed detector is still an executable proxy, not a trained graph model with released checkpoints.
3. Topological SLAM/TAMP and dynamic scene-graph systems may close the gap under real data.
4. Detection F1 is useful, but reviewers will demand real closed-loop robot rollouts.
5. The oracle gap remains material: `0.80095` proposed success versus `0.90486` oracle success.
6. Replanning cost is abstract rather than measured wall-clock robot time.
7. The paper still needs a full manual related-work synthesis.
8. The benchmark is large, but still local; reviewers can attack domain transfer.
9. The fixed-risk audit is local and does not certify safety on hardware.

Response after v5: keep the paper as STRONG_REVISE because the local topology-belief mechanism survives a much stronger audit, but do not submit it without external validation.
