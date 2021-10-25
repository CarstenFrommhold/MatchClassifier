# MatchClassifier

Predictions of football matches for the german bundesliga.

## Benchmark

Newer seasons contain B365 odd data which one can use to create some benchmark metrics.
Note that the calculation of metrics given those odds leads to a little bias. 
One reaches propabilities via the reciprocal value of the odds. 
In a fair setup, they would sum up to 1. Since they do not (the betting provider earns in any case), 
they are corrected in the benchmark calculation. The simple normalization is an assumption made here.
One would expect that the odd manipulation by the betting provider follow some optimization rules given customer specific betting behaviour.

Season | Accuracy | Precision |  AUC
--- | --- | --- | --- | 
18/19 | 0.542 | 0.729 | 0.662
19/20 | 0.52 | 0.698 | 0.654
20/21 | 0.513 | 0.699 | 0.681

One observes a soothing result: These values are not outstanding.

## Development

* Resolve cold start problem for the first matchdays.

### Feature Ideas

* trend given the last n matches
* clubs master data like members, age, stadium capacity -> embedding
* last match between two teams

## Notes

* Home advantage is implicit in the modeling because the variables are set sensitive to home and away position.