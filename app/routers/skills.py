from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.skill import Skill
from app.schemas.skill import SkillCreate, SkillOut, SkillUpdate
from sqlalchemy import func
from app.models.task import Task
from app.schemas.progress import SkillProgressOut

router = APIRouter(prefix="/skills", tags=["skills"])


@router.post("", response_model=SkillOut, status_code=status.HTTP_201_CREATED)
def create_skill(
    payload: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skill = Skill(user_id=current_user.id, name=payload.name, description=payload.description)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


@router.get("", response_model=list[SkillOut])
def list_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skills = db.execute(
        select(Skill).where(Skill.user_id == current_user.id).order_by(Skill.id.desc())
    ).scalars().all()
    return skills


@router.get("/{skill_id}", response_model=SkillOut)
def get_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skill = db.execute(
        select(Skill).where(Skill.id == skill_id, Skill.user_id == current_user.id)
    ).scalar_one_or_none()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@router.patch("/{skill_id}", response_model=SkillOut)
def update_skill(
    skill_id: int,
    payload: SkillUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skill = db.execute(
        select(Skill).where(Skill.id == skill_id, Skill.user_id == current_user.id)
    ).scalar_one_or_none()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    if payload.name is not None:
        skill.name = payload.name
    if payload.description is not None:
        skill.description = payload.description

    db.commit()
    db.refresh(skill)
    return skill


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skill = db.execute(
        select(Skill).where(Skill.id == skill_id, Skill.user_id == current_user.id)
    ).scalar_one_or_none()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    db.delete(skill)
    db.commit()
    return None
@router.get("/{skill_id}/progress", response_model=SkillProgressOut)
def skill_progress(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skill = db.execute(
        select(Skill).where(Skill.id == skill_id, Skill.user_id == current_user.id)
    ).scalar_one_or_none()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    total_tasks = db.execute(
        select(func.count(Task.id)).where(Task.skill_id == skill_id)
    ).scalar_one()

    done_tasks = db.execute(
        select(func.count(Task.id)).where(Task.skill_id == skill_id, Task.status == "done")
    ).scalar_one()

    percent = 0
    if total_tasks > 0:
        percent = int((done_tasks / total_tasks) * 100)

    return SkillProgressOut(
        skill_id=skill_id,
        total_tasks=total_tasks,
        done_tasks=done_tasks,
        percent=percent,
    )

