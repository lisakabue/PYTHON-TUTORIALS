from datetime import datetime, timedelta


savings_goals = {}


def create_savings_goal():
    user_id = input("Enter User ID: ")
    target_amount = float(input("Enter Traget Amount: "))
    taregt_date_str = input("Enter Target Date (YYYY-MM-DD): ")
    target_date = datetime.strptime(taregt_date_str, "%Y-%m-%d")

    savings_goals[user_id] = {
        "target_amount": target_amount,
        "target_date": target_date,
        "amount_saved": 0.0,
        "status": "Active"
    }
    print("\nSavings goal successfully created!")
    
    
def update_savings_progress():
    user_id = input("Enter User ID: ")
    
    if user_id not in savings_goals:
        print("No savings goal found for this user ", user_id)
        return
    additional_amount = float(input("Enter amount to save: "))
    goal = savings_goals[user_id]
    
    goal['amount_saved'] += additional_amount
    
    if goal['amount_saved'] >= goal['target_amount']:
        goal['status'] = "Completed"
        print("🎉 Congrats! You have achieved your savings goal!")
    else:
        print(f"Progress updated: Current Savings: {goal['amount_saved']}")
        
def check_goal_status():
    user_id = input("Enter User ID: ")
    
    if user_id not in savings_goals:
        print("No savings goal found for this user ", user_id)
        return
    goal = savings_goals[user_id]
    
    if goal['status'] == 'Completed':
        print("🎉 Goal Status: COMPLETED, Congrats! You have achieved your savings goal!")
    else:
        remaining = goal['target_amount'] - goal['amount_saved']
        print(f"Goal Status: ACTIVE - Remaining amount: {remaining}")

def send_deadline_notification():
    user_id = input("Enter User ID: ")
    
    if user_id not in savings_goals:
        print("No savings goal found for this user ", user_id)
        return
    
    goal = savings_goals[user_id]
    today = datetime.today()
    days_remaining = (goal['target_date'] - today).days
    remaining_amount = goal['target_amount'] - goal['amount_saved']
    
    if days_remaining <= 5 and remaining_amount > 0:
        print("\n⚠️ NOTIFICATION")
        print(f"Your savings goal deadline is near!")
        print(f"Days left: {days_remaining}")
        print(f"Amount remaining:{remaining_amount}")
        print("Please try to save more before the deadline. \n")
    else:
        print("No notification needed at this time.")



def main():
    print("=== Savings Goal Tracking System ===")
    
    while True:
        print("\n Select and option")
        print("1. Create Savings Goal")
        print("2. Update Savings Progress")
        print("3. Check Goal Status")
        print("4. Check for Deadline Notification")
        print("5. Exit")

        choice = input("Enter your choice: ")
        
        if choice == "1":
            create_savings_goal()
        elif choice == "2":
            update_savings_progress()
        elif choice == "3":
            check_goal_status()
        elif choice == "4":
            send_deadline_notification()
        elif choice == "5":
            print("Exiting System. Goodbye")
            break
        else:
            print("Invalid selection. Try again")


main()
        
