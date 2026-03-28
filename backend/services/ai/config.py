from api.core.config import get_settings

settings = get_settings()

provider = "groq"
model = settings.groq_model or settings.llm_model_primary
