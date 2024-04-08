# Classic Q-table Bot
## V1
1mil games AI vs AI. Learning rate 0.1, greed 0.5, 
Win rate vs Random is good for P1. For P2 losses are more noticeable, due likely to just first turn advantage.
High record vs random sort of hides its failure during decisive scenarios, which will come up during most human vs bot games.

Diminishing returns after 1 mil training.

Adjusting greed higher than 0.5 (epsilon lower) seems to produce worse results.

Bot parameters can be adjusted separately. Notes are so far mostly based on bot mirror pvp.

Ideas for improvement:
- Batched learning
- Replay memory
- Double Q Learning
- Back propagating game results

## V2 Back prop
Results are surprisingly worse for player two with backprop. Against an AI player, the results are worse than training vs Random.

## V3
Setting tie reward to something high seems to fix the rest of player 2 issues. Seems to be consistently 0 losses to random.

# Neural Network Bot
