from support_check_class import CheckAnything
from custom_exception import WrongInputData, DontMatchTemplate
from support_slice_class import Slicer


test_string = 'amount: 50000\ninterest: 20%\ndownpayment: 20000\nnterm: 3\n'


class CreditCalculator:
    checker = CheckAnything()

    def __init__(self, credit_application: str) -> None:
        self.composition_of_the_credit = {
            'amount': None,
            'interest': None,
            'downpayment': None,
            'nterm': None,
        }
        try:
            self.credit_application = type(self).checker.check_is_string(credit_application)
            self.slicer = Slicer(self.credit_application)
        except WrongInputData:
            pass
        self.get_composition_credit()

    def get_composition_credit(self) -> None:
        self.slicer.slice_text('\n')
        templates = list(self.composition_of_the_credit)
        for param in self.slicer.slice_list(': '):
            try:
                template = self.fill_composition_credit(param, templates)
                templates.remove(template)
            except DontMatchTemplate:
                continue

    def fill_composition_credit(self, param: list, templates: list) -> str:
        for template in templates:
            word_for_analyze = param[0]
            min_border_algorithm_pass = int(3 * len(template) / 4)
            checksum = self.compare_word_with_template(word_for_analyze, template)
            if checksum >= min_border_algorithm_pass:
                try:
                    self.composition_of_the_credit[template] = float(param[1])
                except (ValueError, TypeError):
                    self.composition_of_the_credit[template] = self.conver_to_float(param[1])
                return template
        raise DontMatchTemplate

    def compare_word_with_template(self, word_for_analyze: str, template: str) -> int:
        template = list(template)
        result = 0
        for char in word_for_analyze:
            if char in template:
                result += 1
                template.remove(char)
        return result

    def conver_to_float(self, number: str) -> float:
        result = [char for char in number if char.isdigit() or char == '.' or char == ',']
        if ',' not in result:
            return float(''.join(result))
        result.replace(',', '.')
        return float(''.join(result))
    
    def get_annuity_month_pay(self) -> str:
        month_pay = self.calculate_annuity_pay()
        return f'Ежемесячный платёж: {month_pay:.2f} рублей.'

    def calculate_annuity_pay(self) -> float:
        try:
            amount = self.composition_of_the_credit['amount']
            monthly_interest_rate = self.composition_of_the_credit['interest'] / 1200
            number_of_payments = self.composition_of_the_credit['nterm'] * 12
        except TypeError:
            return f'Cannot calculate. Miss element in {self.composition_of_the_credit["amount"]} or {self.composition_of_the_credit["interest"]} or {self.composition_of_the_credit["nterm"]}'
        annuity_ratio = (monthly_interest_rate * ((1 + monthly_interest_rate) ** number_of_payments)) / (((1 + monthly_interest_rate) ** number_of_payments) - 1)
        return amount * annuity_ratio

    def get_total_amount_of_payment(self) -> str:
        month_pay = self.calculate_annuity_pay()
        number_of_payments = self.composition_of_the_credit['nterm'] * 12
        total_sum = month_pay * number_of_payments
        return f'Общая сумма выплаты: {total_sum:.2f} рублей'

    def get_total_amount_of_interest(self) -> str:
        month_pay = self.calculate_annuity_pay()
        number_of_payments = self.composition_of_the_credit['nterm'] * 12
        total_sum = month_pay * number_of_payments
        total_interest = total_sum - self.composition_of_the_credit['amount']
        return f'Общий объём начисленых процентов: {total_interest:.2f} рублей'

a = CreditCalculator(test_string)
print(a.composition_of_the_credit)
print(a.get_annuity_month_pay())
print(a.get_total_amount_of_payment())
print(a.get_total_amount_of_interest())