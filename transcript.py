"""
transcript.py
-------------
Handles everything related to YouTube transcript extraction.

Responsibilities:
  1. Parse a YouTube URL (any common format)
  2. Extract the 11-character video ID
  3. Fetch the transcript using youtube-transcript-api
  4. Clean and join the transcript into a single readable string
  5. Handle errors gracefully with clear messages
"""

import re
from urllib.parse import urlparse, parse_qs
# NEW — replace with this:
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
# from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound


# ---------------------------------------------------------------------------
# STEP 1: Extract Video ID from URL
# ---------------------------------------------------------------------------

def extract_video_id(url: str) -> str:
    """
    Extract the 11-character YouTube video ID from any common URL format.

    Supported formats:
      - https://www.youtube.com/watch?v=VIDEO_ID
      - https://youtu.be/VIDEO_ID
      - https://www.youtube.com/embed/VIDEO_ID
      - https://m.youtube.com/watch?v=VIDEO_ID
      - https://www.youtube.com/watch?v=VIDEO_ID&t=30s

    Args:
        url: A YouTube URL string entered by the user.

    Returns:
        The 11-character video ID string.

    Raises:
        ValueError: If no valid video ID can be found in the URL.
    """

    if not url or not url.strip():
        raise ValueError("URL cannot be empty. Please enter a YouTube URL.")

    url = url.strip()

    # Pattern 1: youtu.be/VIDEO_ID  (short share links)
    short_link_pattern = r"youtu\.be/([a-zA-Z0-9_-]{11})"
    match = re.search(short_link_pattern, url)
    if match:
        return match.group(1)

    # Pattern 2: youtube.com/watch?v=VIDEO_ID  (standard links)
    parsed = urlparse(url)
    if "youtube.com" in parsed.netloc:
        query_params = parse_qs(parsed.query)
        if "v" in query_params:
            video_id = query_params["v"][0]
            if len(video_id) == 11:
                return video_id

    # Pattern 3: youtube.com/embed/VIDEO_ID  (embedded links)
    embed_pattern = r"youtube\.com/embed/([a-zA-Z0-9_-]{11})"
    match = re.search(embed_pattern, url)
    if match:
        return match.group(1)

    # If none of the patterns matched, raise a clear error
    raise ValueError(
        f"Could not extract a video ID from: {url}\n"
        "Please use a standard YouTube URL like:\n"
        "  https://www.youtube.com/watch?v=VIDEO_ID\n"
        "  https://youtu.be/VIDEO_ID"
    )


# ---------------------------------------------------------------------------
# STEP 2: Fetch the Transcript
# ---------------------------------------------------------------------------

def fetch_transcript(video_id: str) -> list[dict]:
    """
    Fetch the raw transcript for a YouTube video using its video ID.

    Compatible with youtube-transcript-api v0.6+ (new API style).

    Args:
        video_id: The 11-character YouTube video ID.

    Returns:
        A list of transcript segment dictionaries.

    Raises:
        ValueError: With a user-friendly message if transcript is unavailable.
    """

    try:
        # New API style (v0.6+): instantiate the class, then call fetch()
        ytt_api = YouTubeTranscriptApi()

        # Try fetching English transcript first
        fetched = ytt_api.fetch(video_id, languages=["en", "en-US", "en-GB"])

        # Convert FetchedTranscript object to a plain list of dicts
        segments = [
            {"text": snippet.text, "start": snippet.start, "duration": snippet.duration}
            for snippet in fetched
        ]
        return segments

    except TranscriptsDisabled:
        raise ValueError(
            "This video has transcripts disabled by the creator. "
            "Please try a different video."
        )

    except NoTranscriptFound:
        # Fallback: try any available language
        try:
            ytt_api = YouTubeTranscriptApi()
            transcript_list = ytt_api.list(video_id)

            # Get the first available transcript
            for transcript_obj in transcript_list:
                fetched = transcript_obj.fetch()
                segments = [
                    {"text": snippet.text, "start": snippet.start, "duration": snippet.duration}
                    for snippet in fetched
                ]
                return segments

        except Exception:
            raise ValueError(
                "No transcript found for this video. "
                "The video may not have captions. Please try a different video."
            )
        
    except VideoUnavailable:
        raise ValueError(
            "This video is unavailable. It may be private, deleted, or "
            "restricted in your region. Please try a different video."
        )    

    except Exception as e:
        raise ValueError(f"Failed to fetch transcript: {str(e)}")

# ---------------------------------------------------------------------------
# STEP 3: Clean and Join Transcript Segments into One String
# ---------------------------------------------------------------------------

def clean_transcript(transcript_segments: list[dict]) -> str:
    """
    Convert the raw list of transcript segments into one clean text string.

    Raw transcript segments look like:
      [{'text': '[Music]', 'start': 0.0, 'duration': 2.0},
       {'text': 'hello everyone', 'start': 2.0, 'duration': 1.5}, ...]

    We:
      1. Extract only the 'text' from each segment
      2. Remove common noise like [Music], [Applause], [Laughter]
      3. Strip extra whitespace
      4. Join everything into one readable paragraph

    Args:
        transcript_segments: Raw list of dicts from fetch_transcript().

    Returns:
        A single cleaned string of the full transcript.
    """

    # Noise patterns to remove — these are auto-generated captions artifacts
    noise_patterns = [
        r"\[.*?\]",   # removes [Music], [Applause], [Laughter], etc.
        r"\(.*?\)",   # removes (music), (laughing), etc.
    ]

    cleaned_segments = []

    for segment in transcript_segments:
        text = segment.get("text", "")

        # Remove noise patterns
        for pattern in noise_patterns:
            text = re.sub(pattern, "", text)

        # Clean up extra spaces and strip leading/trailing whitespace
        text = " ".join(text.split())

        # Only add non-empty segments
        if text.strip():
            cleaned_segments.append(text.strip())

    # Join all segments into one paragraph with spaces
    full_transcript = " ".join(cleaned_segments)

    return full_transcript


# ---------------------------------------------------------------------------
# STEP 4: Main Entry Point — One Function to Call from Other Modules
# ---------------------------------------------------------------------------

def get_transcript(url: str) -> tuple[str, str]:
    """
    Master function: takes a YouTube URL and returns the full clean transcript
    plus a warning message (empty string if no warning needed).

    Returns:
        A tuple of (transcript_text, warning_message).
        warning_message is "" if there's nothing to warn about.

    Raises:
        ValueError: With a descriptive, user-friendly message if anything fails.
    """
    video_id = extract_video_id(url)
    print(f"[transcript] Video ID extracted: {video_id}")

    raw_segments = fetch_transcript(video_id)
    print(f"[transcript] Fetched {len(raw_segments)} transcript segments")

    transcript_text = clean_transcript(raw_segments)
    word_count = len(transcript_text.split())
    print(f"[transcript] Transcript cleaned. Word count: {word_count}")

    if word_count < 30:
        raise ValueError(
            "This video's transcript is too short or empty to generate "
            "meaningful study material. Please try a different video."
        )

    warning = ""
    if word_count > 3000:
        estimated_minutes = word_count // 150  # rough speech rate estimate
        warning = (
            f"⚠️ This video is long (~{word_count} words, ~{estimated_minutes} min of speech). "
            f"Only the first ~3000 words will be used to generate study material, "
            f"so later parts of the video may not be covered."
        )
        print(f"[transcript] {warning}")

    return transcript_text, warning