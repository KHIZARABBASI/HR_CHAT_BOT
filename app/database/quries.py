from sqlalchemy.orm import Session
from sqlalchemy import func, extract, desc

from app.database.database import Base, Sessionlocal
from app.models.database_models import Employee, Leaves, Policies, Salaries
from app.models.pydantic import ManagerSchema
from app.zero_shot.intent import  find_intent_policy, find_second_intent

class Intents:
    def get_all_managers(self, db: Session):
        """
        Retrieves all Project Managers (name + department).
        """
        managers = (
            db.query(Employee.emp_name.label("name"), Employee.department.label("department"),Employee.designation.label("designation"))
            .filter(Employee.designation.ilike("%manager%"))
            .all()
        )

        if not managers:
            return "No project managers found in the company."

        manager_descriptions = [f"{str(m.name)} -{str(m.designation)} from {str(m.department)} department" for m in managers]
        return ", ".join(manager_descriptions)

    

    def remaining_leaves(self, db: Session, emp_id: int):
        """
        Retrieves remaining leaves for an employee by name.
        Formula: 20 - sum(approved leave days in current year)
        """
        current_year = func.extract("year", func.current_date())

        remaining_leave = (
            db.query(
                (20 - func.coalesce(func.sum(Leaves.days), 0)).label("remaining_leaves")
            )
            .join(Employee, Employee.emp_id == Leaves.employee_id)
            .filter(Employee.emp_id == emp_id)
            .filter(Leaves.status == "Approved")
            .filter(extract("year", Leaves.start_date) == current_year)
            .scalar()   # return just the number
        )

        return remaining_leave
    
    def joining_info(self, emp_id: int, db: Session):
        """
        return the Joing date of the employee.
        """
        join_info = db.query(Employee.join_date).filter(Employee.emp_id == emp_id).scalar()
        return join_info
    
    def apply_for_leave(self, emp_id: int, db: Session):
        current_year = func.extract("year", func.current_date())

        remaining_leave = (
            db.query(
                (20 - func.coalesce(func.sum(Leaves.days), 0)).label("remaining_leaves")
            )
            .join(Employee, Employee.emp_id == Leaves.employee_id)
            .filter(Employee.emp_id == emp_id)
            .filter(Leaves.status == "Approved")
            .filter(extract("year", Leaves.start_date) == current_year)
            .scalar()   # return just the number
        )

        if remaining_leave < 20:
            print(f"applying for a leaves")
            return [{"status": "processing"}]

        return [{"status": "you already reached the limmit"}]
    
    def team_info(self, query: str, db: Session):
        intent = find_second_intent(query)
        print(intent)
        num_members = (
            db.query(Employee)
            .filter(Employee.department.ilike(f"%{intent}%"))
            .count()
        )
        return num_members
    
    def company_policy(self, query: str, db: Session):
        intent = find_intent_policy(query)
        print(f"second intent is {intent}")
        policy = (
            db.query(Policies.policy_name.label("policy_name"), Policies.description.label("description"))
            .filter(Policies.policy_name.ilike(f"%{intent}%"))
            .all()
        )
        print(intent)
        if not policy:
            return "No policy found in the company."

        descriptions = [f"{str(p.policy_name)} discription: {str(p.description)}" for p in policy]
        return ", ".join(descriptions)
    
    def my_info(self, emp_id : int, db : Session):
        my_info = (
            db.query(Employee)
            .filter(Employee.emp_id == emp_id)
            .first()
        )
        info_dict = {
            key: value for key, value in my_info.__dict__.items()
            if not key.startswith("_") 
        }
        info_list = [f"{key}: {value}" for key, value in info_dict.items()]
        return info_list
    
    def monthly_salary_information(self, emp_id : int, db : Session):
        salary = (
            db.query(Salaries.month, Salaries.basic_salary, Salaries.bonus)
            .join(Employee, Employee.emp_id == Salaries.emp_id)
            .filter(Salaries.emp_id == emp_id)
            .order_by(desc(Salaries.month))
            .all()
        )
        salary_info = [
            f"{row.month}: Basic Salary {row.basic_salary}, Bonus {row.bonus}"
            for row in salary
        ]
        return salary_info[0]



        



    

# db = Sessionlocal()

# try:
#     intent_service = Intents()
#     user_leaves = intent_service._remaining_leaves(db=db, emp_name="Keven")
#     print(f"Remaining Leaves for Keven: {user_leaves}")
# finally:
#     db.close()