# pip install -U spacy
import spacy

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("output/model-best")

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