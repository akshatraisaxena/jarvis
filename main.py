import speech_recognition as sr
import pyttsx3
import webbrowser
import openai
import datetime
import os

openai.api_key = "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"

# Initialize the text-to-speech engine FOR ACTIVATING COMPUTER VOICE
engine = pyttsx3.init()

def say(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source) 
        # r.pause_threshold = 1
        audio = r.listen(source)
        try:
             print("recognizing...")
             query = r.recognize_google(audio, language = "en-in")
             print(f"User said: {query}\n")
             return query.lower()
        except sr.UnknownValueError:
            say("Sorry, I didn't understand.")
            return None
        except sr.RequestError:
            say("Could not connect to Google API.")
            return None
        except Exception as e:
            say(f" Error: {e}")
            return None

def open_website(query):
    """Dynamically open websites based on voice command"""
    website_dict = {
        "youtube": "https://www.youtube.com",
        "spotify": "https://www.spotify.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "twitter": "https://www.twitter.com",
        "linkedin": "https://www.linkedin.com",
        "github": "https://www.github.com",
        "google": "https://www.google.com"
    }
    for site in website_dict.keys():
        if site in query:
            say(f"Opening {site}")
            webbrowser.open(website_dict[site])
            return

    # If site not found, search on Google
    say("searching on Google")
    webbrowser.open(f"https://www.google.com/search?q={query}")

chatStr = ""
def generate_text(prompt):
    """Generates text using OpenAI"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if available
            messages=[{"role": "user", "content": prompt}],
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"
def chat(query):
    """Maintains conversation history and responds naturally"""
    global chatStr
    chatStr += f"User: {query}\nJarvis: "
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use gpt-4 if available
            messages=[
                {"role": "user", "content": query}
            ]
        )
        reply = response["choices"][0]["message"]["content"].strip()

        if reply:  # Ensure reply is not empty
            say(reply)
            print(f"Jarvis: {reply}\n")  # Print response to console
            return reply
        else:
            say("I am not sure how to respond.")
            return "I am not sure how to respond."

    
    except Exception as e:
            # Print the error to console and also say the error out loud
        print(f"Error: {e}")
        say(f"Sorry, I encountered an error: {e}")
        return f"Error: {e}"


if __name__ == "__main__":
    say("Hello, I am Jarvis AI. How can I assist you?")
    while True:
        command = take_command()
        if command:
            if "exit" in command or "stop" in command:
                say("Goodbye! Have a great day.")
                break  # Stop the loop
            if "open" in command:
                open_website(command.replace("open", "").strip())  # Extract website name

            if "time" in command:
                strfTime = datetime.datetime.now().strftime("%I:%M %p")
                say(f"The current time is {strfTime}")
            if "date" in command:
               strfDate = datetime.datetime.now().strftime("%A, %B %d, %Y")
               say(f"Today is {strfDate}")
            if "camera" in command:
                os.system("start microsoft.windows.camera:")
                say("opening the camera now")
            if "whatsapp" in command:
                os.system("start")
                say("opening the whatsapp now")
            if "great work" in command or "well done" in command or "good job" in command:
                say("Thank you for that!")
            
            if "write an email" in command:
                say("What should the email be about?")
                details = take_command()
                email_content = generate_text(f"Write a professional email about {details}")
                say("Here is your email:")
                print("\n--- Generated Email ---\n")
                print(email_content)

            elif "write a letter" in command:
              say("What should the letter be about?")
              details = take_command()
              letter_content = generate_text(f"Write a formal letter about {details}")
              say("Here is your letter:")
              print("\n--- Generated Letter ---\n")
              print(letter_content)

            elif "quote of the day" in command:
              quote = generate_text("Give me an inspirational quote of the day.")
              say("Here is your quote:")
              print("\n--- Quote of the Day ---\n")
              print(quote)
            else:
                response = chat(command)  # Use chat function for natural response
                say(response)

            
     

