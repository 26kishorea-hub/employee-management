from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import engine, Base, get_db
from .schemas import EmployeeCreate, EmployeeResponse
from .crud import (
    create_employee,
    get_employees,
    get_employee,
    update_employee,
    delete_employee
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management API",
    description="Simple Employee Management System using FastAPI and MySQL",
    version="1.0.0"
)


@app.get("/")
def home():
    return {"message": "Employee Management API is running"}


@app.post("/employees", response_model=EmployeeResponse)
def add_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    return create_employee(db, employee)


@app.get("/employees", response_model=list[EmployeeResponse])
def list_employees(
    db: Session = Depends(get_db)
):
    return get_employees(db)


@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee_by_id(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = get_employee(db, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee_by_id(
    employee_id: int,
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    updated_employee = update_employee(
        db,
        employee_id,
        employee
    )

    if updated_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return updated_employee


@app.delete("/employees/{employee_id}")
def delete_employee_by_id(
    employee_id: int,
    db: Session = Depends(get_db)
):
    deleted_employee = delete_employee(
        db,
        employee_id
    )

    if deleted_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "message": "Employee deleted successfully"
    }