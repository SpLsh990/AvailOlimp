from email_validator import validate_email, EmailNotValidError

"""Проверка и нормализация email"""


def email_is_valid(email):
    try:
        email_info = validate_email(email, check_deliverability=True)
        normalized_email = email_info.normalized
        return True, normalized_email
    except EmailNotValidError as e:
        return False, str(e)


if __name__ == "__main__":
    email = "user@gmail.com"
    is_valid, result = email_is_valid(email)
    if is_valid:
        print(f"Все ок: {result}")
    else:
        print(f"Все не ок: {result}")
