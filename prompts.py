"""
prompts.py
----------
All prompt templates for the YouTube Study Notes application.

Each function takes the transcript text as input and returns
a fully-formed prompt string ready to send to the LLM.

Why separate templates per task?
  - Summary needs a different tone than MCQs
  - Interview questions need a different format than key concepts
  - Keeping them separate makes each easy to tune independently

One function per output type:
  1. build_summary_prompt()
  2. build_study_notes_prompt()
  3. build_key_concepts_prompt()
  4. build_mcq_prompt()
  5. build_interview_questions_prompt()
"""


# ---------------------------------------------------------------------------
# SHARED HELPER — truncate very long transcripts
# ---------------------------------------------------------------------------

MAX_TRANSCRIPT_WORDS = 3000  # Safety limit to avoid overloading the model

def _prepare_transcript(transcript: str) -> str:
    """
    Truncate the transcript to MAX_TRANSCRIPT_WORDS if it exceeds the limit.

    Why: LLMs have a context window limit. Very long transcripts (1hr+ videos)
    can exceed this. We take the first 3000 words which covers ~20-30 minutes
    of content — enough for high-quality study material.

    Args:
        transcript: The full cleaned transcript string.

    Returns:
        Transcript string, truncated if necessary.
    """
    words = transcript.split()
    if len(words) > MAX_TRANSCRIPT_WORDS:
        truncated = " ".join(words[:MAX_TRANSCRIPT_WORDS])
        print(f"[prompts] Transcript truncated from {len(words)} to {MAX_TRANSCRIPT_WORDS} words")
        return truncated
    return transcript


# ---------------------------------------------------------------------------
# PROMPT 1: Summary
# ---------------------------------------------------------------------------

def build_summary_prompt(transcript: str) -> str:
    """
    Build a prompt that generates a concise summary of the video.

    Target output: 150-200 words, plain paragraph format.
    """
    transcript = _prepare_transcript(transcript)

    return f"""You are an expert educational content summarizer having 20+ years of experience in the domain.

Your task is to write a concise summary of the following video transcript.

REQUIREMENTS:
- Write exactly 3 paragraphs
- Each paragraph should be 3-4 sentences
- Use simple, clear language suitable for students
- Cover the main topic, key arguments, and conclusion
- Do NOT use bullet points
- Do NOT include headers
- Write in present tense ("The video explains...", "The speaker discusses...")

TRANSCRIPT:
{transcript}

Write the summary now:"""


# ---------------------------------------------------------------------------
# PROMPT 2: Study Notes
# ---------------------------------------------------------------------------

def build_study_notes_prompt(transcript: str) -> str:
    """
    Build a prompt that generates detailed structured study notes.

    Target output: Well-organized notes with sections and bullet points.
    """
    transcript = _prepare_transcript(transcript)

    return f"""You are an expert study notes creator for university students having 20 years of experience at Harvard, Stanford etc.

Your task is to convert the following video transcript into detailed, structured study notes.

REQUIREMENTS:
- Create clear sections with headings using ## for main headings
- Use bullet points (- ) for key points under each section
- Include important definitions, examples, and explanations
- Make notes self-contained (a student should understand them without watching the video)
- Use bold (**text**) for important terms
- Create 4-6 main sections minimum
- Each section should have 3-6 bullet points

TRANSCRIPT:
{transcript}

Write the detailed study notes now:"""


# ---------------------------------------------------------------------------
# PROMPT 3: Key Concepts
# ---------------------------------------------------------------------------

def build_key_concepts_prompt(transcript: str) -> str:
    """
    Build a prompt that extracts key concepts as a clean glossary.

    Target output: 8-12 concepts, each with a term and definition.
    """
    transcript = _prepare_transcript(transcript)

    return f"""You are an expert at identifying and explaining key concepts from educational content.

Your task is to extract the most important concepts from the following video transcript.

REQUIREMENTS:
- Identify exactly 8-12 key concepts, terms, or ideas
- For each concept, provide:
  * The concept name in bold (**Concept Name**)
  * A clear 1-2 sentence definition or explanation
  * A colon separating the name from the definition
- Order them from most fundamental to most advanced
- Focus on concepts a student would need to understand or memorize
- Do NOT number them — use bullet points (-)

Example format:
- **Neural Network**: A computational model inspired by the human brain that learns patterns from data through interconnected layers of nodes.

TRANSCRIPT:
{transcript}

Extract the key concepts now:"""


# ---------------------------------------------------------------------------
# PROMPT 4: Multiple Choice Questions (MCQs)
# ---------------------------------------------------------------------------

def build_mcq_prompt(transcript: str) -> str:
    """
    Build a prompt that generates 10 MCQs with answers.

    Target output: 10 questions, each with 4 options (A-D) and the correct answer.
    """
    transcript = _prepare_transcript(transcript)

    return f"""You are an expert exam question writer for educational assessments.

Your task is to create 10 multiple choice questions based on the following video transcript.

REQUIREMENTS:
- Create exactly 10 questions
- Each question must have exactly 4 options labeled A), B), C), D)
- Only one option should be correct
- Questions should test understanding, not just memorization
- Vary difficulty: 3 easy, 4 medium, 3 hard questions
- After all 10 questions, add a section called "ANSWER KEY:" with all answers
- Number questions 1-10

EXACT FORMAT TO FOLLOW:
1. [Question text here]
   A) [Option A]
   B) [Option B]
   C) [Option C]
   D) [Option D]

2. [Question text here]
   A) [Option A]
   ...

ANSWER KEY:
1. [Letter] - [Brief explanation]
2. [Letter] - [Brief explanation]
...

TRANSCRIPT:
{transcript}

Generate the 10 MCQs now:"""


# ---------------------------------------------------------------------------
# PROMPT 5: Interview Questions
# ---------------------------------------------------------------------------

def build_interview_questions_prompt(transcript: str) -> str:
    """
    Build a prompt that generates 5 interview-style questions with detailed answers.

    Target output: 5 questions that test deep understanding, with full answers.
    """
    transcript = _prepare_transcript(transcript)

    return f"""You are an expert technical interviewer and educator.

Your task is to create 5 interview questions with detailed answers based on the following video transcript.

REQUIREMENTS:
- Create exactly 5 questions
- Questions should be open-ended (not yes/no)
- Questions should test deep understanding and ability to explain concepts
- Each answer should be 3-5 sentences, thorough enough to impress an interviewer
- Number the questions 1-5
- Clearly separate Question from Answer

EXACT FORMAT TO FOLLOW:
**Q1: [Question text]**
Answer: [Detailed answer here, 3-5 sentences]

**Q2: [Question text]**
Answer: [Detailed answer here, 3-5 sentences]

...and so on.

TRANSCRIPT:
{transcript}

Generate the 5 interview questions with answers now:"""