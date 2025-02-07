# **AI News Cartoon Generator: Convert News to New Yorker-Style Cartoons**  

## **Overview**  
This project takes **news articles** and converts them into **New Yorker-style cartoons** using OpenAI's **DALL·E 3 API**. It extracts **key concepts from the text**, generates a **cartoon with witty captions**, and serves the image through a **Flask backend** with a **React frontend**.  

🚀 **Key Highlights:**  
- **Extracts key concepts from news articles**  
- **Generates relevant cartoons with captions**  
- **Uses OpenAI’s DALL·E 3 API for image generation**  
- **Built with Flask (backend) and React (frontend)**  
- **API for real-time cartoon generation**  

---

## **🛠️ Tech Stack**  
✅ **Flask (Backend API)** – Manages requests & integrates DALL·E 3  
✅ **React (Frontend)** – Provides a user-friendly UI  
✅ **OpenAI DALL·E 3 API** – Generates the cartoon images  
✅ **Flask-CORS** – Handles cross-origin requests  
✅ **Logging & Debugging** – Integrated for better monitoring  

---

## **📁 Project Structure**  

```bash
├── news-to-cartoon-gen/
│   ├── backend/
│   │   ├── app.py                 # Flask backend API
│   │   ├── image_generator.py      # Calls OpenAI API to generate images
│   │   ├── static/                 # Stores generated images
│   ├── frontend/                   # React UI (separate repo or subfolder)
│   ├── README.md                   # Project documentation (this file)
```

---

## **🚀 Running the Application**  

### **1️⃣ Install Dependencies**  
```bash
pip install -r backend/requirements.txt
```

### **2️⃣ Set Up OpenAI API Key**  
Add your **OpenAI API key** as an environment variable:  
```bash
export OPENAI_API_KEY="your_api_key_here"
```

### **3️⃣ Start the Backend**  
```bash
cd backend
python app.py
```

### **4️⃣ Start the Frontend**  
```bash
cd frontend
npm install
npm start
```

---

## **🖼️ Generate a Cartoon via API**  

### **API Endpoint**  
```http
POST /api/generate_cartoon
```

### **Request (JSON Body)**  
```json
{
  "article_text": "Elon Musk just announced a humanoid Tesla bot that can do chores."
}
```

### **Response**  
```json
{
  "image_url": "/images/cartoon_123.png",
  "caption": "Tesla’s latest product is designed to take over the housework… until it starts negotiating its salary."
}
```

---

## **📊 Challenges & Learnings**  

✔️ **Successfully extracted key concepts from articles**  
✔️ **DALL·E image generation quality was optimized for stylized output**  
✔️ **Handled API rate limits & improved response times**  
✔️ **Frontend-react integration for seamless user experience**  

---

## **🔮 Next Steps**  
🔹 **Improve caption generation for humor accuracy**  
🔹 **Enhance text-to-image prompt engineering**  
🔹 **Deploy to a production environment (Vercel + AWS)**  

---

## **📌 Why This Project Matters?**  
This project **automates the creation of satirical cartoons** by leveraging **LLM-powered text understanding** and **AI-generated illustrations**, showcasing:  
- **Text-to-image AI applications**  
- **Humor generation using NLP & prompt tuning**  
- **Scalable AI model deployment via APIs**  

📌 **Ideal for:** AI/ML roles focusing on **LLM-powered creativity, generative AI, and API-driven AI applications.**  
