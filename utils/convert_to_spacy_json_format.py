import os
import json
import random

from spacy.training.iob_utils import iob_to_biluo

from tokenizer import BasicTokenizer


supported_entity_tags_iob = {'O', 'I-PER', 'B-PER'}
# tags outside this will be label as 'O' tag
supported_entity_tags_bliou = {'O', 'I-PER', 'B-PER', 'U-PER', 'L-PER'}


def text_to_iob_clean_format(text_file, iob_file, save_at='data'):
    '''Text data source which is in iob format clean it and save it as iob
    file format and keep only supported tags
    Arge:
        text_flie (str): file path of iob format text data file
        iob_file (str): clean iob file name
        save_at: where you want to save your file
    Returens:
        None
    '''
    os.makedirs(save_at, exist_ok=True)
    iob_data = []
    unique_tags = set()
    with open(text_file, 'r', encoding='utf8') as f:
        data = f.readlines()
        for line in data:
            line = line.strip()
            line = line.strip('\n')
            
            # skip blank lines and invalid data sample
            if not line or len(line.split('\t')) != 2:
                iob_data.append('\n')
                continue
            
            # take text and entity tag name
            text, tag = line.split('\t')
            if text and tag:
                unique_tags.add(tag)
                if tag not in supported_entity_tags_iob:
                    tag = 'O'
                iob_data.append(text + '\t' + tag)

    print("Total lines:", len(iob_data))
    print("Unique tags are:", unique_tags)

    iob_file = os.path.join(save_at, iob_file)
    with open(iob_file, 'w') as f:
        for line in iob_data:
            # keep one newline after each sentence
            if line != '\n':
                f.write(line + '\n')
            else: f.write(line)
        print(f"IOB data save at {iob_file}")


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


def iob_to_bliou_format(iob_file, bliou_file, save_at='data'):
    '''Convert IOB to BLIOU and save bliou file to disk
    Args:
        iob_file (str): path to iob file
        bliou_file (str): bliou file name
        save_at: where you want to save your file
    Returens:
        None
    '''
    os.makedirs(save_at, exist_ok=True)
    with open(iob_file, 'r') as fp:
        data = fp.readlines()
    
    spacy_json_data = []
    tokens = []
    data_id = 0
    for line in data:
        if line == '\n':
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
            text, tag = line.split('\t')
            tokens.append({
                "orth": text,
                "tag": "-",
                "ner": tag
            })
    bliou_file = os.path.join(save_at, bliou_file)
    with open(bliou_file, 'w') as fp:
        json.dump(spacy_json_data, fp, indent=2, ensure_ascii=False)
        print(f"File save at: {bliou_file}")


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


def jsonl_to_clean_bliou_format(jsonl_file, bliou_file, save_at='data'):
    '''Clean the jsonl bliou file and filter it by supported tags
    and seve bliou file to disk
    Args:
        jsonl_file (str): path to jsonl file
        bliou_file (str): bliou_file name
        save_at (str): where file will save
    Returns:
        None
    '''
    os.makedirs(save_at, exist_ok=True)
    bst = BasicTokenizer()

    with open(jsonl_file, 'r', encoding='utf8') as fp:
        lines = fp.readlines()
    
    biluo_data = []
    unique_tags = set()
    miss_match_labels = 0
    for line in lines:
        line = json.loads(line)
        text, labels = line[0], line[1]
        tokens = bst.tokenize(text)

        # skip data samples which has issue with token vs label tag
        if len(tokens) != len(labels):
            # print(tokens, 'length:', len(tokens))
            # print(labels, 'length:', len(labels))
            # print('---')
            miss_match_labels += 1
            continue

        bilou_to_iob_labels = []
        for tag in labels:
            # store unique tag
            unique_tags.add(tag)

            # map PERSON with PER tag
            if 'PERSON' in tag:
                tag = tag.replace('PERSON', 'PER')

            if tag not in supported_entity_tags_bliou:
                tag = 'O'
            
            bilou_to_iob_labels.append(tag)
        
        sentences = []
        for token, tag in zip(tokens, bilou_to_iob_labels):
            sentences.append(token + '\t' + tag)
        biluo_data.append(sentences)
        
    bliou_file = os.path.join(save_at, bliou_file)
    with open(bliou_file, 'w') as fp:
        for sentence in biluo_data:
            # print("sentence", sentence)
            fp.write('\n'.join(sentence))
            # keep one new line after each sentence
            fp.write('\n\n')
        print(f'jsonl data source iob file save at: {bliou_file}')
    
    print(f"Found miss-match labels {miss_match_labels} of total {len(lines)}")
    print(f"Unique tags: {unique_tags}")


def merge_bliou_json_files(bliou_json_files, merge_file, save_at='data'):
    '''Merge two bliou json file into one file
    Args:
        bliou_json_files (list): list of bliou json file paths
        merge_file (str): merge file name
        save_at (str): where file will save
    Returns:
        None
    '''
    merge_data = []
    id_cnt = 0
    for file_name in bliou_json_files:
        print(f"Processing {file_name}")
        with open(file_name, 'r') as fp:
            data = json.load(fp)
        
        for d in data:
            d['id'] = id_cnt
            id_cnt += 1
            merge_data.append(d)

    merge_file = os.path.join(save_at, merge_file)
    with open(merge_file, 'w') as fp:
        json.dump(merge_data, fp, indent=2, ensure_ascii=False)
        print(f"Merge file save at: {merge_file}")
    
    print("Total data samples:", id_cnt)


def split_data_to_train_val(
    file_name, n_shuffle=7, train_percentage=0.9,
    train_file='train.json', val_file='val.json', save_at='data'
):
    '''
    Split merge data into train and validation
    file_name (str): name of file
    n_shuffle (int): number of time you want to shuffle your data
    train_percentage (float): train data percentag
    train_file (str): train data file name
    val_file (str): validation data file name
    save_at (str): where file will save
    '''
    os.makedirs(save_at, exist_ok=True)
    
    with open(file_name, 'r') as fp:
        data = json.load(fp)
    
    for i in range(n_shuffle):
        print(f'Shuffling data ... {i+1} times')
        random.shuffle(data)
    print("Shuffle done ...")

    total_data = len(data)
    train_split = int(total_data * train_percentage)
    train_data = data[:train_split]
    val_data = data[train_split:]

    # save data to json
    train_file = os.path.join(save_at, train_file)
    with open(train_file, 'w') as fp:
        json.dump(train_data, fp, indent=2, ensure_ascii=False)
        print(f'Train file save at: {train_file}')
    
    val_file = os.path.join(save_at, val_file)
    with open(val_file, 'w') as fp:
        json.dump(val_data, fp, indent=2, ensure_ascii=False)
        print(f"Val file save at: {val_file}")
    
    print(f"Total train data: {len(train_data)}")
    print(f"Validation data: {len(val_data)}")


if __name__ == "__main__":
    # ---- Preprocess all_data.txt ----
    # 1. Clean iob raw dataset
    text_file = 'data/all_data.txt'
    iob_file = 'all_data_iob_file.iob'
    text_to_iob_clean_format(text_file, iob_file)
    print('----')

    # 2. Convert iob clean data to bliou json format
    iob_file = os.path.join('data', iob_file)
    bliou_file = 'all_data_bliou_file.json'
    iob_to_bliou_format(iob_file, bliou_file)
    print('----')

    # ----- Preprocess main.jsonl data -----
    # 3. Clean jsonl raw data to and convert it to bliou format
    jsonl_file = 'data/main.jsonl'
    bliou_file = 'main_jsonl_to_bliou_file.bliou'
    jsonl_to_clean_bliou_format(jsonl_file, bliou_file)
    print('----')

    # 4. convert bliou to bliou json format
    bliou_file = os.path.join('data', bliou_file)
    bliou_json_file = 'main_jsonl_to_bliou_file.json'
    iob_to_bliou_format(bliou_file, bliou_json_file)
    print('----')

    # 5. Merge two data source
    bliou_json_files = [
        'data/all_data_bliou_file.json',
        'data/main_jsonl_to_bliou_file.json',
    ]
    merge_file = 'merge_all_data_and_main_jsonl.json'
    merge_bliou_json_files(bliou_json_files, merge_file)
    print('----')

    # 6. split data into train and validation
    file_name = 'data/merge_all_data_and_main_jsonl.json'
    split_data_to_train_val(file_name)
