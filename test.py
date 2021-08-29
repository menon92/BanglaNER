# pip install -U spacy
import spacy

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("output/model-best")

# Process whole documents
# text = ("অগ্রণী ব্যাংকের জ্যেষ্ঠ কর্মকর্তা পদে নিয়োগ পরীক্ষার প্রশ্নপত্র ফাঁসের অভিযোগ উঠেছে।")
text = (
    # "আব্দুর রহিম নামের কাস্টমারকে একশ টাকা বাকি দিলাম"
    # "সাত্তার সাহেব এর কাছে যে টাকা পাওয়া জেট সেই টাকা এখনও দেন নি"
    # "১০০ টাকা জমা দিয়েছেন কবির"
    "ডিপিডিসির স্পেশাল টাস্কফোর্সের প্রধান মুনীর চৌধুরী জানান"
)
doc = nlp(text)

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)
