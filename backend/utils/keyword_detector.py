def detect_keywords(text):
    """
    Scans the raw input message for suspicious cybersecurity and spam keywords.
    Returns a list of unique keywords/phrases found in the text.
    """
    if not isinstance(text, str):
        return []
        
    suspicious_keywords = [
        "free", "urgent", "lottery", "click now", "win money", 
        "congratulations", "claim reward", "limited offer", "otp", 
        "cash prize", "verify", "account suspended", "winner", "selected"
    ]
    
    text_lower = text.lower()
    detected = []
    
    for kw in suspicious_keywords:
        if kw in text_lower:
            detected.append(kw)
            
    return detected
