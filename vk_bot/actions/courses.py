from vkbottle import Keyboard, Callback

from models.courses import CourseInfo


def make_courses_menu(courses: list[CourseInfo]):
    keyboard = Keyboard(inline=True)

    for course in courses:
        keyboard.add(Callback(course.title, payload={"cmd": "show_course_info", "course_id": course.id})).row()

    return keyboard