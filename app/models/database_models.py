from app.database.database import Base
from sqlalchemy import Integer, Column , String, DATETIME , ForeignKey, Date, TIMESTAMP


class Employee(Base):
    __tablename__ = "employees"

    emp_id      = Column(Integer, primary_key=True) 
    emp_name    = Column(String)
    email       = Column(String)
    job_title   = Column(String)
    department  = Column(String)
    designation = Column(String)
    join_date   = Column(DATETIME)

    def __repr__(self):
        return (
            f"<Employee(id={self.emp_id}, name='{self.emp_name}', "
            f"email='{self.email}', job_title='{self.job_title}')>"
        )

class Leaves(Base):
    __tablename__ = "leaves"

    id          = Column(Integer, primary_key=True, index=True) 
    employee_id = Column(Integer, ForeignKey("employees.emp_id"))
    start_date  = Column(Date, nullable=False)
    end_date    = Column(Date, nullable=False)
    days        = Column(Integer)
    leave_type  = Column(String)
    status      = Column(String)
    applied_on  = Column(TIMESTAMP)
    approved_by = Column(String)
    remarks     = Column(String)

class Policies(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    policy_name = Column(String)
    description = Column(String)


class Salaries(Base):
    __tablename__ = "salaries"

    id = Column(Integer, primary_key=True, index=True)
    emp_id = Column(Integer, ForeignKey("employees.emp_id"))
    month = Column(Date, nullable=False)
    basic_salary = Column(Integer)
    bonus = Column(Integer)