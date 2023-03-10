import logging

from opentelemetry import trace
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

logger = logging.getLogger(f"bentoml.{__name__}")
tracer = trace.get_tracer(__name__)


@tracer.start_as_current_span("count_vectorizer")
def cv_transformer(X, cv: CountVectorizer):
    logger.info("doing cv")
    X = cv.transform(X)
    return X


@tracer.start_as_current_span("tfidf_transformer")
def tfidf_transformer(X, tfidf: TfidfTransformer):
    logger.info("doing tfidf")
    X = tfidf.transform(X)
    return X
