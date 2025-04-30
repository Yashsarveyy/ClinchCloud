import sys
import requests
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                             QHBoxLayout, QLineEdit, QPushButton, QMessageBox,
                             QFrame, QScrollArea, QComboBox)
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt, QTimer, QTime, QDateTime

API_KEY = "431d95df0ad4f1017180132ffbaad5d8"

# Helper: Get coordinates from city name
def get_coordinates(city_name):
    try:
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        if not data:
            return None, None, None, None
        return data[0]['lat'], data[0]['lon'], data[0]['name'], data[0]['country']
    except requests.HTTPError as e:
        if res.status_code == 401:
            QMessageBox.critical(None, "API Error", "Unauthorized Access. Check your OpenWeather API Key.")
        elif res.status_code == 404:
            QMessageBox.critical(None, "API Error", "City not found. Please check the city name.")
        else:
            QMessageBox.critical(None, "API Error", f"HTTP Error: {e}")
    except requests.RequestException as e:
        QMessageBox.critical(None, "Network Error", f"Network problem: {e}")
    return None, None, None, None

# Helper: Fetch current + daily weather
def fetch_weather(lat, lon, units="metric"):
    try:
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&units={units}&appid={API_KEY}"
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except requests.HTTPError as e:
        if res.status_code == 401:
            QMessageBox.critical(None, "API Error", "Unauthorized Access. Check your OpenWeather API Key.")
        else:
            QMessageBox.critical(None, "API Error", f"HTTP Error: {e}")
    except requests.RequestException as e:
        QMessageBox.critical(None, "Network Error", f"Network problem: {e}")
    return None

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 850, 550)
        self.unit = "metric"
        self.dark_theme = False
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Top Bar
        top_bar = QHBoxLayout()
        self.time_label = QLabel("--:-- AM")
        self.time_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.location_label = QLabel("")
        self.location_label.setFont(QFont("Arial", 14))
        self.location_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        top_bar.addWidget(self.time_label)
        top_bar.addWidget(self.location_label)
        self.layout.addLayout(top_bar)

        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.update_time()

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter city name")
        self.search_input.setFont(QFont("Arial", 16))

        search_btn = QPushButton("🔍")
        search_btn.clicked.connect(self.perform_search)

        self.unit_toggle = QComboBox()
        self.unit_toggle.addItems(["Celsius", "Fahrenheit"])
        self.unit_toggle.currentIndexChanged.connect(self.change_unit)

        theme_btn = QPushButton("Toggle Theme")
        theme_btn.clicked.connect(self.toggle_theme)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        search_layout.addWidget(self.unit_toggle)
        search_layout.addWidget(theme_btn)
        self.layout.addLayout(search_layout)

        # Current Weather
        self.current_icon = QLabel()
        self.current_icon.setFixedSize(100, 100)

        self.current_info = QLabel("<b>Current Weather:</b>")
        self.current_info.setFont(QFont("Arial", 14))
        self.current_info.setAlignment(Qt.AlignmentFlag.AlignLeft)

        current_layout = QHBoxLayout()
        current_layout.addWidget(self.current_icon)
        current_layout.addWidget(self.current_info)
        self.layout.addLayout(current_layout)

        # Forecast area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.forecast_layout = QHBoxLayout(scroll_content)
        self.scroll_area.setWidget(scroll_content)
        self.layout.addWidget(self.scroll_area)

    def update_time(self):
        now = QTime.currentTime()
        hours = now.hour()
        minutes = now.minute()
        am_pm = "AM" if hours < 12 else "PM"
        display_hours = hours % 12 or 12
        self.time_label.setText(f"{display_hours:02}:{minutes:02} {am_pm}")

    def change_unit(self):
        self.unit = "metric" if self.unit_toggle.currentText() == "Celsius" else "imperial"
        self.perform_search()

    def toggle_theme(self):
        self.dark_theme = not self.dark_theme
        if self.dark_theme:
            self.setStyleSheet("background-color: #212121; color: white;")
        else:
            self.setStyleSheet("background-color: #e0f7fa; color: black;")

    def perform_search(self):
        city = self.search_input.text().strip()
        if not city:
            QMessageBox.warning(self, "Input Error", "Please enter a city name.")
            return

        lat, lon, name, country = get_coordinates(city)
        if lat is None:
            # Error message already shown inside get_coordinates()
            return

        data = fetch_weather(lat, lon, self.unit)
        if data is None:
            # Error message already shown inside fetch_weather()
            return

        self.show_weather(data, name, country, lat, lon)

    def show_weather(self, data, name, country, lat, lon):
        unit_symbol = "°C" if self.unit == "metric" else "°F"
        self.location_label.setText(f"{name}, {country}")

        current = data['current']
        temp = current['temp']
        desc = current['weather'][0]['description'].title()
        humidity = current['humidity']
        pressure = current['pressure']
        wind = current['wind_speed']
        icon_code = current['weather'][0]['icon']

        # Load icon
        pixmap = QPixmap()
        pixmap.loadFromData(requests.get(f"http://openweathermap.org/img/wn/{icon_code}@2x.png").content)
        self.current_icon.setPixmap(pixmap.scaled(100, 100))

        self.current_info.setText(
            f"<b>Temperature:</b> {temp}{unit_symbol} | "
            f"<b>Humidity:</b> {humidity}% | "
            f"<b>Pressure:</b> {pressure}hPa | "
            f"<b>Wind:</b> {wind}m/s | "
            f"<b>{desc}</b>"
        )

        # Clear old forecast cards
        while self.forecast_layout.count():
            item = self.forecast_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Create new forecast cards
        for day in data['daily'][:7]:
            day_name = QDateTime.fromSecsSinceEpoch(day['dt']).toString("dddd")
            day_temp = round(day['temp']['day'], 1)
            night_temp = round(day['temp']['night'], 1)
            day_icon = day['weather'][0]['icon']

            card_widget = QWidget()
            card_layout = QVBoxLayout(card_widget)

            icon_label = QLabel()
            icon_pixmap = QPixmap()
            icon_pixmap.loadFromData(requests.get(f"http://openweathermap.org/img/wn/{day_icon}@2x.png").content)
            icon_label.setPixmap(icon_pixmap.scaled(50, 50))
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            text_label = QLabel(f"<b>{day_name}</b>\n{day_temp}{unit_symbol} / {night_temp}{unit_symbol}")
            text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            text_label.setFont(QFont("Arial", 11))
            text_label.setWordWrap(True)

            card_layout.addWidget(icon_label)
            card_layout.addWidget(text_label)
            card_widget.setFixedWidth(110)

            if self.dark_theme:
                card_widget.setStyleSheet("background-color: #37474F; color: white; border-radius: 8px;")
            else:
                card_widget.setStyleSheet("background-color: #b2ebf2; color: black; border-radius: 8px;")

            self.forecast_layout.addWidget(card_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())