from pydantic import BaseModel


class ShareExperienceData(BaseModel):
    vk_id: int
    experience: str
    experience_type: str = "text"
    publish: bool = True
    is_anonymous: bool = True
