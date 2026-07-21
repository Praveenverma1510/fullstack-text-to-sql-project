from functools import lru_cache
from transformers import pipeline
import time

from app.core.config import settings

PROMPT_TEMPLATE = """You are a PostgreSQL text-to-SQL assistant.
Return only one read-only SQL query.
Use only the provided schema.
Never generate DELETE, UPDATE, INSERT, DROP, ALTER, TRUNCATE, CREATE, or multiple statements.

Question:
{question}

Schema:
{schema}

SQL:
"""


@lru_cache(maxsize=1)
def get_generator():
    try:
        return pipeline(
            task=settings.hf_task,
            model=settings.hf_model_id,
        )
    except Exception as e:
        print("MODEL LOAD ERROR:")
        print(e)
        raise


class TextToSQLService:
    def generate(self, question: str, schema_context: str) -> dict:
        prompt = PROMPT_TEMPLATE.format(question=question, schema=schema_context)
        generator = get_generator()
        print("Generator:", generator)
        if generator:
            print("=" * 80)
            print("PROMPT")
            print(prompt)
            print("=" * 80)

            # result = generator(
            start = time.time()

            result = generator(
                prompt,
                max_new_tokens=32,
                do_sample=False,
                return_full_text=False,
            )

            print("Generation took", time.time() - start, "seconds")
            print(result)

            print("=" * 80)
            print("RAW RESULT")
            print(result)
            print("=" * 80)

            text = result[0]["generated_text"].strip()

            print("GENERATED TEXT")
            print(text)
            print("=" * 80)
        else:
            text = "SELECT 1;"
        sql = text.split(";")[0].strip() + ";"
        return {
            "sql": sql,
            "explanation": "Generated from schema-aware prompting with a Hugging Face model.",
        }
