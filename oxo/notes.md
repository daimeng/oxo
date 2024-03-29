# Classic Q-table Bot
Win rate vs Random is good for P1. For P2 losses are more noticeable, due likely to just first turn advantage.
High record vs random sort of hides its failure during decisive scenarios, which will come up during most human vs bot games.

Diminishing returns after 1 mil training.

Adjusting greed higher than 0.5 (epsilon lower) seems to produce worse results.

Bot parameters can be adjusted separately. Notes are so far mostly based on bot mirror pvp.

Ideas for improvement:
- Batched learning
- Replay memory
- Make a perfect-play rules-based bot to benchmark against

# Neural Network Bot
