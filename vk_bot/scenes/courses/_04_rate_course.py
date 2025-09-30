from vkbottle.bot import BotLabeler, MessageEvent

from customs.events import callback_handler


course_feedback_labeler = BotLabeler()


@callback_handler(course_feedback_labeler, cmd="rate_course")
async def rate_course(event: MessageEvent):
    # event.payload
    pass