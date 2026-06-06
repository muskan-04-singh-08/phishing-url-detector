import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from utils import extract_features

# 1. Load the big dataset
print("Loading dataset... this might take a second.")
df = pd.read_csv('../data/phishing_dataset.csv')

# 2. Extract features from every URL
print("Extracting features (teaching the computer what to look for)...")
# This line takes every URL and runs it through our 'extract_features' function
X = df['URL'].apply(lambda x: extract_features(str(x))).tolist()
y = df['label']

# 3. Split the data (80% for training, 20% for testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train the AI (The 'Random Forest' algorithm)
print("Training the model... please wait.")
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 5. Save the brain!
# We save it as a .pkl file so we can use it in our website later
with open('phishing_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Success! Your AI 'brain' is saved as backend/phishing_model.pkl")