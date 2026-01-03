from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.skill import Skill
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskOut

router = APIRouter(prefix="/skills/{skill_id}/tasks", tags=["tasks"])


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    skill_id: int,
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skill = db.execute(
        select(Skill).where(Skill.id == skill_id, Skill.user_id == current_user.id)
    ).scalar_one_or_none()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    task = Task(skill_id=skill_id, title=payload.title)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("", response_model=list[TaskOut])
def list_tasks(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skill = db.execute(
        select(Skill).where(Skill.id == skill_id, Skill.user_id == current_user.id)
    ).scalar_one_or_none()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    tasks = db.execute(select(Task).where(Task.skill_id == skill_id).order_by(Task.id)).scalars().all()
    return tasks

@router.patch("/{task_id}/done", response_model=TaskOut)
def mark_done(
    skill_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skill = db.execute(
        select(Skill).where(Skill.id == skill_id, Skill.user_id == current_user.id)
    ).scalar_one_or_none()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    task = db.execute(
        select(Task).where(Task.id == task_id, Task.skill_id == skill_id)
    ).scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.is_done = True
    db.commit()
    db.refresh(task)
    return task
