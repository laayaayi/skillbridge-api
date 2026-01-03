from pydantic import BaseModel


class SkillProgressOut(BaseModel):
    skill_id: int
    total_tasks: int
    done_tasks: int
    percent: int
