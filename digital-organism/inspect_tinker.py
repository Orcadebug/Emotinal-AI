import tinker
import pydoc

try:
    print(tinker.types.SampleResponse.model_fields.keys())
except AttributeError:
    print("tinker.types.SampleResponse not found.")
