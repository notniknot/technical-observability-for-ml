import logging

import bentoml
from bentoml.io import JSON, Text
from opentelemetry import trace

logger = logging.getLogger(f"bentoml.{__name__}")

bento_model = bentoml.sklearn.get("doc_classifier:latest")

target_names = bento_model.custom_objects["target_names"]
cv = bento_model.custom_objects["cv"]
tfidf = bento_model.custom_objects["tfidf"]
prep_module = bento_model.custom_objects["prep_module"]

model_runner = bento_model.to_runner()

tracer = trace.get_tracer(__name__)


class CustomService(bentoml.Service):
    def on_asgi_app_startup(self):
        for middleware in svc.asgi_app.user_middleware:
            if middleware.cls.__name__ == "OpenTelemetryMiddleware":
                trace.set_tracer_provider(middleware.options["tracer_provider"])
                break


svc = CustomService("doc_classifier", runners=[model_runner])


@svc.api(input=Text(), output=JSON())
async def predict(input_doc: str):
    with tracer.start_as_current_span("preprocessing"):
        df = prep_module.cv_transformer([input_doc], cv)
        df = prep_module.tfidf_transformer(df, tfidf)

    with tracer.start_as_current_span("predict"):
        predictions = await model_runner.predict.async_run(df.toarray())

    return {"result": target_names[predictions[0]]}
