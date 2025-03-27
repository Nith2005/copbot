import re

class LanguageProcessor:
    def __init__(self):
        # Core concept keywords
        self.CORE_CONCEPTS = {
            'tamil': {
                'passport': ['பாஸ்போர்ட்', 'கடவுச்சீட்டு', 'வெளிநாட்டு'],
                'police': ['காவல்', 'போலீஸ்', 'அதிகாரி'],
                'complaint': ['புகார்', 'முறையீடு', 'கோரிக்கை'],
                'emergency': ['அவசரம்', 'உடனடி', 'அபாயம்'],
                'station': ['நிலையம்', 'மையம்'],
                'help': ['உதவி', 'சேவை', 'ஆலோசனை']
            }
        }

        # Question indicators
        self.QUESTION_WORDS = {
            'tamil': ['எப்படி', 'எங்கே', 'என்ன', 'யார்', 'எப்போது', 'ஏன்']
        }

    def extract_concepts(self, text, lang):
        """Extract core concepts from text"""
        concepts = []
        if lang not in self.CORE_CONCEPTS:
            return concepts

        for concept, keywords in self.CORE_CONCEPTS[lang].items():
            if any(keyword in text.lower() for keyword in keywords):
                concepts.append(concept)
        return concepts

    def is_question(self, text, lang):
        """Check if text is a question"""
        if lang not in self.QUESTION_WORDS:
            return False
        return any(word in text.lower() for word in self.QUESTION_WORDS[lang])

    def get_response_template(self, concepts, is_question):
        """Get appropriate response template based on concepts"""
        # Logic to combine concepts into meaningful response
        return self._build_response(concepts, is_question)

    def _build_response(self, concepts, is_question):
        """Build response from templates based on concepts"""
        if not concepts:
            return None
            
        # Example template combination
        if 'passport' in concepts and 'police' in concepts:
            return 'passport_verification'
        elif 'emergency' in concepts:
            return 'emergency_contact'
        return concepts[0]  # fallback to first concept