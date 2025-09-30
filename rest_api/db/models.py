from sqlalchemy import (
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    JSON
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from typing import List, Optional
from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    vk_id: Mapped[int]
    firstname: Mapped[Optional[str]] = mapped_column(String(255))
    lastname: Mapped[Optional[str]] = mapped_column(String(255))
    is_museum_worker: Mapped[bool] = mapped_column(Boolean, default=False)
    how_long_museum_worker: Mapped[Optional[str]] = mapped_column(String(255))
    occupation: Mapped[Optional[str]] = mapped_column(String(255))
    registration_date: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.now()
    )
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    course_progress: Mapped[List["UserCourseProgress"]] = relationship(
        "UserCourseProgress", back_populates="user"
    )


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, default="")

    parts: Mapped[List["CoursePart"]] = relationship(
        "CoursePart", back_populates="course"
    )


class CoursePart(Base):
    __tablename__ = "course_part"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    order_number: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    video_url: Mapped[Optional[str]] = mapped_column(String(500))
    image_url: Mapped[Optional[str]] = mapped_column(String(500))
    last_part: Mapped[bool] = mapped_column(Boolean, default=False)

    course: Mapped["Course"] = relationship(
        "Course", back_populates="parts"
    )
    progress: Mapped[List["UserCourseProgress"]] = relationship(
        "UserCourseProgress", back_populates="part"
    )
    questions: Mapped[List["UserQuestion"]] = relationship(
        "PartQuestion", back_populates="part"
    )


class PartQuestion(Base):
    __tablename__ = "part_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    part_id: Mapped[int] = mapped_column(ForeignKey("course_part.id"))
    question: Mapped[str] = mapped_column(Text)
    answer_1: Mapped[Optional[str]] = mapped_column(Text)
    answer_2: Mapped[Optional[str]] = mapped_column(Text)
    answer_3: Mapped[Optional[str]] = mapped_column(Text)
    answer_4: Mapped[Optional[str]] = mapped_column(Text)
    correct_answer: Mapped[int] = mapped_column(Integer)
    correct_message: Mapped[str] = mapped_column(Text)
    incorrect_message: Mapped[str] = mapped_column(Text)

    part: Mapped["CoursePart"] = relationship(
        "CoursePart", back_populates="questions"
    )

class UserCourseProgress(Base):
    __tablename__ = "user_course_progress"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    part_id: Mapped[int] = mapped_column(ForeignKey("course_part.id"))
    part_question_id: Mapped[int] = mapped_column(ForeignKey("course_part_question.id"))
    date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())
    answer: Mapped[str] = mapped_column(Text)

    user: Mapped["User"] = relationship(
        "User", back_populates="course_progress"
    )
    part: Mapped["CoursePart"] = relationship(
        "CoursePart", back_populates="progress"
    )


# class Story(Base):
#     __tablename__ = "stories"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[Optional[int]] = mapped_column(
#         ForeignKey("user.id"),
#         nullable=True
#     )
#     user_name: Mapped[Optional[str]] = mapped_column(String(255))
#     status: Mapped[Optional[str]] = mapped_column(String(50))
#     content_type: Mapped[Optional[str]] = mapped_column(String(50))
#     title: Mapped[Optional[str]] = mapped_column(String(255))
#     text: Mapped[Optional[str]] = mapped_column(Text)
#     tag: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
#     media_url: Mapped[Optional[str]] = mapped_column(String(500))
#     link: Mapped[Optional[str]] = mapped_column(String(500))
#     is_anonymous: Mapped[bool] = mapped_column(Boolean, default=False)
#     is_agreed_to_publication: Mapped[bool] = mapped_column(Boolean, default=False)
#     updated: Mapped[Optional[DateTime]] = mapped_column(
#         DateTime,
#         default=datetime.now(),
#         onupdate=datetime.now()
#     )
#     created: Mapped[Optional[DateTime]] = mapped_column(
#         DateTime,
#         default=datetime.now(),
#         onupdate=datetime.now()
#     )
#
#     user: Mapped[Optional["User"]] = relationship(
#         "User", back_populates="stories"
#     )
#     questions: Mapped[List["UserQuestion"]] = relationship(
#         "UserQuestion", back_populates="story"
#     )
#     history: Mapped[List["StoryHistory"]] = relationship(
#         "StoryHistory", back_populates="story"
#     )
#
#
# class StoryHistory(Base):
#     __tablename__ = "story_history"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     story_id: Mapped[Optional[int]] = mapped_column(ForeignKey("stories.id"))
#     user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
#     date: Mapped[Optional[DateTime]] = mapped_column(DateTime, default=datetime.now())
#
#     user: Mapped[Optional["User"]] = relationship(
#         "User", back_populates="story_history"
#     )
#     story: Mapped[Optional["Story"]] = relationship(
#         "Story", back_populates="history"
#     )
#
#
# class UserQuestion(Base):
#     __tablename__ = "user_questions"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
#     story_id: Mapped[Optional[int]] = mapped_column(
#         ForeignKey("stories.id"), nullable=True)
#     question: Mapped[Optional[str]] = mapped_column(Text)
#     answer: Mapped[Optional[str]] = mapped_column(Text)
#     parent_id: Mapped[Optional[int]] = mapped_column(Integer)
#     question_date: Mapped[Optional[DateTime]] = mapped_column(
#         DateTime,
#         default=datetime.now()
#     )
#     answer_date: Mapped[Optional[DateTime]] = mapped_column(
#         DateTime
#     )
#     viewed: Mapped[Optional[DateTime]] = mapped_column(DateTime)
#
#     user: Mapped[Optional["User"]] = relationship(
#         "User", back_populates="questions"
#     )
#     story: Mapped[Optional["Story"]] = relationship(
#         "Story", back_populates="questions"
#     )
