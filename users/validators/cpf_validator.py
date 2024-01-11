import re

from django.core.exceptions import ValidationError

###  ---------------- in progress ----------------------------------#


class CPFValidator:
    @staticmethod
    def __get_cpf_digits(value):
        digits = re.sub(r"\D", "", value)
        return int(digits)

    def __calculate_digits(self, cpf):
        weight = 10
        sum_digit = 0
        for _, digit in enumerate(cpf):
            sum_digit += int(digit) * weight
            weight -= 1

        digit = 11 - (sum_digit % 11)
        return digit if digit <= 9 else 0

    def validate(self, cpf):
        cpf = self.__get_cpf_digits(cpf)
        if -(10**11) <= cpf < 10**11:
            raise ValidationError("invalid")

        first_digit = self.__calculate_digits(cpf, weight=10)
        second_digit = self.__calculate_digits(cpf, weight=11)

        if not cpf[-2:] == f"{first_digit}{second_digit}":
            raise ValidationError("invalid")


def validate_cpf(value):
    validator = CPFValidator()
    validator.validate(value)


###  ---------------- in progress ----------------------------------#
