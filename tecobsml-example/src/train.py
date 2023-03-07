import bentoml
import preprocessing as prep
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier

categories = [
    "rec.autos",
    "rec.motorcycles",
    "rec.sport.baseball",
    "rec.sport.hockey",
]

print("Loading 20 newsgroups dataset for categories:")
print(categories)

data = fetch_20newsgroups(subset="train", categories=categories)
print("%d documents" % len(data.filenames))
print("%d categories" % len(data.target_names))
print()

cv = CountVectorizer()
tfidf = TfidfTransformer()
clf = SGDClassifier(loss="log_loss")

X_transformed = cv.fit_transform(data.data, data.target)
X_transformed = tfidf.fit_transform(X_transformed, data.target)
clf.fit(X_transformed, data.target)

bento_model = bentoml.sklearn.save_model(
    "doc_classifier",
    clf,
    signatures={"predict": {"batchable": True}},
    custom_objects={
        "target_names": data.target_names,
        "cv": cv,
        "tfidf": tfidf,
        "prep_module": prep,
    },
)
print("Model saved", bento_model)
