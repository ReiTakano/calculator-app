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