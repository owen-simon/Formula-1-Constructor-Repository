# Forumla One Constructor Championship Predictions 🏎️

## Introduction

Formula One teams analyze massive volumes of data to design, develop, and optimize cars capable of winning the World Constructors’ Championship. While much of this data remains proprietary, historical trends still provide valuable insight into team performance.

This project builds a predictive model using over two decades of constructor-level data to forecast the Formula One Constructors’ Champion before the season begins.

## Data Description

This dataset contains constructor-level seasonal performance data from the Formula One World Championship spanning 2002 to the present.

The 2002 season was selected as the starting point because it is the first year in which all competing constructors are consistently recorded in official championship standings published by the Formula One Group.

The objective of this dataset is to predict the winner of the Constructors’ Championship. The target variable is `Constructor_Champion`, a binary indicator of whether a constructor won the championship in a given season.

## Data Sources

Seasonal constructor entry and results data were collected from official championship records and supplemented with historical data from external sources:  
- [Formula 1 Results](https://www.formula1.com/en/results.html)
- [F1 Fansite](https://www.f1-fansite.com/)

Constructor lineage, branding continuity, and ownership transitions were compiled using documentation from the Fédération Internationale de l’Automobile (FIA) and compared against the Formula 1 Lineage Project:
- [Formula 1 Lineage Project](https://flamingtempura.github.io/formula1-lineage/)

## Repo Files

- `Data_Dictionary.xlsx`: Definitions and descriptions of all variables used in the dataset.
- `Data Files/`
  - `Driver_Experience.xlsx`: Historical race start totals for drivers competing since 2002.
  - `Laps_Completed.xlsx`: Historical lap counts for drivers competing since 2002.
  - `raw_data_2026.csv`: Constructor-level dataset spanning 2002 through 2026 prior to preprocessing.
- `Feature_Engineering.py`: Script used to clean, transform, and engineer features from the raw dataset, including creation of model-ready training and test sets.
