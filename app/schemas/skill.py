from pydantic import BaseModel, Field


class SkillBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)


class SkillOut(SkillBase):
    id: int

    class Config:
        from_attributes = True
