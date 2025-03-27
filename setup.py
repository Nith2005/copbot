import subprocess
import sys

def setup_environment():
    """Setup required packages and models"""
    try:
        print("Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("\nDownloading NLTK data...")
        import nltk
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        
        print("\nInstalling spaCy model...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        
        # Verify installation
        import spacy
        nlp = spacy.load('en_core_web_sm')
        print("\nSetup completed successfully!")
        
    except Exception as e:
        print(f"Error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_environment()