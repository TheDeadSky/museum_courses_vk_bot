from datetime import datetime

import aiohttp

from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.utils import get_user_by_vk_id
from db.models import User, UserQuestion
from schemas import BaseResponse
from .schemas import Feedback, FeedbackAnswerData, FeedbackListResponse, IncomingFeedback


async def save_user_feedback(feedback: IncomingFeedback, db: Session):
    user = get_user_by_vk_id(db, feedback.vk_id)

    user_question = UserQuestion(
        user_id=user.id,
        question=feedback.feedback
    )

    db.add(user_question)
    db.commit()
    db.refresh(user_question)

    return BaseResponse(
        success=True,
        message="Спасибо за ваш отзыв!"
    )


async def get_feedbacks(
    db: Session,
    page: int = 1,
    per_page: int = 10,
    search: str = "",
    status: str = ""
):
    filters = []

    if status:
        if status == "answered":
            filters.append(UserQuestion.answer.isnot(None))
        elif status == "pending":
            filters.append(UserQuestion.answer.is_(None))

    if search:
        filters.append(UserQuestion.question.like(f"%{search}%"))

    feedbacks = db.query(UserQuestion).filter(
        and_(*filters)
    ).offset((page - 1) * per_page).limit(per_page).all()

    response = FeedbackListResponse(
        success=True,
        message="Отзывы получены",
        feedbacks=[Feedback(
            id=fb.id,
            user_id=fb.user_id,
            user_name=fb.user.firstname,
            question=fb.question,
            question_date=fb.question_date,
            answer=fb.answer,
            answer_date=fb.answer_date,
            viewed=fb.viewed
        ) for fb in feedbacks]
    )

    return response


async def render_feedbacks_page():
    with open("services/feedback/templates/feedbacks.html", "r") as file:
        html_content = file.read()

    return html_content


async def answer_feedback(answer_data: FeedbackAnswerData, db: Session):
    feedback = db.query(UserQuestion).filter(UserQuestion.id == answer_data.feedback_id).first()

    feedback.answer = answer_data.answer
    feedback.answer_date = datetime.now()

    db.commit()
    db.refresh(feedback)

    response = await send_answer_to_user(answer_data, db)
    print(response)

    return BaseResponse(
        success=True,
        message="Ответ записан"
    )


async def send_answer_to_user(feedback_answer: FeedbackAnswerData, db: Session):
    print("feedback_answer", feedback_answer)

    user: None | User = db.query(User).filter(User.id == feedback_answer.user_id).first()

    if not user:
        return BaseResponse(
            success=False,
            message="Пользователь не найден"
        )

    feedback = db.query(UserQuestion).filter(UserQuestion.id == feedback_answer.feedback_id).first()

    if not feedback:
        return BaseResponse(
            success=False,
            message="Обратная связь не найдена"
        )

    print(
        "send_answer_to_user",
        {
            "vk_id": user.vk_id,
            "answer_text": feedback_answer.answer,
            "feedback_text": feedback.question
        }
    )

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://museum_bot:9000/api/send-feedback-answer",
            json={
                "vk_id": user.vk_id,
                "answer_text": feedback_answer.answer,
                "feedback_text": feedback.question
            }
        ) as response:
            return await response.json()
