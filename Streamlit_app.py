{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c8bc9f89",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st  # type: ignore\n",
    "import joblib  # type: ignore\n",
    "import re\n",
    "from nltk.corpus import stopwords\n",
    "from nltk.tokenize import word_tokenize  # type: ignore\n",
    "from nltk.stem import WordNetLemmatizer  # type: ignore\n",
    "\n",
    "# Function to set the background color\n",
    "def set_background_color(color):\n",
    "    st.markdown(\n",
    "        f\"\"\"\n",
    "        <style>\n",
    "        .stApp {{\n",
    "            background-color: {color};\n",
    "        }}\n",
    "        </style>\n",
    "        \"\"\",\n",
    "        unsafe_allow_html=True\n",
    "    )\n",
    "\n",
    "# Set the background color to green\n",
    "set_background_color('#ffdab9')\n",
    "\n",
    "\n",
    "# Custom CSS for the sidebar\n",
    "sidebar_style = \"\"\"\n",
    "    <style>\n",
    "    [data-testid=\"stSidebar\"] {\n",
    "        background-color: #e0ffff;  /* Change this color to any color code you prefer */\n",
    "    }\n",
    "    </style>\n",
    "\"\"\"\n",
    "\n",
    "# Apply the custom CSS\n",
    "st.markdown(sidebar_style, unsafe_allow_html=True)\n",
    "\n",
    "# Sidebar with navigation options\n",
    "st.sidebar.title(\"Get To Know Us!\")\n",
    "st.sidebar.write(\"[Home Page](#)\")\n",
    "st.sidebar.write(\"[About Us](#)\")\n",
    "st.sidebar.write(\"[Contact Us](#)\")\n",
    "st.sidebar.write(\"[Send Anonymous Report](#)\")\n",
    "\n",
    "\n",
    "# Header Section with Title and Image in a Text Box\n",
    "st.markdown(\n",
    "    \"\"\"\n",
    "    <div style=\"padding: 10px; border: 1px solid #ccc; border-radius: 5px; background-color: #e0ffff;\">\n",
    "        <h1 style=\"text-align: center;\">Toxic Language Detection System </h1>\n",
    "    </div>\n",
    "    \"\"\",\n",
    "    unsafe_allow_html=True\n",
    ")\n",
    "\n",
    "\n",
    "# Display an image below the header\n",
    "st.image(\"C:/Users/user/OneDrive/Desktop/toxigen/toxic.jpeg\", caption=\"Online Toxicity\", use_column_width=True)\n",
    "\n",
    "# Explanation Paragraph\n",
    "st.write(\"\"\"\n",
    "    **Online toxicity is the use of hostile, aggressive, or harmful language in online platforms.\n",
    "    This tool aims to detect such toxic language in real-time conversations or content. \n",
    "    By identifying negative sentiments, we can work towards creating a safer online environment.**\n",
    "\"\"\")\n",
    "\n",
    "# Initialize stop words and lemmatizer\n",
    "stop_words = set(stopwords.words('english'))\n",
    "lemmatizer = WordNetLemmatizer()\n",
    "\n",
    "# Load the trained model and TF-IDF vectorizer\n",
    "model = joblib.load('linear_regression_model.pkl')\n",
    "vectorizer = joblib.load('tfidf_vectorizer.pkl')\n",
    "\n",
    "# Function to preprocess the input text\n",
    "def preprocess_text(text):\n",
    "    # Basic text cleaning\n",
    "    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags\n",
    "    text = re.sub(r'\\d+', '', text)  # Remove digits\n",
    "    text = re.sub(r'[^a-zA-Z\\s]', '', text, re.I|re.A)  # Remove special characters\n",
    "    text = text.lower()  # Convert to lowercase\n",
    "    text = text.strip()  # Remove whitespaces\n",
    "    # Tokenize and lemmatize\n",
    "    tokens = word_tokenize(text)\n",
    "    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]\n",
    "    return ' '.join(tokens)\n",
    "\n",
    "# Function to predict sentiment\n",
    "def predict_sentiment(text):\n",
    "    # Preprocess the text\n",
    "    processed_text = preprocess_text(text)\n",
    "    \n",
    "    # Transform the text using the TF-IDF vectorizer\n",
    "    text_vector = vectorizer.transform([processed_text])\n",
    "    \n",
    "    # Predict using the loaded model\n",
    "    prediction = model.predict(text_vector)\n",
    "    \n",
    "    return prediction[0]\n",
    "\n",
    "# Questionnaires in Their Own Text Boxes\n",
    "st.markdown(\n",
    "    \"\"\"\n",
    "    <div style=\"padding: 10px; border: 1px solid #ccc; border-radius: 5px; background-color: #e0ffff;\">\n",
    "        <h2>Please answer the following questions:</h2>\n",
    "        <label>What do you think about the evolution of Tech and the New forms of online Interaction?</label>\n",
    "        <textarea style=\"width: 100%; height: 100px;\"></textarea>\n",
    "        <label>How do you feel when you see negative comments online?</label>\n",
    "        <textarea style=\"width: 100%; height: 100px;\"></textarea>\n",
    "        <label>What do you think can be done to reduce online toxicity?</label>\n",
    "        <textarea style=\"width: 100%; height: 100px;\"></textarea>\n",
    "    </div>\n",
    "    \"\"\",\n",
    "    unsafe_allow_html=True\n",
    ")\n",
    "\n",
    "# User input area for text analysis\n",
    "st.subheader(\"**Toxicity Level Analysis**\")\n",
    "user_input = st.text_area(\"**Input a comment you want us to analyze for toxicity:**\")\n",
    "\n",
    "# Prediction button and display of results\n",
    "# if st.button(\"Predict\"):\n",
    "#     if user_input:\n",
    "#         sentiment = predict_sentiment(user_input)\n",
    "#         sentiment_label = 'Negative' if sentiment > -1/0.33 else 'Positive' if sentiment < 1/0.33 else 'Neutral'\n",
    "#         st.write(f\"The predicted sentiment is: **{sentiment_label}**\")\n",
    "#     else:\n",
    "#         st.write(\"Please enter some text for prediction.\")\n",
    "\n",
    "# Prediction button and display of results\n",
    "       # Define the thresholds\n",
    "neg_threshold = -1/3  # -0.333...\n",
    "pos_threshold = 1/3   # 0.333...\n",
    "if st.button(\"Predict\"):\n",
    "    if user_input:\n",
    "        sentiment = predict_sentiment(user_input)\n",
    "        # Adjusted logic based on a general positive/negative threshold\n",
    "        if sentiment >= pos_threshold:\n",
    "            sentiment_label = 'Positive'\n",
    "        elif sentiment <= neg_threshold:\n",
    "            sentiment_label = 'Negative'\n",
    "        else:\n",
    "            sentiment_label = 'Neutral'\n",
    "        \n",
    "        st.write(f\"The predicted sentiment is: **{sentiment_label}**\")\n",
    "    else:\n",
    "        st.write(\"Please enter some text for prediction.\")\n",
    "\n",
    "\n",
    " "
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (learn-env)",
   "language": "python",
   "name": "learn-env"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}