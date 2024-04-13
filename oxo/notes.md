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

## Back prop
Results are surprisingly worse for player two with backprop. For player 2, training against an AI player, the results are worse than training vs Random. This may be because player 1 trains too fast

## Ties and punishment for loss
Reward for loss or ties create some interesting changes. In earlier versions there was no punishment for loss or reward for tie.

Because I never ramped greed down or up (stayed at episolon 0.5). This caused player 2 to shoot for the moon and try to get lucky wins instead of accepting a draw. Giving either a reward for tie or a punishment for loss causes player 2 to accept draws much more.

# Neural Network Bot
