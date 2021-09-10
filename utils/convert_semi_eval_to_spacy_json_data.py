'''Convert SemiEval BanglaNER dataset to spacy BLIOU json format
'''
import os
import json

from spacy.training.iob_utils import iob_to_biluo


def update_iob_tags_with_biluo_tags(tokens):
    # convert iob tokens to biluo formats
    token_ner_iob_tags = []
    for token in tokens:
        ner_tag = token['ner']
        token_ner_iob_tags.append(ner_tag)
    
    token_ner_biluo_tags = iob_to_biluo(token_ner_iob_tags)
    for token, bilou_tag in zip(tokens, token_ner_biluo_tags):
        token['ner'] = bilou_tag

    return tokens


def get_spacy_json_data_template(id, tokens):
    '''Return standered spacy data formate for a single data point'''
    return {
            "id": id,
            "paragraphs": [{
                "sentences": [{
                    "tokens": tokens
                }]
            }]
        }


def conll_to_bliou_format(conll_file, bliou_file, save_at='data'):
    '''Convert CONLL to BLIOU and save bliou file to disk
    Args:
        conll_file (str): path to iob file
        bliou_file (str): bliou file name
        save_at: where you want to save your file
    Returens:
        None
    '''
    os.makedirs(save_at, exist_ok=True)
    with open(conll_file, 'r') as fp:
        data = fp.readlines()
    
    tokens = []
    data_id = 0
    spacy_json_data = []
    unique_tags = set()
    for line in data:
        if line.startswith("# id"):
            # this is a new sentences
            if tokens:
                tokens = update_iob_tags_with_biluo_tags(tokens)
                sentence_json_data = get_spacy_json_data_template(
                    id=data_id, tokens=tokens
                )
                spacy_json_data.append(sentence_json_data)
                data_id += 1
            # reset tokens list
            tokens = []
        else:
            line = line.strip('\n')
            line = line.strip()
            if not line:
                continue
            text,_, _,tag = line.split(' ')
            unique_tags.add(tag)
            tokens.append({
                "orth": text,
                "tag": "-",
                "ner": tag
            })
    bliou_file = os.path.join(save_at, bliou_file)
    with open(bliou_file, 'w') as fp:
        json.dump(spacy_json_data, fp, indent=2, ensure_ascii=False)
        print(f"File save at: {bliou_file}")
    print(f"Unique tags: {unique_tags}")


if __name__ == "__main__":
    train_data_path = 'data/SemiEval/SemEval2022-Task11_Train-Dev/BN-Bangla/bn_train.conll'
    dev_data_path = 'data/SemiEval/SemEval2022-Task11_Train-Dev/BN-Bangla/bn_dev.conll'

    conll_to_bliou_format(
        conll_file=dev_data_path,
        bliou_file='bn_dev.json',
        save_at='data/SemiEval/SemEval2022-Task11_Train-Dev/BN-Bangla'
    )

    conll_to_bliou_format(
        conll_file=train_data_path,
        bliou_file='bn_train.json',
        save_at='data/SemiEval/SemEval2022-Task11_Train-Dev/BN-Bangla'
    )