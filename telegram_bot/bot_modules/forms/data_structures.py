from typing import List
from pydantic import BaseModel
from bot_modules.register.data_structures import Prepod, User


class Question(BaseModel):
    question_text: str
    question_type: str
    question_message_id: str
    user_answered: str


class TextQuestion(Question):
    question_type = "msg"


class PollQuestion(Question):
    question_type = "poll"
    options: List[str]


#############################


class Form(BaseModel):
    form_id: int
    form_name: str
    creator: Prepod
    questions: List[Question]


class SentForm(Form):
    sent_form_id: str
    sent_to_groups: List[str]
    sent_to_users_ids: List[str]
    completed_users_ids: List[str]


class CompletableForm(Form):
    sent_form_id: str
    current_question_num: int


#############################


class ChoosingGroupsPoll(BaseModel):
    poll_id: str
    poll_num: int
    poll_options: List[str]
    created_by: User


class ChoosingGroupsDispatcher(BaseModel):
    user_id: int
    polls: List[ChoosingGroupsPoll]
    selected_form: Form
    selected_groups: List[str]


##############################


class CompletingFormsDisatcherSessionData(BaseModel):
    sent_form: SentForm
    current_question_num: int
    current_question: Question
    answers: list
