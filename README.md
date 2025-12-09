# Sleep Pattern Analysis

This project analyzes the relationship between lifestyle factors, specifically smoking and alcohol consumption, and sleep patterns in adults. The goal is to identify how these habits correlate with sleep duration and quality.

## Dataset

The data used in this analysis is a merged dataset from the National Health and Nutrition Examination Survey (NHANES). The primary dataset is `merged_sleep_dataset.csv`, which contains various health, demographic, and lifestyle variables.

### Key Variables of Interest:

*   **Sleep Patterns:**
    *   `SLD012`: Average sleep duration on weekdays.
    *   `SLD013`: Average sleep duration on weekends.
    *   `SLQ050`: Felt unrested during the day.
    *   `SLQ120`: How often do you feel overly sleepy during the day.

*   **Alcohol Consumption:**
    *   `ALQ111`: Ever had a drink of any kind of alcohol.
    *   `ALQ130`: Average number of drinks on a day when drinking.

*   **Smoking Status:**
    *   `SMQ020`: Smoked at least 100 cigarettes in life.
    *   `SMQ040`: Do you now smoke cigarettes.

*   **Demographics:**
    *   `DMDEDUC2`: Education level.
    *   `RIAGENDR`: Gender.
    *   `RIDAGEYR`: Age in years.

## Analysis

The analysis is performed in the `merge_nhanes.py` script. This script loads the raw NHANES data, merges the relevant datasets, cleans the data, and performs statistical analysis to explore the relationship between sleep patterns and the variables of interest.

## Usage



To run the analysis, execute the following command:



```bash

python merge_nhanes.py

```



## NHANES Data Usage Policy



The data used in this project is from the National Health and Nutrition Examination Survey (NHANES), which is a program of the National Center for Health Statistics (NCHS), part of the Centers for Disease Control and Prevention (CDC).



The use of NHANES data is subject to the following policy:

1.  The data is to be used for statistical reporting and analysis only.

2.  Any attempt to identify individual participants is strictly prohibited and against the law.

3.  The confidentiality of all participants must be maintained.



For more information, please refer to the official [NHANES website](https://www.cdc.gov/nchs/nhanes/index.htm).
