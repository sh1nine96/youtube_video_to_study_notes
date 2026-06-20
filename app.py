"""
app.py
------
Main Gradio application for YouTube Video to Study Notes.

Milestone 6.3: Final tabbed layout — each output type gets its own
dedicated tab instead of one long scrolling page.
"""

import gradio as gr
from transcript import get_transcript
from study_generator import generate_all_study_material_stream


def process_video(url: str):
    """
    Full pipeline: URL -> transcript -> all 5 study outputs.
    Generator function — yields updates to all 6 outputs live.
    """

    empty = "*Waiting for processing to start...*"
    processing = "*⏳ Generating... please wait.*"

    # --- Basic input validation ---
    if not url or not url.strip():
        yield "⚠️ Please enter a YouTube URL.", empty, empty, empty, empty, empty
        return

    if "youtube.com" not in url and "youtu.be" not in url:
        yield (
            "⚠️ That doesn't look like a YouTube URL. "
            "Please paste a link like https://www.youtube.com/watch?v=...",
            empty, empty, empty, empty, empty,
        )
        return

    # Clear any previous results immediately so old content doesn't linger
    yield "🔄 Step 1/2: Fetching transcript from YouTube...", processing, processing, processing, processing, processing

    try:
        transcript, warning = get_transcript(url)
    except ValueError as e:
        error_msg = f"❌ {str(e)}"
        yield error_msg, empty, empty, empty, empty, empty
        return

    word_count = len(transcript.split())
    status_base = f"✓ Transcript fetched ({word_count} words)."
    if warning:
        status_base += f"\n\n{warning}"

    yield f"{status_base}\n\n🔄 Generating study material...", processing, processing, processing, processing, processing

    current_results = {
        "summary": processing,
        "study_notes": processing,
        "key_concepts": processing,
        "mcqs": processing,
        "interview_questions": processing,
    }

    for status_message, results in generate_all_study_material_stream(transcript):
        if results is None:
            live_status = f"{status_base}\n\n🔄 {status_message}"
            yield (
                live_status,
                current_results["summary"],
                current_results["study_notes"],
                current_results["key_concepts"],
                current_results["mcqs"],
                current_results["interview_questions"],
            )
        else:
            current_results = results
            final_status = f"{status_base}\n\n✅ All study material generated successfully!"
            yield (
                final_status,
                current_results.get("summary", "Not available"),
                current_results.get("study_notes", "Not available"),
                current_results.get("key_concepts", "Not available"),
                current_results.get("mcqs", "Not available"),
                current_results.get("interview_questions", "Not available"),
            )

# ---------------------------------------------------------------------------
# Build the UI
# ---------------------------------------------------------------------------

with gr.Blocks(title="YouTube Study Notes Generator") as demo:

    gr.Markdown("# 📚 YouTube Video to Study Notes")
    gr.Markdown("Paste a YouTube URL below and generate study material instantly.")

    with gr.Row():
        url_input = gr.Textbox(
            label="YouTube URL",
            placeholder="https://www.youtube.com/watch?v=...",
            scale=4,
        )
        generate_btn = gr.Button("Generate", variant="primary", scale=1)

    status_display = gr.Markdown("*Enter a URL and click Generate to begin.*")

    with gr.Tabs():
        with gr.Tab("📝 Summary"):
            summary_output = gr.Markdown()

        with gr.Tab("📚 Study Notes"):
            study_notes_output = gr.Markdown()

        with gr.Tab("🔑 Key Concepts"):
            key_concepts_output = gr.Markdown()

        with gr.Tab("❓ MCQs"):
            mcqs_output = gr.Markdown()

        with gr.Tab("💼 Interview Questions"):
            interview_output = gr.Markdown()

    generate_btn.click(
        fn=process_video,
        inputs=url_input,
        outputs=[
            status_display,
            summary_output,
            study_notes_output,
            key_concepts_output,
            mcqs_output,
            interview_output,
        ],
    )


if __name__ == "__main__":
    demo.launch()