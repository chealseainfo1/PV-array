from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
import math

class First(Screen):
    pass

class SolarCalculator(Screen):
    def calculate(self):
        if not self.ids.load_input.text:
            self.ids.results.text = "Please enter total load."
            return

        load = int(self.ids.load_input.text)
        load_kw = load / 1000

        # Inverter sizing (min–max)
        inverter_min = round(load_kw * 1.1, 1)
        inverter_max = round(load_kw * 1.8, 1)

        # Snap to common inverter sizes
        def snap(size):
            for s in (3, 5, 8, 10):
                if size <= s:
                    return s
            return 10

        inverter_min = snap(inverter_min)
        inverter_max = snap(inverter_max)

        # Lithium battery energy requirement
        battery_kwh = round(load_kw * 6, 1)

        # 10 kWh battery calculation
        battery_unit_kwh = 10
        batteries_needed = math.ceil(battery_kwh / battery_unit_kwh)

        # Solar sizing
        solar_kw = round((battery_kwh / 5.5) * 1.15, 2)

        panels_400_min = math.ceil((solar_kw * 1000) / 400)
        panels_400_max = panels_400_min + 2

        panels_600_min = math.ceil((solar_kw * 1000) / 600)
        panels_600_max = panels_600_min + 2

        self.ids.results.text = (
            f"Hi! for a total running load of {load} W, the recommended inverter size is "
            f"{inverter_min + .5}–{inverter_max} kW, with a battery capacity of {battery_kwh}–{battery_kwh + 5} kWh lithium "
            f"approx {batteries_needed} batteries of 10 kWh. "
            f"The PV array is about {solar_kw}–{solar_kw + 1} kW "
            f"approx {panels_400_min}–{panels_400_max} panels of 400 W or "
            f"{panels_600_min}–{panels_600_max} panels of 600 W.\n\n"
        )

    def clear(self):
        self.ids.load_input.text = ""
        self.ids.results.text = ""

Builder.load_file("solar.kv")

class SolarApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(First())
        sm.add_widget(SolarCalculator())
        return sm

if __name__ == "__main__":
    SolarApp().run()
