import os
import subprocess
import json
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

API_KEY = "YOUR_GEMINI_API_KEY_HERE"  # तुमचा API Key येथे टाका

class VoiceAssistantUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=20, **kwargs)
        
        self.status_label = Label(
            text="AI Voice Assistant Ready!",
            font_size='20sp',
            halign='center'
        )
        self.add_widget(self.status_label)
        
        self.listen_btn = Button(
            text="🎙️ बोला (Listen)",
            font_size='24sp',
            background_color=(0.2, 0.6, 1, 1),
            size_hint=(1, 0.4)
        )
        self.listen_btn.bind(on_press=self.start_assistant)
        self.add_widget(self.listen_btn)

    def speak(self, text):
        self.status_label.text = f"AI: {text}"
        subprocess.run(["termux-tts-speak", text])

    def start_assistant(self, instance):
        self.status_label.text = "ऐकत आहे... बोलण्यास सुरुवात करा"
        Clock.schedule_once(self.process_voice, 0.5)

    def process_voice(self, dt):
        # Voice Recognition
        res = subprocess.run(["termux-speech-to-text"], capture_output=True, text=True)
        user_text = res.stdout.strip()
        
        if user_text:
            self.status_label.text = f"You: {user_text}"
            
            # Gemini Call
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": f"You are a helpful voice assistant. Keep answers short and friendly (1-2 sentences). Respond in Marathi/English based on input: {user_text}"}]}]
            }
            try:
                r = requests.post(url, json=payload)
                if r.status_code == 200:
                    ai_reply = r.json()['candidates'][0]['content']['parts'][0]['text']
                    self.speak(ai_reply)
                else:
                    self.speak("API एरर आला आहे.")
            except:
                self.speak("इंटरनेट तपासा.")
        else:
            self.status_label.text = "आवाज ऐकू आला नाही. पुन्हा प्रयत्न करा."

class AssistantApp(App):
    def build(self):
        return VoiceAssistantUI()

if __name__ == "__main__":
    AssistantApp().run()
