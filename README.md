# 🎨 AI Story Generator

An end-to-end **multimodal GenAI application** that generates **creative stories and narrated audio** from user-uploaded images using **Google Gemini** and **ElevenLabs**, deployed via **Streamlit**. <br>
Live website link for you to try: [Streamlit Website](https://ai-story-generator-samyak.streamlit.app/)

---

## ✨ Features

* 🖼️ **Image-driven storytelling** using Gemini Vision
* ✍️ **Optional user prompt** with automatic relevance evaluation
* 🎭 **Genre selection** (Fantasy, Sci-Fi, Mystery, Horror, etc.)
* 📏 **Word limit control**
* 🔊 **High-quality narrated audio** using ElevenLabs
* ⚡ **Streamlit-based interactive UI**
* ☁️ **Streamlit Cloud deployable**

---

## 🧠 How It Works

1. User uploads **1–8 images**
2. Optional prompt is **evaluated for story relevance** using Gemini
3. A story is generated using **Gemini Vision** based on:

   * Uploaded images
   * Selected genre
   * Word limit
   * Optional user context
4. The generated story is converted into **natural-sounding narrated audio** using ElevenLabs
5. The app displays:

   * 📖 Story text
   * 🔊 Audio narration

---

## 🗂️ Project Structure

```text
AI_Story_Generator/
├── app.py                  # Streamlit UI
├── generate_artifacts.py   # LLM, vision, and audio logic
├── requirements.txt        # Dependencies
├── .gitignore
└── README.md
```

---

## 🖥️ User Interface

* Rotating placeholder prompts for inspiration
* Drag-and-drop image uploads
* Genre selector with **Random** option
* Adjustable word limit
* One-click story and audio generation

---

## 🧩 Tech Stack

### 🧠 LLM & Vision

* **Google Gemini 2.5 Flash**

  * Prompt evaluation
  * Multimodal story generation (text + images)

### 🔊 Text-to-Speech

* **ElevenLabs API**

  * High-quality neural voices
  * Expressive narration suitable for storytelling

### 🖥️ Frontend

* **Streamlit**
* Session state–driven UI
* Auto-refresh control to prevent unintended reruns

---

## ⚠️ Notes & Limitations

* Gemini **free tier is rate-limited**
* Multiple Gemini calls per generation can exhaust quota quickly
* Audio generation depends on available ElevenLabs voices
* At least **one image is required** to generate a story

---

## 👤 Author

**Samyak Jain**
📊 Data Science | 🤖 Generative AI | 📈 Applied Machine Learning
GitHub: [https://github.com/SamyakJain-DS](https://github.com/SamyakJain-DS)

---
