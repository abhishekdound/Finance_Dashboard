from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from app.api import deps
from app.models.record import FinancialRecord
from app.schemas.record import Record, RecordCreate
from app.schemas.summary import DashboardSummary

router = APIRouter()


@router.post("/", response_model=Record)
def create_record(
        record_in: RecordCreate,
        db: Session = Depends(deps.get_db),
        current_user=Depends(deps.RoleChecker(["Admin"]))
):
    new_record = FinancialRecord(**record_in.model_dump(), owner_id=current_user.id)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


@router.get("/", response_model=List[Record])
def read_records(
        db: Session = Depends(deps.get_db),
        type: Optional[str] = None,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
        current_user=Depends(deps.get_current_user)
):
    query = db.query(FinancialRecord)

    if type:
        query = query.filter(FinancialRecord.type == type.lower())
    if category:
        query = query.filter(FinancialRecord.category == category)

    return query.order_by(FinancialRecord.date.desc()).offset(skip).limit(limit).all()


@router.get("/summary", response_model=DashboardSummary)
def get_summary(
        db: Session = Depends(deps.get_db),
        current_user=Depends(deps.get_current_user)
):
    income = db.query(func.sum(FinancialRecord.amount)).filter(FinancialRecord.type == "income").scalar() or 0
    expenses = db.query(func.sum(FinancialRecord.amount)).filter(FinancialRecord.type == "expense").scalar() or 0

    cat_data = db.query(FinancialRecord.category, func.sum(FinancialRecord.amount)).group_by(
        FinancialRecord.category).all()
    category_totals = {cat: amt for cat, amt in cat_data}

    recent = db.query(FinancialRecord).order_by(FinancialRecord.date.desc()).limit(5).all()

    return {
        "total_income": income,
        "total_expenses": expenses,
        "net_balance": income - expenses,
        "category_totals": category_totals,
        "recent_activity": recent
    }


@router.delete("/{record_id}", status_code=204)
def delete_record(
        record_id: int,
        db: Session = Depends(deps.get_db),
        current_user=Depends(deps.RoleChecker(["Admin"]))
):
    record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(record)
    db.commit()
    return None


import math


@router.get("/paginated", response_model=dict)
def read_records_paginated(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 10,
        current_user=Depends(deps.get_current_user)
):
    total_records = db.query(FinancialRecord).count()

    total_pages = math.ceil(total_records / limit) if limit > 0 else 0

    current_page = (skip // limit) + 1 if limit > 0 else 1

    data = db.query(FinancialRecord).order_by(FinancialRecord.date.desc()).offset(skip).limit(limit).all()

    return {
        "total_records": total_records,
        "total_pages": total_pages,
        "current_page": current_page,
        "limit": limit,
        "data": data
    }
