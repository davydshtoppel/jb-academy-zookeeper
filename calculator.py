from collections import deque
import string
import re


class Operation:
    def __init__(self, weight):
        self.weight = weight

    def execute(self, operand1, operand2):
        pass


class Subtraction(Operation):
    def __init__(self):
        super().__init__(1)

    def execute(self, operand1, operand2):
        return operand1 - operand2


class Addition(Operation):
    def __init__(self):
        super().__init__(1)

    def execute(self, operand1, operand2):
        return operand1 + operand2


class Multiplying(Operation):
    def __init__(self):
        super().__init__(2)

    def execute(self, operand1, operand2):
        return operand1 * operand2


class Division(Operation):
    def __init__(self):
        super().__init__(2)

    def execute(self, operand1, operand2):
        return operand1 // operand2


class Power(Operation):
    def __init__(self):
        super().__init__(3)

    def execute(self, operand1, operand2):
        return operand1 ** operand2


class CalculationException(Exception):
    def __init__(self, message):
        self.message = message


def parse_operation(operation_str: str):
    if operation_str == '*':
        return Multiplying()
    elif operation_str == '/':
        return Division()
    elif operation_str == '^':
        return Power()
    elif re.match('^-+$', operation_str) is not None:
        return Addition() if len(operation_str) % 2 == 0 else Subtraction()
    elif re.match('^\++$', operation_str) is not None:
        return Addition()
    else:
        raise CalculationException('Invalid expression')


class Calculator:
    def __init__(self):
        self.variables = {}

    @staticmethod
    def check_variable_name(name: str):
        name = name.replace(' ', '')
        if not name.isalpha():
            raise CalculationException('Invalid identifier')
        return name

    def parse_infix(self, expression: str):
        expression = expression.replace(' ', '')
        result = []
        operation_turn = False
        buffer = ''
        idx = 0
        quotes = 0
        while True:
            if len(expression) <= idx:
                if len(buffer) > 0:
                    result.append(self.parse_operand(buffer))
                break
            it = expression[idx]
            if operation_turn:
                if it.isalnum() or it == '(':
                    result.append(parse_operation(buffer))
                    buffer = ''
                    operation_turn = False
                elif it in '-+*/^':
                    buffer += it
                    idx += 1
            else:
                if it.isalnum():
                    buffer += it
                    idx += 1
                elif len(buffer) == 0 and it == '-':
                    buffer = it
                    idx += 1
                elif it == '(':
                    result.append(it)
                    idx += 1
                    quotes += 1
                elif it == ')':
                    result.append(self.parse_operand(buffer))
                    result.append(it)
                    idx += 1
                    quotes -= 1
                    buffer = ''
                    operation_turn = True
                else:
                    result.append(self.parse_operand(buffer))
                    buffer = ''
                    operation_turn = True
        if quotes != 0:
            raise CalculationException('Invalid expression')
        return result

    def convert_to_postfix(self, expression: str):
        infix_exp = self.parse_infix(expression)
        result = []
        stack = deque()
        for it in infix_exp:
            if isinstance(it, int):
                result.append(it)
            elif isinstance(it, Operation) and (len(stack) == 0 or stack[-1] == '('):
                stack.append(it)
            elif isinstance(it, Operation) and isinstance(stack[-1], Operation) and it.weight > stack[-1].weight:
                stack.append(it)
            elif isinstance(it, Operation) and isinstance(stack[-1], Operation) and it.weight <= stack[-1].weight:
                while len(stack) > 0 and isinstance(stack[-1], Operation) and stack[-1].weight >= it.weight:
                    result.append(stack.pop())
                stack.append(it)
            elif isinstance(it, str) and it == '(':
                stack.append(it)
            elif isinstance(it, str) and it == ')':
                el = stack.pop()
                while el != '(':
                    result.append(el)
                    el = stack.pop()
        while len(stack) > 0:
            result.append(stack.pop())
        return result

    def add_variable(self, name: str, expression: str):
        name = self.check_variable_name(name)
        try:
            self.variables[name] = self.execute_expression(expression)
        except Exception:
            raise CalculationException('Invalid assignment')

    def get_variable(self, name: str):
        name = self.check_variable_name(name)
        if name not in self.variables:
            raise CalculationException('Unknown variable')
        return self.variables[name]

    def parse_operand(self, value: str):
        if re.search('[a-zA-Z]', value) is not None:
            return self.get_variable(value)
        else:
            return int(value)

    def execute_expression(self, expression):
        postfix = self.convert_to_postfix(expression)
        stack = deque()
        for it in postfix:
            if isinstance(it, int):
                stack.append(it)
            elif isinstance(it, Operation):
                first = stack.pop()
                second = stack.pop()
                stack.append(it.execute(second, first))
        return stack.pop()


def execute_command(command):
    if command == '/exit':
        print('Bye!')
        return True
    if command == '/help':
        print('The program calculates the sum of numbers')
    else:
        print('Unknown command')
    return False


calculator = Calculator()
# print(calculator.parse_infix('8 * (2 + 3'))
# print(calculator.convert_to_postfix('3 + 2 * 4'))
# print(calculator.parse_infix('2 * (3 + 4) + 1'))
# print(calculator.convert_to_postfix('2 * (3 + 4) + 1'))
# print(calculator.parse_infix('2^2'))
# print(calculator.convert_to_postfix('2^2'))
# print(calculator.parse_infix('2*2^3'))
# print(calculator.convert_to_postfix('2*2^3'))
# print(calculator.parse_infix('8 * 3 + 12 * (4 - 2)'))
# print(calculator.convert_to_postfix('8 * 3 + 12 * (4 - 2)'))

while True:
    user_input = input()
    if user_input.startswith('/'):
        if execute_command(user_input):
            break
    elif user_input == '':
        continue

    try:
        if user_input.find('=') >= 0:
            calculator.add_variable(*user_input.split('=', maxsplit=2))
        else:
            result = calculator.execute_expression(user_input)
            print(result)
    except CalculationException as ex:
        print(ex.message)
    except:
        print('Invalid expression')
