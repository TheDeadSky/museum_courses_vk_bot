import json
import logging
import os
import random
import aiohttp

from models.base import BaseResponse
from models.experience import ShareExperienceData
from models.feedback import Feedback
from models.registration import RegistrationData, RegistrationResponse
from models.stories import HistoryResponse
from models.course import SelfSupportCourseResponse, CourseUserAnswer
from services.http import HttpService


class JsonApiService:
    base_url: str

    def __init__(self, base_url, **kwargs):
        self.base_url = base_url

    async def create(
        self,
        *,
        module: str,
        data: dict | None,
        as_json: bool = True,
    ) -> dict:
        response = await HttpService.post(
            url=f"{self.base_url}/{module}/",
            params=data if not as_json and data else None,
            json=data if as_json and data else None,
        )

        return await self._make_response(response)

    async def read(self, *, module: str, data: dict | None = None) -> dict:
        response = await HttpService.get(
            url=f"{self.base_url}/{module}/",
            params=data
        )

        return await self._make_response(response)

    async def update(self, *, module: str, data: dict) -> dict:
        """
        Not implemented yet.
        """
        raise NotImplementedError()

    async def delete(self, *, module: str, data: dict) -> dict:
        """
        Not implemented yet.
        """
        raise NotImplementedError()

    async def _make_response(self, response: aiohttp.ClientResponse) -> dict:
        if response.status in [200, 400]:
            return await response.json()

        raise Exception(f"ApiServiceError: {response.status} | {await response.text()}")


async def get_self_support_course_part(vk_id: str) -> SelfSupportCourseResponse:
    api_base_url = os.getenv("API_BASE_URL", "http://museum_api:8000")

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{api_base_url}/self-support-course/{vk_id}") as response:
            if response.status == 200:
                response_data = await response.json()
                return SelfSupportCourseResponse(**response_data)
            else:
                error_data = await response.json()
                raise Exception(f"API error: {error_data.get('detail', 'Unknown error')}")


async def self_support_course_answer(vk_id: str, part_id: int, answer: str):
    api_base_url = os.getenv("API_BASE_URL", "http://museum_api:8000")
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f"{api_base_url}/self-support-course/{vk_id}/answer",
            json=CourseUserAnswer(
                sm_id=vk_id,
                part_id=part_id,
                answer=answer
            ).model_dump()
        ) as response:
            if response.status == 200:
                response_data = await response.json()
                return BaseResponse(**response_data)
            else:
                error_data = await response.json()
                raise Exception(f"API error: {error_data.get('detail', 'Unknown error')}")


async def get_text_from_db(text_key: str):
    with open("src/texts_in_db.json", "r", encoding="utf-8") as file:
        return json.load(file)[text_key]


async def get_random_achievement_photo_url():
    achievement_photo_url = "https://ideasformuseums.com/botimages/ach-{}.png"
    return achievement_photo_url.format(random.randint(1, 6))


async def get_is_registered(sm_id: str):
    """Check if a user is registered by social media ID (telegram_id or vk_id)"""
    api_base_url = os.getenv("API_BASE_URL", "http://museum_api:8000")

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{api_base_url}/is-registered/{sm_id}") as response:
            if response.status == 200:
                return await response.json()
            else:
                error_data = await response.json()
                raise Exception(f"API error: {error_data.get('detail', 'Unknown error')}")


async def get_random_history(vk_id: str) -> HistoryResponse:
    """Get random history from the museum API."""
    api_base_url = os.getenv("API_BASE_URL", "http://museum_api:8000")

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{api_base_url}/random-history/{vk_id}") as response:
            if response.status == 200:
                response_data = await response.json()
                return HistoryResponse(**response_data)
            else:
                error_data = await response.json()
                raise Exception(f"API error: {error_data.get('detail', 'Unknown error')}")


async def send_experience(data: ShareExperienceData):
    api_base_url = os.getenv("API_BASE_URL", "http://museum_api:8000")

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{api_base_url}/share-experience", json=data.model_dump()) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_data = await response.json()
                raise Exception(f"API error: {error_data.get('detail', 'Unknown error')}")


async def send_feedback(data: Feedback):
    api_base_url = os.getenv("API_BASE_URL", "http://museum_api:8000")

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{api_base_url}/send-feedback", json=data.model_dump()) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_data = await response.json()
                raise Exception(f"API error: {error_data.get('detail', 'Unknown error')}")


async def send_feedback_response_to_user(user_id: str, response_text: str, feedback_id: str | None = None):
    """Send feedback response to user via bot's external API endpoint"""
    api_base_url = os.getenv("API_BASE_URL", "http://localhost:3000")

    payload = {
        "user_id": user_id,
        "response_text": response_text,
        "feedback_id": feedback_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{api_base_url}/api/send-feedback-response", json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_data = await response.json()
                raise Exception(f"API error: {error_data.get('error', 'Unknown error')}")


async def send_message_to_user(user_id: str, message: str):
    """Send any message to user via bot's external API endpoint"""
    api_base_url = os.getenv("API_BASE_URL", "http://localhost:3000")

    payload = {
        "user_id": user_id,
        "message": message
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{api_base_url}/api/send-message", json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_data = await response.json()
                raise Exception(f"API error: {error_data.get('error', 'Unknown error')}")
