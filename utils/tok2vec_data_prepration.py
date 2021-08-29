'''This scrip take input bliou json file and
convert it to SpaCy supported jsonl file so that 
we can train SpaCy tok2vec model

jsonl data format,
```
{"text": "Can I ask where you work now and what you do, and if you enjoy it?"}
{"text": "They may just pull out of the Seattle market completely, at least until they have autonomous vehicles."}
```

Trainin command tok2vec model using spacy
python -m spacy pretrain config.cfg ./output_pretrain --paths.raw_text ./data.jsonl
'''
import json


data_file = 'data/merge_all_data_and_main_jsonl.json'
tok2vec_jsonl_file = "data/tok2vec_jsonl_file.jsonl"

with open(data_file, 'r') as fp:
    data = json.load(fp)

jsonl_data = []
for d in data:
    sentence_tokens = d["paragraphs"][0]["sentences"][0]["tokens"]
    text = []
    for token in sentence_tokens:
        text.append(token["orth"])
    sentence = ' '.join(text)
    jsonl_data.append({"text": sentence})

with open(tok2vec_jsonl_file, 'w') as fp:
    for d in jsonl_data:
        json.dump(d, fp, ensure_ascii=False)
        fp.write("\n")
