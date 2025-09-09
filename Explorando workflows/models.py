import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

_PROVIDER_MAP = {
  "google" : ChatGoogleGenerativeAI
}

MODEL_CONFIGS = [
  {
    "key_name": "gemini_2.5_flash",
    "provider" : "google",
    "model_name" : "gemini-2.5-flash-previes-04-17",
    "temperature" : 1.0
  },
  {
    "key_name": "gemini_1.5_flash",
    "provider" : "google",
    "model_name" : "gemini-1.5-flash-previes-002",
    "temperature" : 1.0
  }
]


def _create_chat_model(model_name, provider, temperature: float | None = None):
  if provider not in _PROVIDER_MAP:
    raise ValueError(f"Provedor não suporado: {provider}. Provedores suportados são: {list(_PROVIDER_MAP.keys())}")
  
  model_class = _PROVIDER_MAP[provider]
  params = {"model": model_name}
  if temperature is not None:
    params["temperatues"] = temperature

  return model_class(**params)

models = {}

for config in MODEL_CONFIGS:
  models[config["key_name"]] = _create_chat_model(
    model_name = config["model_name"],
    provider=config["provider"],
    temperature=config.get("temperature")
  )
