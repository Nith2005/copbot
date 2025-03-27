import spacy
import string
import random
import pandas as pd
from googletrans import Translator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langdetect import detect

# Load spaCy model
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("Downloading spaCy model...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load('en_core_web_sm')

# Read and process data from CSV format
try:
    df = pd.read_csv('police_faq.csv', encoding='utf-8')
    questions = df['Question Pattern'].tolist()
    responses = df['Response'].tolist()
    intents = df['Intent'].tolist()
except Exception as e:
    print(f"Error loading data: {e}")
    print("Please check if police_faq.csv exists and is properly formatted")
    exit(1)

def LemNormalize(text):
    """Normalize text by removing punctuation and lemmatizing"""
    doc = nlp(text.lower())
    return [token.lemma_ for token in doc if not token.is_punct and not token.is_space]

# Initialize translator
translator = Translator()

# Define greetings in multiple languages with their responses
GREETINGS = {
    'en': {
        'inputs': [
            'hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 
            'good evening', 'good night', 'how are you', 'what\'s up', 'whats up',
            'sup', 'greeting', 'good day', 'morning', 'afternoon', 'evening'
        ],
        'responses': [
            "Hello! I can help you with FIRs, complaints, and emergency procedures.",
            "Hi! How can I assist you today?",
            "Welcome! Ask me about police services.",
            "Hello! I'm here to help you with any police-related queries.",
            "Hi there! What would you like to know about police services?",
            "Greetings! I'm your police information assistant. How can I help you?"
        ]
    },
    'ta': {
        'inputs': [
            'வணக்கம்', 'நமஸ்காரம்', 'வணக்கம் எப்படி இருக்கிறீர்கள்',
            'காலை வணக்கம்', 'மதிய வணக்கம்', 'மாலை வணக்கம்',
            'இரவு வணக்கம்', 'நலமா', 'எப்படி இருக்கிறீர்கள்'
        ],
        'responses': [
            "வணக்கம்! FIR, புகார்கள் மற்றும் அவசர நடைமுறைகளில் நான் உங்களுக்கு உதவ முடியும்.",
            "நமஸ்காரம்! நான் எப்படி உதவ முடியும்?",
            "வணக்கம்! நான் உங்கள் காவல்துறை தகவல் உதவியாளர். உங்களுக்கு என்ன உதவ முடியும்?"
        ]
    }
}

# Define conversation termination patterns
TERMINATION_PATTERNS = {
    'en': {
        'inputs': [
            'bye', 'goodbye', 'see you', 'see you later', 'take care',
            'quit', 'exit', 'end', 'stop', 'close', 'terminate',
            'good night', 'have a good day', 'thanks', 'thank you',
            'thank you very much', 'thanks a lot'
        ],
        'responses': [
            "Thank you for using our service! Stay safe!",
            "Goodbye! Feel free to return if you need more assistance.",
            "Take care! We're here if you need us again.",
            "Thank you for chatting with us. Have a great day!",
            "Goodbye! Don't hesitate to ask if you need help in the future."
        ]
    },
    'ta': {
        'inputs': [
            'போய் வருகிறேன்', 'வணக்கம்', 'நன்றி', 'நன்றி மிகவும்',
            'போய் வருவோம்', 'போய் வருவேன்', 'விடைபெறுகிறேன்'
        ],
        'responses': [
            "நன்றி! பாதுகாப்பாக இருங்கள்!",
            "போய் வருகிறேன்! மேலும் உதவி தேவைப்பட்டால் திரும்ப வரலாம்.",
            "நன்றி! மீண்டும் உதவி தேவைப்பட்டால் கேளுங்கள்."
        ]
    }
}

def detect_language(text):
    """Detect language of input text"""
    try:
        # Add minimum text length check
        if len(text.strip()) < 4:
            return 'en'  # Default to English for very short texts
            
        # Check for English characters
        if all(ord(char) < 128 for char in text):
            return 'en'
            
        detected_lang = detect(text)
        print(f"Debug: Language detected as {detected_lang} for text: {text}")
        return detected_lang
    except:
        print("Debug: Language detection failed, defaulting to English")
        return 'en'

def get_greeting(text):
    """Return appropriate greeting based on language"""
    lang = detect_language(text)
    text_lower = text.lower()
    
    # Check if input matches any greeting in detected language
    if (lang in GREETINGS) and (text_lower in GREETINGS[lang]['inputs']):
        return random.choice(GREETINGS[lang]['responses'])
    
    # Default to English if no match found
    if text_lower in GREETINGS['en']['inputs']:
        return random.choice(GREETINGS['en']['responses'])
    
    return None

def detect_and_translate(text):
    """Detect language and translate to English if needed"""
    try:
        # Detect language
        detected_lang = detect_language(text)
        
        # Only translate if definitely not English
        if detected_lang != 'en':
            print(f"Debug: Translating from {detected_lang} to English")
            translation = translator.translate(text, src=detected_lang, dest='en')
            return translation.text, detected_lang
            
        print("Debug: Text identified as English, no translation needed")
        return text, 'en'
        
    except Exception as e:
        print(f"Translation error: {e}")
        return text, 'en'

def translate_to_original(text, target_lang):
    """Translate response back to original language"""
    try:
        if target_lang != 'en':
            translation = translator.translate(text, dest=target_lang)
            return translation.text
        return text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def get_response(user_query):
    """Process query and return response in original language"""
    try:
        # Step 1: Detect language and translate to English if needed
        english_query, original_lang = detect_and_translate(user_query)
        print(f"Debug: Query '{user_query}' detected as {original_lang}")
        print(f"Debug: Processing English query: '{english_query}'")
        
        # Step 2: Get response in English
        all_questions = questions + [english_query]
        vectorizer = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(all_questions)
        similarity = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])[0]
        
        idx = similarity.argmax()
        confidence = similarity[idx]
        
        if confidence > 0.3:
            english_response = f"{responses[idx]} (Confidence: {confidence:.2f})"
        else:
            english_response = ("I apologize, I couldn't understand your query. You can ask me anything about police services, FIRs, complaints, and emergency procedures:\n" + 
                             "\n")
        
        # Step 3: Translate response back to original language
        if original_lang != 'en':
            print(f"Translating response to {original_lang}")
            return translate_to_original(english_response, original_lang)
        return english_response
                   
    except Exception as e:
        print(f"Error in get_response: {e}")
        return "I apologize, but I'm having trouble processing that request."

def get_termination(text):
    """Return appropriate termination message based on language"""
    lang = detect_language(text)
    text_lower = text.lower()
    
    # Check if input matches any termination pattern in detected language
    if (lang in TERMINATION_PATTERNS) and (text_lower in TERMINATION_PATTERNS[lang]['inputs']):
        return random.choice(TERMINATION_PATTERNS[lang]['responses'])
    
    # Default to English if no match found
    if text_lower in TERMINATION_PATTERNS['en']['inputs']:
        return random.choice(TERMINATION_PATTERNS['en']['responses'])
    
    return None

def main():
    """Main chat loop"""
    print('🌍 Multilingual Police Information Bot')
    print('You can ask questions in any language. Type "bye" to exit.')
    
    while True:
        try:
            user_input = input('You: ').strip()
            
            # Check for termination patterns first
            termination = get_termination(user_input)
            if termination:
                print('Bot:', termination)
                break
            
            # Check for greetings
            greeting = get_greeting(user_input)
            if greeting:
                print('Bot:', greeting)
                continue
            
            # Process other queries...
            response = get_response(user_input)
            print('Bot:', response)
                    
        except Exception as e:
            print('Bot: Sorry, please try again.')

if __name__ == "__main__":
    main()