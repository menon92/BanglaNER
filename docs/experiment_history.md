# Experiment gist with F1 score status

### Experiment - 1
- Clean raw data
- Convert all the clean data to spacy format
- Merge different data source into one data soruce
- Total data found `9985`
- Split data into train, validation
  - 90% training data
  - 10% validation data
- Taining spacy model
- Best `score 0.66` on validation data

### Experiment - 2
- User external [word vector](https://drive.google.com/file/d/1cQ8AoSdiX5ATYOzcTjCqpLCV1efB9QzT/view)
  - Vectore is trained on wiki data
- Taining spacy model `score 0.66`

### Experiment - 3
- Create a custom tok2vec using SpaCy tok2vec pipeline
  - Vectore trained on `9985` data
- Taining spacy model `score 0.66`

### Experiment - 4
- Dataset `EDA`
- Take data sample which contain name entiry
- Discard sample that contain no name entiry
- Total this kinds of data found 2895
- Split into train validation
    - Train sample 2605
    - Validation sample 290
- Taining spacy model `score 0.69`

### Experiment - 5
- Transformer multilingual bert
- Total data 9985
- Taining spacy transformer model `score 0.80`
- Experiment is done in `kaggle notebook gpu enable`
```