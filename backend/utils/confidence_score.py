def calculate_confidence(probabilities):
    """
    Converts model probability distributions to a high-fidelity confidence percentage.
    Takes a list or array of class probabilities and returns max(proba) * 100 rounded to 1 decimal.
    """
    if not probabilities or len(probabilities) == 0:
        return 0.0
    return round(max(probabilities) * 100, 1)

def determine_risk_level(prediction, spam_probability):
    """
    Calculates the threat risk level.
    High (>85% Spam Probability), Medium (60-85% Spam Probability), Low (<60% Spam Probability).
    If the prediction is Safe (Ham), the risk is Low by default since spam probability is low.
    """
    if prediction == "Safe" or prediction == "ham":
        return "Low"
        
    spam_pct = spam_probability * 100
    if spam_pct > 85.0:
        return "High"
    elif spam_pct >= 60.0:
        return "Medium"
    else:
        return "Low"
