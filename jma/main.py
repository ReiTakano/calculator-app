import flet as ft
import requests
from datetime import datetime
from typing import Dict

# 地域コードをキーにして地域名を取得できるようにする
area_cache: Dict[str, Dict] = {}

def main(page: ft.Page):
    page.title = "地域ごとの天気を予報するぜ"
    page.theme_mode = "light"

    progress_bar = ft.ProgressBar(visible=False)

    # エラーメッセージを表示する
    def show_error(message: str):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            action="閉じる",
            bgcolor=ft.colors.ERROR,
        )
        page.snack_bar.open = True
        page.update()

    # 地域リスト
    region_list_view = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
    )

    # 天気予報
    forecast_view = ft.Column(
        expand=True,
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
    )

    def fetch_data(url: str) -> Dict:
        try:
            response = requests.get(url)
            response.raise_for_status()  
            return response.json()
        except requests.RequestException as e:
            show_error(f"データ取得エラー: {str(e)}")
            return {}

    def load_region_list():
        try:
            progress_bar.visible = True
            page.update()

            data = fetch_data("http://www.jma.go.jp/bosai/common/const/area.json")
            if "offices" in data:
                area_cache.update(data["offices"])
                update_region_menu()
            else:
                show_error("地域データの形式が予期したものと異なります。")
        except Exception as e:
            show_error(f"地域データの読み込みに失敗しました: {str(e)}")
        finally:
            progress_bar.visible = False
            page.update()

    def update_region_menu():
        region_list_view.controls.clear()
        for code, area in area_cache.items():
            region_list_view.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.icons.LOCATION_ON),
                    title=ft.Text(area["name"]),
                    subtitle=ft.Text(f"地域コード: {code}"),
                    on_click=lambda e, code=code: load_forecast(code),
                )
            )
        page.update()

    def load_forecast(region_code: str):
        try:
            progress_bar.visible = True
            page.update()

            url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{region_code}.json"
            data = fetch_data(url)

            if data:
                display_forecast(data)
            else:
                show_error("天気予報データが見つかりません。")
        except Exception as e:
            show_error(f"天気予報の取得に失敗しました: {str(e)}")
        finally:
            progress_bar.visible = False
            page.update()

    # 天気予報を表示
    def display_forecast(data: Dict):
        forecast_view.controls.clear()
        forecasts = data[0]["timeSeries"][0]  
    # 予報日時と天気を表示
        for i, date in enumerate(forecasts["timeDefines"]):
            weather_code = forecasts["areas"][0]["weatherCodes"][i]
            forecast_view.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(format_date(date), size=18, weight="bold"),
                                ft.Text(get_weather_text(weather_code)),
                                ft.Text(get_weather_icon(weather_code), size=40),  
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        padding=10,
                    )
                )
            )
        page.update()

    # 天気予報サイトのデザイん
    page.add(
        ft.Row(
            [
                ft.Container(
                    width=300,
                    content=region_list_view,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                ),
                ft.Container(
                    expand=True,
                    content=forecast_view,
                ),
            ],
            expand=True,
        ),
        progress_bar,
    )

    # データの読み込み
    load_region_list()

# ここで定義した関数は、他の関数から呼び出すことができる
def format_date(date_str: str) -> str:
# 日付を日本語表記に変換
    date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    return date.strftime("%Y年%m月%d日")

def get_weather_text(code: str) -> str:
# 天気コードに対応する天気を返す
    weather_codes = {
        "100": "晴れ",
        "101": "晴れ時々曇り",
        "102": "晴れ時々雨",
        "200": "曇り",
        "201": "曇り時々晴れ",
        "202": "曇り時々雨",
        "218": "曇り時々雪",
        "270": "雪時々曇り",
        "300": "雨",
        "400": "雪",
        "500": "雷雨",
        "413": "雪のち雨",
        "206": "雨時々曇り",
        "111": "雨時々晴れ",
        "112": "雨時々雪",
        "211": "雪時々晴れ",
        "206": "雨時々曇り",
        "212": "雪時々曇り",
        "313": "雪のち雨",
        "314": "雨のち雪",
        "203": "曇り時々雪",
        "302": "雪",
        "114": "雪時々晴れ",
    }
    return weather_codes.get(code, f"不明な天気 (コード: {code})")

def get_weather_icon(code: str) -> str:
# 天気コードに対応する絵文字を返す
    weather_icons = {
        "100": "☀️",  # 晴れ
        "101": "🌤️",  # 晴れ時々曇り
        "102": "🌦️",  # 晴れ時々雨
        "200": "☁️",  # 曇り
        "300": "🌧️",  # 雨
        "400": "❄️",  # 雪
        "500": "⛈️",  # 雷雨
        "413": "❄️→🌧️",  # 雪のち雨
        "314": "🌧️→❄️",  # 雨のち雪
        "201": "🌤️",
        "202": "☁️🌧️",
        "218": "☁️❄️",
        "270": "❄️☁️",
        "206": "🌧️☁️",
        "111": "🌧️☀️",
        "112": "🌧️❄️",
        "211": "❄️☀️",
        "212": "❄️☁️",
        "313": "❄️🌧️",
        "203": "☁️❄️",
        "302": "❄️",
        "114": "❄️☀️",


        
    }
    # 聞いたことも無い天気の場合は❓を返す
    return weather_icons.get(code, "❓") 

# 起動
ft.app(target=main)
