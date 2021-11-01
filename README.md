# MatchClassifier

- [MatchClassifier](#matchclassifier)
  * [Data](#data)
  * [Model](#model)
    + [Current model](#current-model)
    + [Benchmark](#benchmark)
  * [Next steps](#next-steps)
    + [Feature Ideas](#feature-ideas)
  * [Notes](#notes)

[twitter]: https://twitter.com/carstenfr91

This repo aims to predict odds of football matches for the german bundesliga.
Note that, at the moment, it acts as a playground to do some first steps.
To start, match outcomes should be predicted. #goals and other kpi are note taken into account so far. 
A match has three potential outcomes. The home team wins (general marked with "1"), the away team wins ("2") or a draft ("X").  
  
[<img align="left" width="20px" src="https://cdn-icons-png.flaticon.com/512/733/733579.png" />][twitter]
Odds will be twittered on every friday.


## Data

### Matches

Match result taken from [here](https://www.football-data.co.uk/).  
It will be worthy to take a look at [open data repo](https://github.com/statsbomb/open-data)

### Fifa Player Skills

* season 15-21 taken from [here](https://www.kaggle.com/stefanoleone992/fifa-21-complete-player-dataset)
* season 22 taken from [here](https://www.kaggle.com/cashncarry/fifa-22-complete-player-dataset)

Note that there exist some solutions to scrap sofifa.com, just a google search away. 

## Model

### Current model

To start, a simple decicion tree classfier is chosen. Note that no model competition, feature selection and hyperparameter tuning is done yet. Modelling steps done so far have been just by eye to get a first idea. 
The next step would be to use a specific framework to do that. 

But this already contained an interesting learning: A minimum sample leaf of 0.03 was needes to get a plausible odd for the match between Union Berlin and Bayern Munich at matchday 10: A minimal sample leaf results in odds of 2.4 | 4.0 | 3.0 to whereas a minimum of 0.03 (=55 observations) leads to odds of 11.6 | 9.67 | 1.23. The favorite won 5:2.

### Benchmark

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

## Next steps

* Search for a better model.
* Resolve cold start problem for the first matchdays.
* Adjust prepare season 19/20 -> solve covid issues. 

### Feature Ideas

* clubs master data like members, age, stadium capacity -> create embeddings
* last match between two teams (one can find [here](http://www.bulibox.de/downloads/download.html), for example)
* calculate skills based on actual first 11 players (look for data!)
* use specific fifa offensive & defensive skills 


## Notes

* Home advantage is implicit in the modeling because the variables are set sensitive to home and away position.
* It would be interesting to explicitly model it to get an insight of feature importance.
