from ....core.exceptions import InvalidDateFormat, InvalidEmail, InvalidPhoneFormat


def handle_input_error_and_repeat(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidDateFormat as e:
            print(e)
            return inner(*args, **kwargs)
        except InvalidEmail as e:
            print(e)
            return inner(*args, **kwargs)
        except InvalidPhoneFormat as e:
            print(e)
            return inner(*args, **kwargs)

    return inner
