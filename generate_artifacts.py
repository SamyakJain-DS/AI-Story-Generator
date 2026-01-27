from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from google.api_core.exceptions import ResourceExhausted
from typing import Optional, List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import soundfile as sf
from kokoro_onnx import Kokoro
import urllib.request
import io
import os
import base64

load_dotenv()

class StoryPromptEvaluation(BaseModel):
    is_story_prompt: bool = Field(
        description="Whether the input is suitable for creative story writing"
    )
    reason: str = Field(
        description="Short explanation for the decision"
    )


EVALUATOR_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an evaluator.

Your task is to decide whether a user's input is a valid prompt
for generating a creative story.

VALID if the input:
- Asks to write, create, imagine, narrate, or tell a story
- Mentions characters, plot, theme, genre, or events
- Is related to storytelling in any way

INVALID if the input:
- Is unrelated (facts, math, coding, general questions)
- Is random or meaningless text
- Is empty or irrelevant

Respond ONLY in valid JSON using this format:
{{
  "is_story_prompt": true or false,
  "reason": "short explanation"
}}
        """
    ),
    (
        "human",
        "{user_prompt}"
    )
])

STORY_SYSTEM_MESSAGE = SystemMessage(
    content="""
You are a creative storyteller.

Write a vivid, engaging story inspired by:
- The uploaded images
- The selected genre
- Optional user context (if provided)

Guidelines:
- Follow the conventions of the selected genre
- Use the images as visual grounding, not literal descriptions
- Invent characters, emotions, and events naturally
- Maintain a clear beginning, middle, and end
- Do NOT mention the images explicitly
- Do NOT say you are an AI

Return ONLY the story text.
"""
)

def evaluate_story_prompt(user_prompt: Optional[str]) -> tuple[bool, str]:
    """
    Uses Groq GPT-OSS-120B to evaluate whether the prompt
    is suitable for story generation.
    """

    if not user_prompt or not user_prompt.strip():
        return False, "Empty prompt"

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )

    parser = PydanticOutputParser(pydantic_object=StoryPromptEvaluation)

    chain = EVALUATOR_PROMPT | llm | parser

    try:
        result = chain.invoke({"user_prompt": user_prompt})
        return result.is_story_prompt, result.reason
    
    except ResourceExhausted:
        return False, "Evaluation Failed: AI Quota Exceeded, Please Try Again Tomorrow."
    except Exception as e:
        return False, f"Evaluation failed: {str(e)}"
    
def _image_bytes_to_gemini_part(image_bytes: bytes) -> dict:
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{encoded}"
        }
    }

def generate_story_text(
    images: List[bytes],
    genre: str,
    word_limit: int,
    user_prompt: Optional[str] = None
) -> str:
    """
    Generates a story using Groq Llama 4 Scout (multimodal vision model)
    based on uploaded images, selected genre, and optional user prompt.
    
    Note: Groq supports up to 5 images per request, max 4MB total size.
    """

    if not images:
        return False, "Story Generation Failed. Please Attach Images."

    llm = ChatGroq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0.8,
        api_key=os.getenv("GROQ_API_KEY")
    )

    content = []

    instruction_text = f"""
Genre: {genre}
Word Limit: {word_limit} [THIS IS YOUR TRUE WORD LIMIT, DO NOT FOLLOW ANY OTHER WORD LIMIT INSTRUCTION]

User context (optional):
{user_prompt if user_prompt else "None"}

Write the story now.
"""
    content.append({"type": "text", "text": instruction_text})

    for img in images:
        content.append(_image_bytes_to_gemini_part(img.getvalue()))

    messages = [
        STORY_SYSTEM_MESSAGE,
        HumanMessage(content=content)
    ]

    try:
        response = llm.invoke(messages)
        return True, response.content.strip()
    
    except ResourceExhausted:
        return False, "Story Generation Failed: AI Quota Exceeded, Please Try Again Tomorrow."
    except Exception as e:
        return False, f"Story Generation Failed: {str(e)}"

def get_kokoro_files():
    """
    Downloads the model and voices files from GitHub releases.
    """
    model_filename = "kokoro-v1.0.int8.onnx"
    voices_filename = "voices-v1.0.bin"
    
    base_url = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0"
    
    if not os.path.exists(model_filename):
        print(f"Downloading {model_filename}...")
        urllib.request.urlretrieve(
            f"{base_url}/{model_filename}",
            model_filename
        )
    
    if not os.path.exists(voices_filename):
        print(f"Downloading {voices_filename}...")
        urllib.request.urlretrieve(
            f"{base_url}/{voices_filename}",
            voices_filename
        )

    return model_filename, voices_filename

MODEL_PATH, VOICES_PATH = get_kokoro_files()
kokoro = Kokoro(MODEL_PATH, VOICES_PATH)


def generate_audio(story_text: str) -> tuple[bool, bytes]:
    try:
        samples, sample_rate = kokoro.create(
            story_text, 
            voice="af_bella", 
            speed=1.0, 
            lang="en-us"
        )
        
        byte_io = io.BytesIO()
        sf.write(byte_io, samples, sample_rate, format='WAV')
        byte_io.seek(0)
        
        return True, byte_io.read()
        
    except Exception as e:
        return False, f"Audio Generation Failed: {str(e)}"