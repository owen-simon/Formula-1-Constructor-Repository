# Forumla One Constructor Championship Predictions 🏎️

## Data Description
This dataset contains constructor-level seasonal performance data from the Formula One World Championship, from 2002 to the present.

The 2002 season was selected as the starting point because it represents the first year in which all competing constructors are consistently listed in the official championship standings published by the Formula One Group.

The purpose of this data is to predict the winner of the Formula One Constructor's Championship. The target variable is `Constructor_Champion`.

## Data Sources

Seasonal constructor entry and results data were collected from official championship records published by the Formula One Group, as well as fan-curated historical data:  
- [Formula 1 Results](https://www.formula1.com/en/results.html)
- [F1 Fansite](https://www.f1-fansite.com/)

Constructor branding continuity, ownership transitions, and historical lineage relationships were compiled using documentation from the Fédération Internationale de l'Automobile in conjunction with the Formula 1 Lineage Project:
- [Formula 1 Lineage Project](https://flamingtempura.github.io/formula1-lineage/)

## Data Files

- `Data_Dictionary.xlsx`: Provides definitions and descriptions for all variables used in the dataset.
- `Data Files/`
  - `Driver_Experience.xlsx`: Contains historical race start totals for each driver who has competed since the 2002 season.
  - `Laps_Completed.xlsx`: Contains historical lap counts for each driver who has competed since the 2002 season.
  - `Train.csv`: Team-level historical data from the 2002 through 2025 seasons used for model training.
  - `Test.csv`: Team-level constructor data for the 2026 season used for out-of-sample prediction.
