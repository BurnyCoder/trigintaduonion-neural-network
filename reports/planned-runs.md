# Run matrix

| Stage | Models and data | Budget and endpoint |
|---|---|---|
| Pilot | Canonical scene network, canonical sensor, seed 42. Constant prediction and generating-rule oracle. | 1,024 parent pairs, 80 epochs. Validate checkpoints and classify unseen pilot pairs. |
| Primary | C and R learners × C and R sensors. | Seeds 0–7, shared schedules. Differences and thresholds in the preregistration. |
| Controls | Frozen encoder, one-hop, shallow set, full-width real, budget-matched real, CD16. | On C scenes. Frozen, one-hop and shallow use all eight seeds for the depth comparison. Strong real and CD16 baselines use seeds 0–2 descriptively. |
| Sensitivity | C and R learners on C scenes with 256, 4,096 and 32,768 training families. | Seed 0, same architecture and epoch limit. Raw curves and computational cost. |
| Algebra | Hidden left multiplier with 2, 8, 32, 128 training vectors. CD32, randomized and unrestricted fits on both teachers. Blind bilinear fit with 256, 1,024, 2,048 Gaussian pairs. | Independent fresh inputs. Target-energy-normalized squared error. Predict matching error below 0.0001 at eight examples and advantage reversal. At 2,048 pairs require all ordered basis products to have correct component and sign plus error below 0.0001. Include shuffled target and exact reference. |
| Superpixels | Same distance-message blocks with RGB node adapter, symmetric graph pool, ten-class head on published CIFAR-10 graphs. | Seed 0, C/R, 60 epochs. Published splits. |
| Natural images | Three RGB residual stages of widths 32, 64, 128, two convolutions per stage. C versus R, full-width real, count-matched real and CD16. | Eight C/R pairs, three seeds for comparative baselines, batch 128, 60 epochs SGD 0.1, momentum 0.9, weight decay 0.0005, cosine decay. Hash-grouped stratified training/validation, ciFAIR-10 primary, original CIFAR-10 secondary. |

The primary graph budget is intended to expose low-data behavior and fit the laptop. Both test mates count as one family for splitting. Reserve one week for training. Check longer jobs at 5, 15 or 30 minutes once their expected duration exceeds 10, 30 or 60 minutes respectively. Record hardware throughput and update ETA from actual runs.
