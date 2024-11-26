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


import flet as ft


def main(page: ft.Page):
    page.title = "Calc App"
    result = ft.Text(value="0")

    page.add(
        result,
        ft.ElevatedButton(text="AC"),
        ft.ElevatedButton(text="+/-"),
        ft.ElevatedButton(text="%"),
        ft.ElevatedButton(text="/"),
        ft.ElevatedButton(text="7"),
        ft.ElevatedButton(text="8"),
        ft.ElevatedButton(text="9"),
        ft.ElevatedButton(text="*"),
        ft.ElevatedButton(text="4"),
        ft.ElevatedButton(text="5"),
        ft.ElevatedButton(text="6"),
        ft.ElevatedButton(text="-"),
        ft.ElevatedButton(text="1"),
        ft.ElevatedButton(text="2"),
        ft.ElevatedButton(text="3"),
        ft.ElevatedButton(text="+"),
        ft.ElevatedButton(text="0"),
        ft.ElevatedButton(text="."),
        ft.ElevatedButton(text="="),
        ft.ElevatedButton(text="√"),
        ft.ElevatedButton(text="^"),
        ft.ElevatedButton(text="sin"),
        ft.ElevatedButton(text="cos"),
        ft.ElevatedButton(text="tan"),
        ft.ElevatedButton(text="π"),
        ft.ElevatedButton(text="("),
        ft.ElevatedButton(text=")"),
        ft.ElevatedButton(text="x"),
        ft.ElevatedButton(text="!"),
    )


ft.app(target=main)

import flet as ft


def main(page: ft.Page):
    page.title = "Calc App"
    result = ft.Text(value="0")

    page.add(
        ft.Row(controls=[result]),
        ft.Row(
            controls=[
                ft.ElevatedButton(text="AC"),
                ft.ElevatedButton(text="+/-"),
                ft.ElevatedButton(text="%"),
                ft.ElevatedButton(text="/"),
                ft.ElevatedButton(text="√"),
                ft.ElevatedButton(text="^"),
            ]
        ),
        ft.Row(
            controls=[
                ft.ElevatedButton(text="7"),
                ft.ElevatedButton(text="8"),
                ft.ElevatedButton(text="9"),
                ft.ElevatedButton(text="*"),
                ft.ElevatedButton(text="π"),
            ]
        ),
        ft.Row(
            controls=[
                ft.ElevatedButton(text="4"),
                ft.ElevatedButton(text="5"),
                ft.ElevatedButton(text="6"),
                ft.ElevatedButton(text="-"),
            ]
        ),
        ft.Row(
            controls=[
                ft.ElevatedButton(text="1"),
                ft.ElevatedButton(text="2"),
                ft.ElevatedButton(text="3"),
                ft.ElevatedButton(text="+"),
            ]
        ),
        ft.Row(
            controls=[
                ft.ElevatedButton(text="0"),
                ft.ElevatedButton(text="."),
                ft.ElevatedButton(text="="),
            ]
        ),
        ft.Row(
            controls=[
                ft.ElevatedButton(text="sin"),
                ft.ElevatedButton(text="cos"),
                ft.ElevatedButton(text="tan"),
                ft.ElevatedButton(text="("),
                ft.ElevatedButton(text=")"),
                ft.ElevatedButton(text="!"),
            ]
        ),
    )


ft.app(target=main)


import flet as ft


def main(page: ft.Page):
    page.title = "Calc App"
    result = ft.Text(value="0", color=ft.colors.WHITE, size=20)

    class CalcButton(ft.ElevatedButton):
        def __init__(self, text, expand=1):
            super().__init__()
            self.text = text
            self.expand = expand

    class DigitButton(CalcButton):
        def __init__(self, text, expand=1):
            CalcButton.__init__(self, text, expand)
            self.bgcolor = ft.colors.WHITE24
            self.color = ft.colors.WHITE

    class ActionButton(CalcButton):
        def __init__(self, text):
            CalcButton.__init__(self, text)
            self.bgcolor = ft.colors.ORANGE
            self.color = ft.colors.WHITE

    class ExtraActionButton(CalcButton):
        def __init__(self, text):
            CalcButton.__init__(self, text)
            self.bgcolor = ft.colors.BLUE_GREY_100
            self.color = ft.colors.BLACK

    page.add(
        ft.Container(
            width=350,
            bgcolor=ft.colors.BLACK,
            border_radius=ft.border_radius.all(20),
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Row(controls=[result], alignment="end"),
                    ft.Row(
                        controls=[
                            ExtraActionButton(text="AC"),
                            ExtraActionButton(text="+/-"),
                            ExtraActionButton(text="%"),
                            ActionButton(text="/"),
                            ActionButton(text="√"),
                            ActionButton(text="^"),
                    
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(text="7"),
                            DigitButton(text="8"),
                            DigitButton(text="9"),
                            ActionButton(text="*"),
                            DigitButton(text="π"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(text="4"),
                            DigitButton(text="5"),
                            DigitButton(text="6"),
                            ActionButton(text="-"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(text="1"),
                            DigitButton(text="2"),
                            DigitButton(text="3"),
                            ActionButton(text="+"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(text="0", expand=2),
                            DigitButton(text="."),
                            ActionButton(text="="),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(text="sin"),
                            DigitButton(text="cos"),
                            DigitButton(text="tan"),
                            DigitButton(text="("),
                            DigitButton(text=")"),
                            DigitButton(text="!"),
                        ]
                    ),
                ]
            ),
        )
    )


ft.app(target=main)

import flet as ft
import math

# ベースボタンクラス
class CalcButton(ft.ElevatedButton):
    def __init__(self, text, on_click, expand=1):
        super().__init__(text=text, on_click=on_click, expand=expand)


class DigitButton(CalcButton):
    def __init__(self, text, on_click, expand=1):
        super().__init__(text, on_click, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, on_click):
        super().__init__(text, on_click)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE

class ExtraActionButton(CalcButton):
    def __init__(self, text, on_click):
        super().__init__(text, on_click)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK

class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
        self.current_value = ["0"]  

        def button_clicked(e):
            data = e.control.text
            if data == "AC":
                self.current_value[0] = "0"
            elif data == "+/-":
                self.toggle_sign()
            elif data == "%":
                self.calculate_percent()
            elif data == "=":
                self.calculate_result()
            elif data == "√":
                self.calculate_square_root()
            elif data == "^":
                self.current_value[0] += "**"
            elif data == "π":
                self.current_value[0] = str(math.pi)
            elif data in ("sin", "cos", "tan"):
                self.calculate_trigonometric(data)
            elif data == "!":
                self.calculate_factorial()
            else:
                self.handle_input(data)

            self.result.value = self.current_value[0]
            self.update()

        self.width = 350
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        ExtraActionButton(text="AC", on_click=button_clicked),
                        ExtraActionButton(text="+/-", on_click=button_clicked),
                        ExtraActionButton(text="%", on_click=button_clicked),
                        ActionButton(text="/", on_click=button_clicked),
                        ActionButton(text="√", on_click=button_clicked),
                        ActionButton(text="^", on_click=button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="7", on_click=button_clicked),
                        DigitButton(text="8", on_click=button_clicked),
                        DigitButton(text="9", on_click=button_clicked),
                        ActionButton(text="*", on_click=button_clicked),
                        DigitButton(text="π", on_click=button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="4", on_click=button_clicked),
                        DigitButton(text="5", on_click=button_clicked),
                        DigitButton(text="6", on_click=button_clicked),
                        ActionButton(text="-", on_click=button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="1", on_click=button_clicked),
                        DigitButton(text="2", on_click=button_clicked),
                        DigitButton(text="3", on_click=button_clicked),
                        ActionButton(text="+", on_click=button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="0", expand=2, on_click=button_clicked),
                        DigitButton(text=".", on_click=button_clicked),
                        ActionButton(text="=", on_click=button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="(", on_click=button_clicked),
                        DigitButton(text=")", on_click=button_clicked),
                        DigitButton(text="x", on_click=button_clicked),
                        ExtraActionButton(text="!", on_click=button_clicked),
                        ExtraActionButton(text="sin", on_click=button_clicked),
                        ExtraActionButton(text="cos", on_click=button_clicked),
                        ExtraActionButton(text="tan", on_click=button_clicked),
                    ]
                ),
            ]
        )

    def toggle_sign(self):
        if self.current_value[0].startswith("-"):
            self.current_value[0] = self.current_value[0][1:]
        else:
            self.current_value[0] = "-" + self.current_value[0]

    def calculate_percent(self):
        try:
            self.current_value[0] = str(float(self.current_value[0]) / 100)
        except:
            self.current_value[0] = "Error"

    def calculate_result(self):
        try:
            self.current_value[0] = str(eval(self.current_value[0]))
        except:
            self.current_value[0] = "Error"

    def calculate_square_root(self):
        try:
            self.current_value[0] = str(float(self.current_value[0]) ** 0.5)
        except:
            self.current_value[0] = "Error"

    def calculate_trigonometric(self, function):
        try:
            value = float(self.current_value[0])
            if function == "sin":
                self.current_value[0] = str(math.sin(math.radians(value)))
            elif function == "cos":
                self.current_value[0] = str(math.cos(math.radians(value)))
            elif function == "tan":
                self.current_value[0] = str(math.tan(math.radians(value)))
        except:
            self.current_value[0] = "Error"

    def calculate_factorial(self):
        try:
            self.current_value[0] = str(math.factorial(int(float(self.current_value[0]))))
        except:
            self.current_value[0] = "Error"

    def handle_input(self, data):
        if self.current_value[0] == "0":
            self.current_value[0] = data
        else:
            self.current_value[0] += data


def main(page: ft.Page):
    page.title = "Calc App"
    calc = CalculatorApp()
    page.add(calc)


ft.app(target=main)

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

        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
        self.width = 350
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        ExtraActionButton(text="AC", button_clicked=self.button_clicked),
                        ExtraActionButton(text="+/-", button_clicked=self.button_clicked),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="/", button_clicked=self.button_clicked),
                        ActionButton(text="√", button_clicked=self.button_clicked),
                        ActionButton(text="^", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                        DigitButton(text="π", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="0", expand=2, button_clicked=self.button_clicked),
                        DigitButton(text=".", button_clicked=self.button_clicked),
                        ActionButton(text="=", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(text="sin", button_clicked=self.button_clicked),
                        ExtraActionButton(text="cos", button_clicked=self.button_clicked),
                        ExtraActionButton(text="tan", button_clicked=self.button_clicked),
                        ExtraActionButton(text="(", button_clicked=self.button_clicked),
                        ExtraActionButton(text=")", button_clicked=self.button_clicked),
                        ExtraActionButton(text="!", button_clicked=self.button_clicked),
                    ]
                ),
            ]
        )

    def button_clicked(self, e):
        data = e.control.data
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()
        elif data == "√":
            try:
                value = float(self.result.value)
                if value < 0:
                    self.result.value = "Error"
                else:
                    self.result.value = self.format_number(math.sqrt(value))
            except:
                self.result.value = "Error"
        elif data == "^":
            self.operator = "^"
            self.operand1 = float(self.result.value)
            self.new_operand = True
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", "π", "(", ")"):
            if data == "π":
                self.result.value = str(math.pi)
            elif self.result.value == "0" or self.new_operand == True:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value = self.result.value + data
        elif data in ("+", "-", "*", "/"):
            self.result.value = self.calculate(self.operand1, float(self.result.value), self.operator)
            self.operator = data
            if self.result.value == "Error":
                self.operand1 = "0"
            else:
                self.operand1 = float(self.result.value)
            self.new_operand = True
        elif data == "=":
            self.result.value = self.calculate(self.operand1, float(self.result.value), self.operator)
            self.reset()
        elif data == "%":
            self.result.value = float(self.result.value) / 100
            self.reset()
        elif data == "+/-":
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)
            elif float(self.result.value) < 0:
                self.result.value = str(self.format_number(abs(float(self.result.value))))
        elif data in ("sin", "cos", "tan"):
            try:
                if data == "sin":
                    self.result.value = self.format_number(math.sin(math.radians(float(self.result.value))))
                elif data == "cos":
                    self.result.value = self.format_number(math.cos(math.radians(float(self.result.value))))
                elif data == "tan":
                    self.result.value = self.format_number(math.tan(math.radians(float(self.result.value))))
            except:
                self.result.value = "Error"
            self.new_operand = True
        elif data == "!":
            try:
                self.result.value = self.format_number(math.factorial(int(float(self.result.value))))
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
        try:
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
        except:
            return "Error"

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True

def main(page: ft.Page):
    page.title = "Calc App"
    calc = CalculatorApp()
    page.add(calc)

ft.app(target=main)