from vkbottle.bot import rules, MessageEvent
from vkbottle_types.events import GroupEventType
from vkbottle.framework.labeler.abc import ABCLabeler


def callback_handler(labeler: ABCLabeler, **rules_args):
    return labeler.raw_event(
        GroupEventType.MESSAGE_EVENT,
        MessageEvent,
        rules.PayloadContainsRule(rules_args)
    )
