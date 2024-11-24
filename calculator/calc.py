import flet as ft
import math


class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text


class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE


class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK


class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=30)
        self.width = 350
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 10
        self.content = ft.Column(
            spacing=5,
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    spacing=5,
                    controls=[
                        ExtraActionButton("AC", self.button_clicked),
                        ExtraActionButton("+/-", self.button_clicked),
                        ExtraActionButton("%", self.button_clicked),
                        ActionButton("/", self.button_clicked),
                    ],
                ),
                ft.Row(
                    spacing=5,
                    controls=[
                        DigitButton("7", self.button_clicked),
                        DigitButton("8", self.button_clicked),
                        DigitButton("9", self.button_clicked),
                        ActionButton("*", self.button_clicked),
                    ],
                ),
                ft.Row(
                    spacing=5,
                    controls=[
                        DigitButton("4", self.button_clicked),
                        DigitButton("5", self.button_clicked),
                        DigitButton("6", self.button_clicked),
                        ActionButton("-", self.button_clicked),
                    ],
                ),
                ft.Row(
                    spacing=5,
                    controls=[
                        DigitButton("1", self.button_clicked),
                        DigitButton("2", self.button_clicked),
                        DigitButton("3", self.button_clicked),
                        ActionButton("+", self.button_clicked),
                    ],
                ),
                ft.Row(
                    spacing=5,
                    controls=[
                        DigitButton("0", self.button_clicked, expand=2),
                        DigitButton(".", self.button_clicked),
                        ActionButton("=", self.button_clicked),
                    ],
                ),
                ft.Row(
                    spacing=5,
                    controls=[
                        DigitButton("(", self.button_clicked),
                        DigitButton(")", self.button_clicked),
                        ActionButton("√", self.button_clicked),
                        ActionButton("^", self.button_clicked),
                    ],
                ),
                ft.Row(
                    spacing=5,
                    controls=[
                        ActionButton("!", self.button_clicked),
                        ActionButton("sin", self.button_clicked),
                        ActionButton("cos", self.button_clicked),
                        ActionButton("tan", self.button_clicked),
                    ],
                ),
            ],
        )

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True

    def button_clicked(self, e):
        data = e.control.data
        print(f"Button clicked with data = {data}")
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", "π", "(", ")"):
            if self.result.value == "0" or self.new_operand == True:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value = self.result.value + data

        elif data in ("+", "-", "*", "/"):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.operator = data
            if self.result.value == "Error":
                self.operand1 = "0"
            else:
                self.operand1 = float(self.result.value)
            self.new_operand = True

        elif data in ("="):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()

        elif data in ("%"):
            self.result.value = float(self.result.value) / 100
            self.reset()

        elif data in ("+/-"):
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)

            elif float(self.result.value) < 0:
                self.result.value = str(
                    self.format_number(abs(float(self.result.value)))
                )
        elif data == "√":
            if float(self.result.value) >= 0:
                self.result.value = self.format_number(math.sqrt(float(self.result.value)))
            else:
                self.result.value = "Error"
            self.new_operand = True
        
        elif data == "^":
            self.operator = "^"
            self.operand1 = float(self.result.value)
            self.new_operand = True
    
        elif data == "sin":
            try:
                self.result.value = self.format_number(math.sin(math.radians(float(self.result.value))))
            except:
                self.result.value = "Error"
            self.new_operand = True
    
        elif data == "cos":
            try:
                self.result.value = self.format_number(math.cos(math.radians(float(self.result.value))))
            except:
                self.result.value = "Error"
            self.new_operand = True
    
        elif data == "tan":
            try:
                self.result.value = self.format_number(math.tan(math.radians(float(self.result.value))))
            except:
                self.result.value = "Error"
            self.new_operand = True
    
        elif data == "!":
            try:
                self.result.value = self.format_number(math.factorial(int(self.result.value)))
            except:
                self.result.value = "Error"
            self.new_operand = True
        self.update()

    def format_number(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num

    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            return self.format_number(operand1 + operand2)
        elif operator == "-":
            return self.format_number(operand1 - operand2)
        elif operator == "*":
            return self.format_number(operand1 * operand2)
        elif operator == "/":
            if operand2 == 0:
                return "Error"
            else:
                return self.format_number(operand1 / operand2)
        elif operator == "^":
            return self.format_number(operand1 ** operand2)


def main(page: ft.Page):
    page.title = "Calc App"
    calc = CalculatorApp()

    page.add(calc)


ft.app(target=main)
