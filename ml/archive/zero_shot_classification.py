from transformers import pipeline

classifier = pipeline('zero-shot-classification', model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli")
candidate_labels = ['happy', 'sad', 'angry', 'fear', 'neutral']

text='My mother passed away'

output = classifier(text, candidate_labels, multi_label=False)

dom_emotion = output['labels'][0]
print(dom_emotion)