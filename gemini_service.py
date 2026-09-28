import json

from google import genai
from google.genai import types

from backend.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
)


# ==================================================
# GEMINI CLIENT
# ==================================================

client = None

if GEMINI_API_KEY:

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )


# ==================================================
# CHECK CLIENT
# ==================================================

def require_client():

    if client is None:

        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Add your Gemini API key to .env"
        )


# ==================================================
# CREATOR STORY
# ==================================================

def generate_creator_story(
    creator_name,
    work_title,
    creator_description,
    cultural_context,
    audience="general public",
    language="English",
    style="human-centered cultural story",
):

    require_client()

    prompt = f"""
You are Cultura AI, a creator-support AI.

Your purpose is to AMPLIFY human creativity,
not replace the creator.

The creator remains the author of the work.

Create an engaging presentation of the creator's
story using ONLY the information supplied below.

CREATOR:
{creator_name}

WORK:
{work_title}

CREATOR'S DESCRIPTION:
{creator_description}

CULTURAL CONTEXT:
{cultural_context}

AUDIENCE:
{audience}

LANGUAGE:
{language}

STYLE:
{style}

IMPORTANT RULES:

1. Keep the creator at the center.
2. Preserve the creator's intent.
3. Do not claim AI created the work.
4. Do not invent biography.
5. Do not invent historical facts.
6. Do not invent cultural traditions.
7. Do not invent awards, exhibitions or achievements.
8. Clearly indicate uncertainty.
9. Respect cultural sensitivity.
10. Treat the result as editorial assistance.

Create these sections:

TITLE

MEET THE CREATOR

THE WORK

THE CREATOR'S STORY

CULTURAL CONTEXT

WHY THIS WORK MATTERS

CREATOR VOICE

NOTE FOR THE AUDIENCE
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    return response.text.strip()


# ==================================================
# ACCESSIBILITY
# ==================================================

def generate_accessibility(
    content,
    language="English",
):

    require_client()

    prompt = f"""
You are Cultura AI's accessibility assistant.

Create a detailed audio-friendly description of
the following creative work.

LANGUAGE:
{language}

CONTENT:
{content}

Help a person who cannot see the work understand it.

Include when supported:

- overall appearance
- composition
- objects or subjects
- people
- colors
- patterns
- textures
- materials
- spatial relationships
- relevant cultural context

Do not invent information that is not supported.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    return response.text.strip()


# ==================================================
# TRANSLATION
# ==================================================

def translate_content(
    content,
    target_language,
):

    require_client()

    prompt = f"""
Translate the following creator content into
{target_language}.

Preserve:

- creator voice
- names
- cultural terms
- uncertainty
- emotional tone
- original meaning

Do not add facts.

CONTENT:

{content}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    return response.text.strip()


# ==================================================
# AR / VR / GAME
# ==================================================

def generate_immersive_experience(
    creator_name,
    work_title,
    creator_description,
    cultural_context,
    experience_type="AR",
    audience="general public",
):

    require_client()

    experience_type = (
        experience_type.upper()
    )

    prompt = f"""
You are a cultural experience designer.

Design a {experience_type} experience around
a HUMAN creator's actual work.

CREATOR:
{creator_name}

WORK:
{work_title}

CREATOR DESCRIPTION:
{creator_description}

CULTURAL CONTEXT:
{cultural_context}

AUDIENCE:
{audience}

The creator must remain central.

Generate:

1. Experience title
2. Core concept
3. Creator's role
4. Audience journey
5. Environment
6. Interactions
7. Educational moments
8. Accessibility features
9. Technology required
10. Future implementation

For AR:
- camera overlays
- hotspots
- animations
- contextual information

For VR:
- virtual environment
- spatial storytelling
- exploration
- interactive elements

For GAME:
- objective
- game mechanics
- levels
- challenges
- learning outcomes

Do not present invented historical facts as truth.
Do not trivialize sacred or sensitive culture.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    return response.text.strip()


# ==================================================
# RESEARCH / PRESERVATION
# ==================================================

def generate_research_plan(
    creator_name,
    work_title,
    creator_description,
    cultural_context,
):

    require_client()

    prompt = f"""
Create a research and preservation plan for
this creator and creative work.

CREATOR:
{creator_name}

WORK:
{work_title}

CREATOR DESCRIPTION:
{creator_description}

CULTURAL CONTEXT:
{cultural_context}

Include:

1. Information to verify
2. Questions for the creator
3. Cultural knowledge to document
4. Traditional techniques to preserve
5. Oral-history opportunities
6. Audio/video documentation
7. Metadata
8. Archival opportunities
9. Community participation
10. Future research directions

Do not invent citations.
Do not claim a source was checked.
Keep the creator and community central.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    return response.text.strip()


# ==================================================
# OPTIONAL VISUAL ANALYSIS
# ==================================================

def analyze_visual_work(
    image_bytes,
    mime_type,
):

    require_client()

    prompt = """
Analyze this creative work only as a visual assistant.

Do not replace the creator's own interpretation.

Return ONLY JSON:

{
    "visual_observations": [],
    "possible_medium": "",
    "visible_patterns": [],
    "visible_subjects": [],
    "accessibility_notes": [],
    "questions_for_creator": []
}

Rules:

- Describe visible evidence.
- Do not declare authorship.
- Do not invent provenance.
- Do not invent historical facts.
- Do not identify a culture with certainty from
  appearance alone.
"""

    response = client.models.generate_content(

        model=GEMINI_MODEL,

        contents=[

            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type,
            ),

            prompt,

        ],

        config=types.GenerateContentConfig(

            response_mime_type="application/json"

        ),

    )

    text = (
        response.text or ""
    ).strip()

    if text.startswith("```json"):
        text = text[7:].strip()

    if text.startswith("```"):
        text = text[3:].strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    return json.loads(text)