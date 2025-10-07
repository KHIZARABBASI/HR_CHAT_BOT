from app.database.quries import Intents
from app.database.database import Sessionlocal

def query_connector(intent: str, employee_id: int = None, query: str= None):
    """this function will cheak the INTENT and the matching intent will seleced and perform action."""
    match intent:
        case "check remaining leaves":
            db = Sessionlocal()
            try:
                intent_service = Intents()
                user_leaves = intent_service.remaining_leaves(db=db, emp_id=employee_id)
            finally:
                db.close()
                return user_leaves
        
        case "employee joining information":
            db = Sessionlocal()
            try:
                intent_service = Intents()
                joing_date = intent_service.joining_info(emp_id=employee_id,db = db)
            finally:
                db.close()
                print(type(joing_date))
                return joing_date
            
        case "list all managers":
            db = Sessionlocal()
            try:
                intent_service = Intents()
                managers = intent_service.get_all_managers(db=db)
            finally:
                db.close()
                return managers

        case "apply for leave request":
            db = Sessionlocal()
            try:
                intent_service = Intents()
                apply_leave = intent_service.apply_for_leave(employee_id, db)
            finally:
                db.close()
                return apply_leave
            
        case "team members information":
            db = Sessionlocal()
            try:
                intent_service = Intents()
                apply_leave = intent_service.team_info(query, db)
            finally:
                db.close()
                return apply_leave
            

        case "company policies":
            db = Sessionlocal()
            try:
                intent_service = Intents()
                apply_leave = intent_service.company_policy(query, db)
            finally:
                db.close()
                return apply_leave
            
        case "profile information":
            db = Sessionlocal()
            try: 
                intent_service = Intents()
                my_info = intent_service.my_info(emp_id = employee_id, db = db)
            finally:
                db.close()
                return my_info
            
        case "monthly salary information":
            db = Sessionlocal()
            try: 
                intent_service = Intents()
                my_info = intent_service.monthly_salary_information(emp_id = employee_id, db = db)
            finally:
                db.close()
                return my_info

        case "greetings":
            greet = "greetings"
            return greet
        
        case "thanks":
            return "thanks"

        case "unknown":
            return "unknown"
    