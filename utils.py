import re
from urllib.parse import urlparse

def extract_features(url):
    features = []
    url = str(url).lower()
    
    # 1. URL Length
    features.append(len(url))
    
    # 2. Number of dots
    features.append(url.count('.'))
    
    # 3. Number of hyphens (Very common in phishing like 'secure-login-bank')
    features.append(url.count('-'))
    
    # 4. Presence of sensitive words
    # If the URL contains these words, it's more likely to be phishing
    sensitive_words = ['login', 'verify', 'update', 'banking', 'secure', 'account', 'billing']
    found_word = 0
    for word in sensitive_words:
        if word in url:
            found_word = 1
            break
    features.append(found_word)
    
    # 5. Number of digits (Phishing URLs often have random numbers)
    digits = re.findall(r'\d', url)
    features.append(len(digits))
    
    # 6. Is it an IP address?
    has_ip = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0
    features.append(has_ip)
    
    return features