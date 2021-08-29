# BanglaNER
Bangla Name Entity Recognition (`NER`) using [SpaCy](https://spacy.io/). NER from bangla input text sentences. Experiment is done only using one entity name (`person`) label as `PER`

Perform 5 different experiment this this data and foud that transformer base model perform better compare to other model. Please check the experimental detail and `F1 score` in [experimental history](./docs/experiment_history.md). Where best `F1 score ~.80`

Bangla NER data is collected from, 
- [Rifat1493/Bengali-NER](https://raw.githubusercontent.com/Rifat1493/Bengali-NER/master/all_data.txt)
- [banglakit/bengali-ner-data](https://raw.githubusercontent.com/banglakit/bengali-ner-data/master/main.jsonl)

### Dependency
```bash
conda install spacy=3.1
pip install spacy-transformers # need if you want to use transformer 
```

### Data prepration
1. Clean IOB and remove data which is in wrong IOB format

#### Data conversion command (Optional)
1. IOB to spacy `.spacy` data format in in SpaCy3.x
    - `python -m spacy convert -c iob -s -n 1 ner-token-per-line.iob ./data`
    - [Example SpaCy json data](https://github.com/explosion/spaCy/blob/v2.3.5/examples/training/ner_example_data/ner-token-per-line.json)
2. Convert `BLIOU` json format to `.spacy` data format
    `python -m spacy convert train.json ./data`

#### Automate data prepration
1. To automate data prepration just run,
```bash
python utils/convert_to_spacy_json_format.py
```
This scrip will generate `data/train.json`, `data/val.json`

2. Convert json data to `.spacy` data
```sh
python -m spacy convert data/train.json ./data
python -m spacy convert data/val.json ./data
```
Above two command will generate `data/train.spacy`, and `data/val.spacy`

### Training & inferance of SpaCy Transition base model

#### Training 
#### Create base config file

Go to the [link](https://spacy.io/usage/training#config) and create a base config file and save it uinder `./configs/base_config.cfg`

![](./docs/images/spacy_base_config_file.png)

#### Prepare configuration files
Now convert `./configs/base_config.cfg` to config file `./configs/config.cfg`

```
python -m spacy init fill-config configs/base_config.cfg configs/config.cfg
```

#### Start training
```bash
python -m spacy train configs/config.cfg \
    --output ./models \
    --paths.train ./data/train.spacy \
    --paths.dev ./data/val.spacy
```
You will get F1 score on val data around `0.66`

#### Inferance
For inferance please run,
```bash
python test.py
```
You can already pretrain model in `test.py`. Please download the pretrain model from [google drive (4.4MB)](https://drive.google.com/file/d/1IqF87JGlClqPsU7I7Et5lvi_BZksnKDl/view?usp=sharing) and set the model path in `test.py` file


### Training and inferance SpaCy transformer pipeline
To training spacy transformer model please check `need GPU`,

[Transformer training and inferance guide](./transformers/readme.md)

You will get F1 score on val data around `0.80`


#### Transformer based model sample output

if you want to use already trained model please download pretrain model from [google drive (622.8MB)](https://drive.google.com/file/d/1kGBfAOvazd7w0BJKADUDfbvdum7JqRNh/view?usp=sharing) and set the model path in `test.py` file

```python
import spacy

nlp = spacy.load("./models_multilingual_bert/model-best")

text_list = [
    "আব্দুর রহিম নামের কাস্টমারকে একশ টাকা বাকি দিলাম",
    "১০০ টাকা জমা দিয়েছেন কবির",
    "ডিপিডিসির স্পেশাল টাস্কফোর্সের প্রধান মুনীর চৌধুরী জানান",
    "অগ্রণী ব্যাংকের জ্যেষ্ঠ কর্মকর্তা পদে নিয়োগ পরীক্ষার প্রশ্নপত্র ফাঁসের অভিযোগ উঠেছে।",
    "সে আজকে ঢাকা যাবে",
]
for text in text_list:
    doc = nlp(text)

    print(f"Input: {text}")
    for entity in doc.ents:
        print(f"Entity: {entity.text}, Label: {entity.label_}")
    print("---")

# Outputs
    Input: আব্দুর রহিম নামের কাস্টমারকে একশ টাকা বাকি দিলাম
    Entity: আব্দুর রহিম, Label: PER
    ---
    Input: ১০০ টাকা জমা দিয়েছেন কবির
    Entity: কবির, Label: PER
    ---
    Input: ডিপিডিসির স্পেশাল টাস্কফোর্সের প্রধান মুনীর চৌধুরী জানান
    Entity: মুনীর চৌধুরী, Label: PER
    ---
    Input: অগ্রণী ব্যাংকের জ্যেষ্ঠ কর্মকর্তা পদে নিয়োগ পরীক্ষার প্রশ্নপত্র ফাঁসের অভিযোগ উঠেছে।
    ---
    Input: সে আজকে ঢাকা যাবে
    ---
```

### Trainng Tok2Vec model
#### Data format
```
{"text": "Can I ask where you work now and what you do, and if you enjoy it?"}
{"text": "They may just pull out of the Seattle market completely, at least until they have autonomous vehicles."}
```

python -m spacy pretrain config.cfg ./output_pretrain --paths.raw_text ./data.jsonl

### Init pretrain vector file
```bash
    python -m spacy init vectors bn pretrain_vectors/bangla_word2vec_gen4/bangla_word2vec/bnwiki_word2vec.vector pretrain_vectors/bangla_word2vec_gen4/bangla_word2vec_spacy --verbose
```

### NER Data formats
```
BLIOU data format meaning
B = Begin
L = Last
I = Inside
O = Outside
U = Unique
```

```
IOB data format meaning
I = Inside
O = Outside
B = Begin
```

### Referance
- [BILOU data formats meaning](https://stackoverflow.com/questions/17116446what-do-the-bilou-tags-mean-in-named-entity-recognition)
- [SpaCy 3.1 data format](https://zachlim98.github.io/me/2021-03/spacy3-ner-tutorial)
- [Preparing the training data](https://spacy.io/usage/training#training-data)
- [Performance throught uncertainty](https://saxamos.github.io/2020/07/31/en-improve-spacy-performance-through-uncertainty/)
- [WikiANN model](https://huggingface.co/datasets/wikiann)
