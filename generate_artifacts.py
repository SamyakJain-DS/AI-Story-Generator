from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from google.api_core.exceptions import ResourceExhausted
from elevenlabs.core.api_error import ApiError
from typing import Optional, List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import base64
import os

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
    Uses Gemini to evaluate whether the prompt
    is suitable for story generation.
    """

    if not user_prompt or not user_prompt.strip():
        return False, "Empty prompt"

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY")
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
    Generates a story using Gemini Vision based on uploaded images,
    selected genre, and optional user prompt.
    """

    if not images:
        return False, "Story Generation Failed. Please Attach Images."
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.8,
        google_api_key=os.getenv("GOOGLE_API_KEY")
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
    
eleven_client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

def generate_audio(story_text: str) -> bytes:
    """
    Generate high-quality narrated audio using ElevenLabs.
    """

    try:
        audio = eleven_client.text_to_speech.convert(
            voice_id="cgSgspJ2msm6clMCkdW9",
            model_id="eleven_v3",
            text=story_text
        )
        audio_bytes = b"".join(audio)
        return True, audio_bytes
    
    except ApiError as e:
        if e.status_code == 429:
            return False, "Audio Generation Failed: Rate Limit Exceeded, Please Try Again Later."
        else:
            return False, f"Audio Generation Failed: API Error {e.status_code}"
    except Exception as e:
        return False, f"Audio Generation Failed: {str(e)}"