## Training the SpaCy transformer

1. Upload you train, val data to kaggle
2. Upoad this notebook
3. Execute the notebook

Or you can directly go to [bangla ner public notebook](https://www.kaggle.com/menonbrur/spacy-transformer-bangla-ner)

This notebook contain both training and inferance code

Training log
```bash
2021-08-29 07:28:43.423139: I tensorflow/stream_executor/platform/default/dso_loader.cc:49] Successfully opened dynamic library libcudart.so.11.0
ℹ Saving to output directory: models_multilingual_bert
ℹ Using GPU: 0

=========================== Initializing pipeline ===========================
[2021-08-29 07:28:46,866] [INFO] Set up nlp object from config
[2021-08-29 07:28:46,879] [INFO] Pipeline: ['transformer', 'ner']
[2021-08-29 07:28:46,884] [INFO] Created vocabulary
[2021-08-29 07:28:46,885] [INFO] Finished initializing nlp object
Some weights of the model checkpoint at bert-base-multilingual-uncased were not used when initializing BertModel: ['cls.predictions.transform.dense.weight', 'cls.predictions.transform.LayerNorm.bias', 'cls.seq_relationship.bias', 'cls.predictions.transform.LayerNorm.weight', 'cls.predictions.decoder.weight', 'cls.seq_relationship.weight', 'cls.predictions.bias', 'cls.predictions.transform.dense.bias']
- This IS expected if you are initializing BertModel from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
- This IS NOT expected if you are initializing BertModel from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
[2021-08-29 07:29:10,646] [INFO] Initialized pipeline components: ['transformer', 'ner']
✔ Initialized pipeline

============================= Training pipeline =============================
ℹ Pipeline: ['transformer', 'ner']
ℹ Initial learn rate: 0.0
E    #       LOSS TRANS...  LOSS NER  ENTS_F  ENTS_P  ENTS_R  SCORE 
---  ------  -------------  --------  ------  ------  ------  ------
  0       0         253.19    157.43    1.41    0.79    6.85    0.01
  1     200       16986.96  23225.82   70.65   61.82   82.42    0.71
  3     400        1056.91   4223.66   75.79   72.26   79.68    0.76
  4     600         721.97   2888.16   72.91   65.23   82.65    0.73
  6     800         477.32   2034.42   76.97   73.10   81.28    0.77
  7    1000         382.41   1706.97   77.17   77.17   77.17    0.77
  9    1200         333.42   1508.52   75.12   80.63   70.32    0.75
 10    1400         284.51   1347.13   73.97   79.17   69.41    0.74
 12    1600         243.10   1180.03   76.20   76.38   76.03    0.76
 13    1800         229.68   1152.56   73.04   78.84   68.04    0.73
 15    2000         219.99   1088.95   74.20   77.42   71.23    0.74
 17    2200         198.61   1054.74   74.59   76.19   73.06    0.75
 18    2400         184.80   1005.88   70.90   76.32   66.21    0.71
 20    2600         170.58    939.51   78.36   78.18   78.54    0.78
 21    2800         157.75    899.26   77.62   79.29   76.03    0.78
 23    3000         168.71    921.55   75.60   80.26   71.46    0.76
 24    3200         145.18    855.08   74.41   77.34   71.69    0.74
 26    3400         137.02    815.80   76.80   79.32   74.43    0.77
 27    3600         149.18    842.57   74.44   76.89   72.15    0.74
 29    3800         148.89    855.05   75.21   77.48   73.06    0.75
 31    4000         141.55    806.16   74.21   83.67   66.67    0.74
 32    4200         140.30    834.55   76.49   78.42   74.66    0.76
✔ Saved pipeline to output directory
models_multilingual_bert/model-last
```
