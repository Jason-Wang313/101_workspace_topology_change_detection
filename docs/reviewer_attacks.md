# Reviewer Attacks

1. The topology-change families are hand-designed and not calibrated from real robot logs.
2. The proposed detector is an executable proxy, not a trained graph model.
3. Topological SLAM/TAMP and dynamic scene-graph systems may close the gap under real data.
4. Detection F1 is useful, but reviewers will demand real closed-loop rollouts.
5. The oracle gap remains large: `0.677` proposed success versus `0.829` oracle success under combined stress.
6. Replanning cost is abstract rather than measured wall-clock robot time.
7. The paper still needs a full manual related-work synthesis.

Response after v4.1: keep the paper as STRONG_REVISE because the local topology-change mechanism reproduced, but do not submit it without external validation.
