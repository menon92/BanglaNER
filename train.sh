# python -m spacy train configs/config.cfg \
#     --output ./models_from_pretrain_model \
#     --paths.train ./data/train.spacy \
#     --paths.dev ./data/val.spacy


python -m spacy train configs/config.cfg \
    --output ./bangla_data_models \
    --paths.train ./data/bangla-ner-data/train.spacy \
    --paths.dev ./data/bangla-ner-data/train.spacy
