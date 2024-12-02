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

    # 地域の番号リスト
    region_list_view = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
    )

    # 天気を予報する部分
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

    def display_forecast(data: Dict):
        forecast_view.controls.clear()
        try:
            weekly_data = data[1]  # 週間予報データ
            weather_forecasts = weekly_data["timeSeries"][0]
            temp_forecasts = weekly_data["timeSeries"][1]
            
            # グリッドビューの作成
            grid = ft.GridView(
                expand=True,
                runs_count=4,
                max_extent=200,
                child_aspect_ratio=0.8,
                spacing=10,
                run_spacing=10,
                padding=20,
            )
            # 1週間分の予報を表示するぞ
            for i in range(len(weather_forecasts["timeDefines"])):
                date = weather_forecasts["timeDefines"][i]
                weather_code = weather_forecasts["areas"][0]["weatherCodes"][i]
                
                try:
                    min_temp = temp_forecasts["areas"][0]["tempsMin"][i]
                    max_temp = temp_forecasts["areas"][0]["tempsMax"][i]
                except (IndexError, KeyError):
                    min_temp = max_temp = "--"

                # 予報を表示する部分を作る
                card = ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(format_date(date), size=16, weight="bold"),
                                ft.Text(get_weather_icon(weather_code), size=25),
                                ft.Text(get_weather_text(weather_code), size=16),
                                ft.Text(
                                    f"最低 {min_temp if min_temp != '--' else '不明'}°C",
                                    size=16,
                                    color=ft.colors.BLUE,
                                    weight="bold",
                                ),
                                ft.Text(
                                    f"最高 {max_temp if max_temp != '--' else '不明'}°C",
                                    size=16,
                                    color=ft.colors.RED,
                                    weight="bold",
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        padding=20,
                    )
                )
                grid.controls.append(card)
            
            forecast_view.controls.append(grid)
            
        except (KeyError, IndexError) as e:
            show_error("週間予報データの取得に失敗しました。")
        
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
# 日付をフォーマットする
def format_date(date_str: str) -> str:
    date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    weekdays = ["月", "火", "水", "木", "金", "土", "日"]
    weekday = weekdays[date.weekday()]
    return f"{date.month}/{date.day}\n({weekday})"

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
        "402": "大雪",
        "204": "雪時々雨",
        "207": "雷雨時々雪",
        "205": "雨時々雪",
        "209": "雪時々雷雨",
        "210": "雷雨時々雪",
        "260": "雷雨時々曇り",
    }
    return weather_codes.get(code, f"不明な天気 (コード: {code})")

def get_weather_icon(code: str) -> str:
    # 天気コードに対応する絵文字を返す
    weather_icons = {
        "100": "☀️",  # 晴れ
        "101": "🌤️",  # 晴れ時々曇り
        "102": "🌦️",  # 晴れ時々雨
        "200": "☁️",  # 曇り
        "300": "🌧️", 
        "400": "❄️", 
        "500": "⛈️", 
        "413": "❄️→🌧️", 
        "314": "🌧️→❄️", 
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
        "402": "❄️❄️❄️",
        "204": "❄️🌧️",
        "207": "⛈️❄️",
        "205": "🌧️❄️",
        "209": "❄️⛈️",
        "210": "⛈️❄️",
        "260": "⛈️☁️",
    }
    # 聞いたことも無いような天気コードの場合は❓を返す
    return weather_icons.get(code, "❓")

# 起動する
if __name__ == "__main__":
    ft.app(target=main)