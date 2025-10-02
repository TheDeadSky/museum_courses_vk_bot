from pydantic import BaseModel, Field, ConfigDict


class CourseInfo(BaseModel):
    id: int
    title: str
    description: str
    is_started: bool = False

    model_config = ConfigDict(from_attributes=True)


class CoursePart(BaseModel):
    id: int
    title: str
    description: str = Field(description="Description of the current part", max_length=4096)
    video_url: str | None = None
    image_url: str | None = None
    last_part: bool = False
    question_id: int | None = None
    question: str | None = None
    answer_1: str | None = None
    answer_2: str | None = None
    answer_3: str | None = None
    answer_4: str | None = None
    correct_answer: int | None = None
    correct_message: str | None = None
    incorrect_message: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CoursePartQuestionAnswer(BaseModel):
    vk_id: int
    course_id: int
    part_id: int
    part_question_id: int
    answer: str


class CourseFeedback(BaseModel):
    course_id: int
    vk_id: int
    rate: int
    rate_description: str
    public_feedback: str
