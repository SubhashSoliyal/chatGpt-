# import tkinter as tk
# import speech_recognition as sr
# import pyttsx3
# # import openai_secret_manager
import openai
import os

# # Set up OpenAI API credentials
# # secrets = openai_secret_manager.get_secret("openai")
# # openai.api_key = secrets["api_key"]
openai.api_key =os.getenv("OPENAI_API_KEY")

# # Create a recognizer object and a text-to-speech object
# r = sr.Recognizer()
# engine = pyttsx3.init()

# def listen():
#     # Use the default microphone as the audio source
#     with sr.Microphone() as source:
#         # Adjust for ambient noise
#         r.adjust_for_ambient_noise(source)

#         # Prompt the user to speak
#         status_text.set("Listening...")
#         window.update()
#         audio = r.listen(source)
#         status_text.set("Recognizing...")

#     # Use Google Speech Recognition to transcribe the audio
#     try:
#         text = r.recognize_google(audio)
#         status_text.set(f"You said: {text}")
#         window.update()
#         return text
#     except sr.UnknownValueError:
#         status_text.set("Could not understand audio")
#         window.update()
#         return None
#     except sr.RequestError as e:
#         status_text.set(f"Could not request results from Google Speech Recognition service; {e}")
#         window.update()
#         return None

# def speak(text):
#     # Set the text-to-speech voice and rate
#     voices = engine.getProperty('voices')
#     engine.setProperty('voice', voices[0].id)
#     engine.setProperty('rate', 175)

#     # Convert the text to speech
#     engine.say(text)
#     engine.runAndWait()

# def query_openai(prompt):
#     # Set up the OpenAI request parameters
#     model_engine = "text-davinci-002"
#     prompt = f"{prompt}\n\nAI:"
#     max_tokens = 60
#     temperature = 0.5

#     # Generate the OpenAI response
#     response = openai.Completion.create(
#         engine=model_engine,
#         prompt=prompt,
#         max_tokens=max_tokens,
#         temperature=temperature,
#         n=1,
#         stop=None,
#         frequency_penalty=0,
#         presence_penalty=0
#     )

#     # Return the response text
#     return response.choices[0].text.strip()

# def process_input():
#     # Call the listen function to capture user's speech
#     text = listen()

#     if text is not None:
#         # Call the query_openai function to process the user's input and generate a response
#         response = query_openai(text)

#         # Call the speak function to convert the response to speech
#         speak(response)

#         # Update the status text with the response
#         status_text.set(f"AI: {response}")
#         window.update()

# # Set up the GUI
# window = tk.Tk()
# window.title("Voice AI")
# window.geometry("600x400")

# # Create the status text label
# status_text = tk.StringVar()
# status_text.set("Press the button to start")
# status_label = tk.Label(window, textvariable=status_text, font=("Arial", 14))
# status_label.pack(pady=20)

# # Create the button to process user input
# process_button = tk.Button(window, text="Process Input", font=("Arial", 14), command=process_input)
# process_button.pack(pady=20)

# # Start the GUI main loop
# window.mainloop()





import tkinter as tk
import speech_recognition as sr
import pyttsx3
# import openai_secret_manager
import openai

# Set up OpenAI API credentials
# secrets = openai_secret_manager.get_secret("openai")
# openai.api_key = secrets["api_key"]

# Create a recognizer object and a text-to-speech object
r = sr.Recognizer()
engine = pyttsx3.init()

def listen():
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        # Adjust for ambient noise
        r.adjust_for_ambient_noise(source)

        # Prompt the user to speak
        status_text.set("Listening...")
        window.update()
        audio = r.listen(source)
        status_text.set("Recognizing...")

    # Use Google Speech Recognition to transcribe the audio
    try:
        text = r.recognize_google(audio)
        status_text.set(f"You said: {text}")
        window.update()
        return text
    except sr.UnknownValueError:
        status_text.set("Could not understand audio")
        window.update()
        return None
    except sr.RequestError as e:
        status_text.set(f"Could not request results from Google Speech Recognition service; {e}")
        window.update()
        return None

def speak(text):
    # Set the text-to-speech voice and rate
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 175)

    # Convert the text to speech
    engine.say(text)
    engine.runAndWait()

def query_openai(prompt):
    # Set up the OpenAI request parameters
    model_engine = "text-davinci-002"
    prompt = f"{prompt}\n\nAI:"
    max_tokens = 60
    temperature = 0.5

    # Generate the OpenAI response
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        n=1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Return the response text
    return response.choices[0].text.strip()

def process_input():
    # Call the listen function to capture user's speech
    text = listen()

    if text is not None:
        # Call the query_openai function to process the user's input and generate a response
        response = query_openai(text)

        # Call the speak function to convert the response to speech
        speak(response)

        # Update the status text with the response
        status_text.set(f"AI: {response}")
        window.update()

def set_mode(mode):
    # Set the current mode
    global current_mode
    current_mode = mode

    # Update the status text
    status_text.set(f"Current mode: {mode}")

def create_mode_menu():
    # Create the mode menu label and scrollbar
    mode_label = tk.Label(window, text="Select a mode:", font=("Arial", 14))
    mode_label.pack(pady=20)
    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create the mode menu frame
    mode_frame = tk.Frame(window)
    mode_frame.pack(pady=20)

    # Create the mode buttons and add them to the mode menu frame
    modes = ["OpenAI", "Voice recognition"]
    for mode in modes:
        button = tk.Button(mode_frame, text=mode, font=("Arial", 12), command=lambda m=mode: set_mode(m))
    for m in modes:
        button = tk.Button(mode_frame, text=m, font=("Arial", 12), command=lambda m=m: set_mode(m))
        button.pack(side=tk.LEFT, padx=10, pady=10)

        # Bind the button to the scrollbar
        button.bind("<Enter>", lambda e, s=scrollbar: s.set(0, 0.5))
        button.bind("<Leave>", lambda e, s=scrollbar: s.set(0, 0))

        # Configure the scrollbar to respond to the mouse wheel
        scrollbar.bind("<Enter>", lambda e: scrollbar.bind_all("<MouseWheel>", lambda event: scrollbar.yview_scroll(int(-1*(event.delta/120)), "units")))
        scrollbar.bind("<Leave>", lambda e: scrollbar.unbind_all("<MouseWheel>"))

    # Set the initial mode
    set_mode(current_mode)

# Set up the main window
window = tk.Tk()
window.title("Voice Assistant")
window.geometry("500x500")

# Create the status text label
status_text = tk.StringVar()
status_text.set("Current mode: OpenAI")
status_label = tk.Label(window, textvariable=status_text, font=("Arial", 14))
status_label.pack(pady=20)

# Create the mode menu
current_mode = "OpenAI"
create_mode_menu()

# Create the process input button
process_button = tk.Button(window, text="Process Input", font=("Arial", 12), command=process_input)
process_button.pack(pady=20)

# Run the GUI main loop
window.mainloop()
