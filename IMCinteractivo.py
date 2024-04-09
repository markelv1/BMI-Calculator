import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class IMCCalculator(App):
    # Create Interface
    def build(self):
        # Main
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=40)

        # Title
        welcome_label = Label(text='Body mass index calculator (BMI)', font_size=20)
        self.layout.add_widget(welcome_label)

        # User input labels
        self.weight_input = TextInput(hint_text='Enter your weight in kg', size_hint=(1, None), height=30)
        self.height_input = TextInput(hint_text='Enter your height in meters', size_hint=(1, None), height=30)

        self.layout.add_widget(self.weight_input)
        self.layout.add_widget(self.height_input)

        # Button to run
        calculate_button = Button(text='Calculate BMI')
        calculate_button.bind(on_press=self.calculate_imc)
        self.layout.add_widget(calculate_button)

        return self.layout
    
    # Calculate IMC
    def calculate_imc(self, instance):
        weight = self.weight_input.text
        height = self.height_input.text
        try:
            weight = float(weight)
            height = float(height)
            if height == 0:
                raise ValueError("La altura no puede ser cero.")
            imc = weight / (height ** 2)
            category = self.interpret_imc(imc)
            self.show_result(imc, category)
            self.save_data(weight, height, imc, category)
        except ValueError as e:
            self.show_error(str(e))

    # Console Answer to input
    def interpret_imc(self, imc):
        if imc < 18.5:
            return "Underweight"
        elif 18.5 <= imc < 25:
            return "Normal"
        elif 25 <= imc < 30:
            return "Overweight"
        else:
            return "Obesity"

    # Show results
    def show_result(self, imc, category):
        result_label = Label(text=f"Your BMI is: {imc:.2f}\nCategory: {category}", size_hint=(None, None), size=(400, 100))
        add_data_button = Button(text='Add more', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5})
        add_data_button.bind(on_press=self.clear_inputs)
        
        content_layout = BoxLayout(orientation='vertical')
        content_layout.add_widget(result_label)
        content_layout.add_widget(add_data_button)

        self.popup = Popup(title='Results', content=content_layout, size_hint=(None, None), size=(400, 200))
        self.popup.open()

    # Show error
    def show_error(self, message):
        popup_content = f"Error: {message}"
        popup = Popup(title='Error', content=Label(text=popup_content), size_hint=(None, None), size=(400, 200))
        popup.open()

        return self.popup

    # Clear previous inputs
    def clear_inputs(self, instance):
        self.weight_input.text = ''
        self.height_input.text = ''
        self.popup.dismiss() 

    # Save data on json file   
    def save_data(self, weight, height, imc, category):
        data = {
            "weight": weight,
            "height": height,
            "imc": imc,
            "ategory": category
        }
        file_path = "IMC.json"
        if os.path.exists(file_path) and os.stat(file_path).st_size > 0:
            with open(file_path, 'r') as file:
                try:
                    data_list = json.load(file)
                except json.decoder.JSONDecodeError:
                    data_list = []
        else:
            data_list = []

        data_list.append(data)

        with open(file_path, 'w') as file:
            json.dump(data_list, file, indent=4)

if __name__ == '__main__':
    IMCCalculator().run()
