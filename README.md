# 🎨 AI Story Generator

An end-to-end **multimodal GenAI application** that generates **creative stories and narrated audio** from user-uploaded images using **Groq-hosted multimodal LLMs** and a **fully offline neural TTS pipeline**, deployed via **Streamlit**. <br>
[Live website link for you to try](https://ai-story-generator-samyak.streamlit.app/)

---

## ✨ Features

* 🖼️ **Image-driven storytelling** using Groq-hosted multimodal vision-language models
* ✍️ **Optional user prompt** with automatic relevance evaluation
* 🎭 **Genre selection** (Fantasy, Sci-Fi, Mystery, Horror, etc.)
* 📏 **Word limit control**
* 🔊 **High-quality narrated audio** using Kokoro ONNX (fully offline)
* ⚡ **Streamlit-based interactive UI**
* ☁️ **Streamlit Cloud deployable (CPU-only)**

---

## 🧠 How It Works

1. User uploads **1–5 images**
2. Optional prompt is **evaluated for story relevance** using a Groq-hosted LLM
3. A story is generated using a **Groq multimodal vision-language model** based on:

   * Uploaded images
   * Selected genre
   * Word limit
   * Optional user context

4. The generated story is converted into **natural-sounding narrated audio** using a **local neural TTS model**
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

* **Groq-hosted Multimodal LLMs**

  * Prompt relevance evaluation using GPT-OSS-120B
  * Multimodal story generation using LLaMA 4 Scout (Vision-Language Model)
  * Free-tier friendly, high-throughput inference

### 🔊 Text-to-Speech (Offline)

* **Kokoro ONNX**

  * Local neural text-to-speech engine
  * No API keys required
  * Fully offline audio generation
  * ONNX-optimized for CPU inference
  * WAV audio output

> The model and voice files are automatically downloaded from official GitHub releases on first run.

### 🖥️ Frontend

* **Streamlit**
* Session state–driven UI
* Auto-refresh control to prevent unintended reruns
* Graceful error handling for AI rate limits

---

Website Demo:

<img width="864" height="691" alt="image" src="https://github.com/user-attachments/assets/01df0ead-8d6f-480e-b802-0f83756ed5b4" />


https://github.com/user-attachments/assets/dfda6bea-f40c-466d-85e7-7a4dcbe50b3b

---

## ⚠️ Notes & Limitations

* Multimodal requests are limited to 5 images per generation
* At least **one image is required** to generate a story
* Initial run may take longer due to model file downloads

---

## 👤 Author

**Samyak Jain**
📊 Data Science | 🤖 Generative AI | 📈 Applied Machine Learning
GitHub: [https://github.com/SamyakJain-DS](https://github.com/SamyakJain-DS)

---
