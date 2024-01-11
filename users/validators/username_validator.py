from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator


class CustomUserValidationError(ValidationError):
    def __init__(self, error_list, code=None, message=None):
        super().__init__(error_list, code=code)
        self.message = message


class CustomUsernameValidator:
    MIN_LENGTH = 5
    START_LETTER_REGEX = "^[a-zA-Z]"
    SPECIAL_CHARS_REGEX = "^[a-zA-Z0-9._-]*$"

    def __default_validator(self):
        return [
            MinLengthValidator(
                CustomUsernameValidator.MIN_LENGTH,
                message=self.get_help_text_min_length(),
            ),
            RegexValidator(
                CustomUsernameValidator.START_LETTER_REGEX,
                message=self.get_help_text_starts_with_letter(),
                code="starts_with_letter",
            ),
            RegexValidator(
                CustomUsernameValidator.SPECIAL_CHARS_REGEX,
                message=self.get_help_text_starts_with_letter(),
                code="invalid_characters",
            ),
        ]

    @staticmethod
    def get_help_text_min_length():
        return "Username must be at least 5 characters long."

    @staticmethod
    def get_help_text_starts_with_letter():
        return "Username must be start with a letter."

    @staticmethod
    def get_help_text_specials_chars():
        return "Username must contain only letters, numbers, dots, underscores, and hyphens."

    def validate(self, username_field):
        errors = []
        for validator in self.__default_validator():
            try:
                validator(username_field)
            except ValidationError as error:
                errors.extend(error.error_list)
        if errors:
            raise CustomUserValidationError(
                error_list=errors,
                code="username_validation_error",
            )


def validate_username(value):
    validator = CustomUsernameValidator()
    validator.validate(value)
    return value


if __name__ == "__main__":
    ...
