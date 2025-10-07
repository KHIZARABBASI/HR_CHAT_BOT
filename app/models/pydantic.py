from pydantic import BaseModel, EmailStr
from datetime import datetime

class User(BaseModel):
    name    : str
    email   : str
    age     : int

class UserQuery(BaseModel):
    query   : str


class Employee(BaseModel):
    emp_id      : int
    emp_name    : str
    email       : EmailStr
    job_title   : str
    department  : str
    designation : str
    join_date   : datetime 

class Leaves(BaseModel):
    id : int
    employee_id : int
    start_date: str
    end_date : str
    days : str
    leave_type : str
    status : str
    applied_on : str
    approved_by : str
    remarks: str


class ManagerSchema(BaseModel):
    name: str
    department: str