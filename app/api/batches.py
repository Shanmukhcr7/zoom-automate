from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Batch, BatchDay
from app.schemas.batch import BatchResponse, BatchUpdateWeek, BatchDayBase

router = APIRouter(prefix="/api/batches", tags=["Batches"])

@router.get("", response_model=List[BatchResponse])
def get_batches(db: Session = Depends(get_db)):
    return db.query(Batch).all()

@router.get("/{batch_id}", response_model=BatchResponse)
def get_batch(batch_id: int, db: Session = Depends(get_db)):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch

@router.put("/{batch_id}/week", response_model=BatchResponse)
def update_batch_week(batch_id: int, week_update: BatchUpdateWeek, db: Session = Depends(get_db)):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    batch.current_week = week_update.current_week
    db.commit()
    db.refresh(batch)
    return batch

@router.post("/{batch_id}/days", response_model=BatchResponse)
def add_batch_day(batch_id: int, day: BatchDayBase, db: Session = Depends(get_db)):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
        
    day_str = day.day_of_week.upper()
    existing = db.query(BatchDay).filter(BatchDay.batch_id == batch_id, BatchDay.day_of_week == day_str).first()
    
    if not existing:
        db.add(BatchDay(batch_id=batch_id, day_of_week=day_str))
        db.commit()
        db.refresh(batch)
        
    return batch

@router.delete("/{batch_id}/days/{day_of_week}", response_model=BatchResponse)
def remove_batch_day(batch_id: int, day_of_week: str, db: Session = Depends(get_db)):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
        
    day_str = day_of_week.upper()
    existing = db.query(BatchDay).filter(BatchDay.batch_id == batch_id, BatchDay.day_of_week == day_str).first()
    
    if existing:
        db.delete(existing)
        db.commit()
        db.refresh(batch)
        
    return batch
