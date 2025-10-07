import os 
os.environ["HF_HOME"] = "D:/models"
from transformers import pipeline

from app.models import pydantic
from app.config.config import CHOISES, TEAMS_CHOISES, COMPANY_POLICIES


pipeline = pipeline(task = "zero-shot-classification",
                    model="facebook/bart-large-mnli")



def find_intent(message: str, verables = CHOISES):
    result = pipeline(message, verables)
    result = result["labels"][0]
    return result


def find_second_intent(message: str, verables = TEAMS_CHOISES):
    result = pipeline(message, verables)
    result = result["labels"][0]
    return result

def find_intent_policy(message: str, verables = COMPANY_POLICIES):
    result = pipeline(message, verables)
    result = result["labels"][0]
    return result



