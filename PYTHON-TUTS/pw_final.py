import re

# Function to check password length
def check_length(password):
    """Checks if the password is at least 12 characters long."""
    if len(password) >= 12:
        return True, "Good length"
    else:
        return False, "Password should be at least 12 characters long"


# Function to check for uppercase and lowercase letters
def check_case(password):
    """Checks if the password has both uppercase and lowercase letters."""
    if any(char.islower() for char in password) and any(char.isupper() for char in password):
        return True, "Contains both uppercase and lowercase letters"
    else:
        return False, "Password should have both uppercase and lowercase letters"


# Function to check for numbers and special characters
def check_numbers_special(password):
    """Checks if the password contains at least one number and one special character."""
    if re.search(r"\d", password) and re.search(r"\W", password):
        return True, "Contains numbers and special characters"
    else:
        return False, "Password should include at least one number and one special character"


# Function to check if the password is a common weak password
def check_common_passwords(password):
    """Checks if the password is too common."""
    common_passwords = ["password", "123456", "qwerty", "letmein", "welcome", "password123"]
    if password.lower() in common_passwords:
        return False, "Password is too common and easy to guess"
    return True, "Not a commonly used password"


# REQUIRED FUNCTION (must match assignment exactly)
def check_password_strength(password):
    """Evaluates the password using all checks and returns feedback."""
    results = []
    
    # Call each function and collect feedback
    length_ok, length_msg = check_length(password)
    case_ok, case_msg = check_case(password)
    num_spec_ok, num_spec_msg = check_numbers_special(password)
    common_ok, common_msg = check_common_passwords(password)

    results.append(length_msg)
    results.append(case_msg)
    results.append(num_spec_msg)
    results.append(common_msg)

    # Determine overall strength
    if all([length_ok, case_ok, num_spec_ok, common_ok]):
        return "Strong password! Good job."
    else:
        return "Weak password. Recommendations:\n" + "\n".join(results)


# Task 3: User input validation
while True:
    user_password = input("Enter a password to validate for your account: ").strip()
    if user_password:
        break
    else:
        print("Password cannot be empty. Please enter a valid password.")


# Task 6: Call function and display results
password_feedback = check_password_strength(user_password)
print(password_feedback)