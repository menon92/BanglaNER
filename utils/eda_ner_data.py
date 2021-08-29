
import json


data_file = 'data/merge_all_data_and_main_jsonl.json'


with open(data_file, 'r') as fp:
    data = json.load(fp)

token_o = 0
token_per = 0
data_contain_at_list_one_name_tag = []
id_cnt = 0
for d in data:
    sentence_tokens = d["paragraphs"][0]["sentences"][0]["tokens"]
    tags = set()
    for token in sentence_tokens:
        tags.add(token["ner"])
    
    if tags == set('O'):
        token_o += 1
    else:
        token_per += 1
        d['id'] = id_cnt
        data_contain_at_list_one_name_tag.append(d)
        id_cnt += 1

print(f"Total sentences that only contain 'O' tags {token_o}")
print(f"Total sentence that only contain `PER` tags {token_per}")


with open("data/data_contain_at_list_one_name_tag.json", 'w') as fp:
    json.dump(data_contain_at_list_one_name_tag, fp, indent=2, ensure_ascii=False)