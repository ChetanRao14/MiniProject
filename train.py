import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import joblib # Used for saving our trained model

# --- 1. Load Data ---
try:
    df = pd.read_csv('complaints.csv')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: 'complaints.csv' not found. Make sure it's in the same folder.")
    exit()

# --- 2. Define Features (X) and Labels (y) ---
X = df['complaint_text']
y_category = df['category']
y_priority = df['priority']

# --- 3. Create Training and Testing Sets (80% train, 20% test) ---
# We split our data to train the model and then test it on unseen data
X_train, X_test, y_category_train, y_category_test, y_priority_train, y_priority_test = train_test_split(
    X, y_category, y_priority, test_size=0.20, random_state=42, stratify=y_category
)

print(f"Training set size: {len(X_train)} rows")
print(f"Testing set size: {len(X_test)} rows")


# ======================================================================
# --- 4. TRAIN MODEL 1: CATEGORY CLASSIFIER ---
# ======================================================================
print("\n--- Training Category Model ---")

# Create a 'pipeline': This chains steps together.
# 1. TfidfVectorizer: Converts text into a matrix of numbers.
# 2. LinearSVC: The actual classification model.
model_category = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('clf', LinearSVC(C=1.0, random_state=42)) 
])

# Train the model
model_category.fit(X_train, y_category_train)

# --- Test the Category Model ---
y_category_pred = model_category.predict(X_test)
accuracy_cat = accuracy_score(y_category_test, y_category_pred)

print(f"Category Model Accuracy: {accuracy_cat * 100:.2f}%")

# --- Save the Category Model ---
joblib.dump(model_category, 'model_category.joblib')
print("Category Model saved as 'model_category.joblib'")


# ======================================================================
# --- 5. TRAIN MODEL 2: PRIORITY CLASSIFIER ---
# ======================================================================
print("\n--- Training Priority Model ---")

# We create a new, separate pipeline for the priority
model_priority = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('clf', LinearSVC(C=1.0, random_state=42))
])

# Train the model
model_priority.fit(X_train, y_priority_train)

# --- Test the Priority Model ---
y_priority_pred = model_priority.predict(X_test)
accuracy_pri = accuracy_score(y_priority_test, y_priority_pred)

print(f"Priority Model Accuracy: {accuracy_pri * 100:.2f}%")

# --- Save the Priority Model ---
joblib.dump(model_priority, 'model_priority.joblib')
print("Priority Model saved as 'model_priority.joblib'")

print("\nTraining complete! Both models are saved.")