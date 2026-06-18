import time
from llm import run_prompt
from prompts import (
    build_summary_prompt,
    build_study_notes_prompt,
    build_key_concepts_prompt,
    build_mcq_prompt,
    build_interview_questions_prompt,
)    


def generate_all_study_material_stream(transcript: str):
    """
    Generator version of generate_all_study_material().

    Instead of returning once at the end, this yields after EVERY step:
      - A status update string while processing
      - The final results dict once everything is done

    This allows the Gradio UI to show live progress in real time.

    Args:
        transcript: The cleaned transcript text.

    Yields:
        Tuples of (status_message: str, results_so_far: dict or None)
        The final yield will have results_so_far fully populated.
    """

    results = {}

    tasks = [
        ("summary", "📝 Generating Summary", build_summary_prompt),
        ("study_notes", "📚 Generating Study Notes", build_study_notes_prompt),
        ("key_concepts", "🔑 Extracting Key Concepts", build_key_concepts_prompt),
        ("mcqs", "❓ Creating MCQs", build_mcq_prompt),
        ("interview_questions", "💼 Creating Interview Questions", build_interview_questions_prompt),
    ]

    total_tasks = len(tasks)

    for index, (key, label, prompt_builder) in enumerate(tasks, start=1):
        status_message = f"{label}... ({index}/{total_tasks})"

        # Yield status BEFORE running, so UI updates immediately
        yield status_message, None

        try:
            prompt = prompt_builder(transcript)
            output = run_prompt(prompt)
            results[key] = output
        except Exception as e:
            results[key] = f"⚠️ Failed to generate this section: {str(e)}"

    # Final yield: everything is done, send back the full results dict
    yield "✅ All done!", results


# """
# study_generator.py
# -------------------
# Orchestrates the full study-material generation pipeline.

# Takes a transcript and runs it through all 5 prompt templates,
# collecting results into a single dictionary.

# This is the ONLY function app.py needs to call:
#     generate_all_study_material(transcript) -> dict
# """

# import time
# from llm import run_prompt
# from prompts import (
#     build_summary_prompt,
#     build_study_notes_prompt,
#     build_key_concepts_prompt,
#     build_mcq_prompt,
#     build_interview_questions_prompt,
# )


# def generate_all_study_material(transcript: str, progress_callback=None) -> dict:
#     """
#     Run the transcript through all 5 prompt templates and collect results.

#     Args:
#         transcript: The cleaned transcript text.
#         progress_callback: Optional function called with status updates,
#                             e.g. progress_callback("Generating summary...")
#                             Used later to update the Gradio UI live.

#     Returns:
#         A dictionary with keys:
#             'summary', 'study_notes', 'key_concepts', 'mcqs', 'interview_questions'
#         Each value is the generated text, or an error message if that
#         specific step failed (other steps still continue).
#     """

#     results = {}

#     # Define each task as (key_name, label, prompt_builder_function)
#     tasks = [
#         ("summary", "Generating Summary", build_summary_prompt),
#         ("study_notes", "Generating Study Notes", build_study_notes_prompt),
#         ("key_concepts", "Extracting Key Concepts", build_key_concepts_prompt),
#         ("mcqs", "Creating MCQs", build_mcq_prompt),
#         ("interview_questions", "Creating Interview Questions", build_interview_questions_prompt),
#     ]

#     total_tasks = len(tasks)

#     for index, (key, label, prompt_builder) in enumerate(tasks, start=1):
#         status_message = f"[{index}/{total_tasks}] {label}..."
#         print(f"\n{status_message}")

#         # Notify UI of progress, if a callback was provided
#         if progress_callback:
#             progress_callback(status_message)

#         start_time = time.time()

#         try:
#             prompt = prompt_builder(transcript)
#             output = run_prompt(prompt)
#             results[key] = output

#             elapsed = time.time() - start_time
#             print(f"  ✓ {label} done in {elapsed:.1f}s")

#         except Exception as e:
#             # If one task fails, don't kill the whole pipeline —
#             # record the error and continue with the remaining tasks.
#             error_message = f"⚠️ Failed to generate this section: {str(e)}"
#             results[key] = error_message
#             print(f"  ✗ {label} failed: {e}")

#     return results


def format_results_as_markdown(results: dict) -> str:
    """
    Combine all 5 results into one big markdown document.
    Useful for exporting/saving the full study pack as a single file.

    Args:
        results: The dictionary returned by generate_all_study_material().

    Returns:
        A single markdown-formatted string containing everything.
    """

    sections = [
        ("📝 Summary", results.get("summary", "")),
        ("📚 Study Notes", results.get("study_notes", "")),
        ("🔑 Key Concepts", results.get("key_concepts", "")),
        ("❓ Multiple Choice Questions", results.get("mcqs", "")),
        ("💼 Interview Questions", results.get("interview_questions", "")),
    ]

    markdown_parts = []
    for title, content in sections:
        markdown_parts.append(f"# {title}\n\n{content}\n")

    return "\n---\n\n".join(markdown_parts)