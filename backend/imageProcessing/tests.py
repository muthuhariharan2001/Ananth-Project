import re
from rapidfuzz import fuzz

def clean_tamil_address(raw_text):
    # Remove English, numbers, symbols
    cleaned = re.sub(r'[^அ-ஹ௧-௯\s]', '', raw_text)
    # Remove duplicate words
    words = cleaned.split()
    seen = set()
    result = []
    for word in words:
        if word not in seen:
            result.append(word)
            seen.add(word)
    return ' '.join(result)

# Example input
aadhar_text = """ஐதெரு கொம்பாடிதளவாய்புரம் தூத்துக்குடி தமிழ்நாடு"""
smartcard_text = """வடக்கு தெரு தளவாய்புரம் சவரிமங்களம் தூத்துக்குடி தமிழ்நாடு"""

# Clean both
aadhar_clean = clean_tamil_address(aadhar_text)
smartcard_clean = clean_tamil_address(smartcard_text)

# Fuzzy compare
match_score = fuzz.partial_ratio(aadhar_clean, smartcard_clean)
print(f"✅ Final Match Score: {match_score}%")

# Check if the match score is above a certain threshold

if match_score > 80:
    print("✅ Addresses match!")
