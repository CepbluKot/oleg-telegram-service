from typing import List
from pydantic import BaseModel
from bot_modules.forms.data_structures import Question, SentForm


class CompletingFormDispatcher(BaseModel):
    current_question: Question
    current_question_num: int
    current_sent_form: SentForm
    completed_by_user_id: int


class UserInterface(BaseModel):
    user_id: str
    GUI: bool
