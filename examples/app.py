# /// script
# requires-python = ">=3.14,<3.15"
# dependencies = [
#     "gradio>=6.27.0,<7",
#     "kokoro-onnx>=0.6.1",
# ]
#
# [tool.uv.sources]
# kokoro-onnx = { path = "../" }
# ///

"""
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.0.onnx
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.0.bin
uv run examples/app.py
"""

import gradio as gr
import numpy as np
from numpy.typing import NDArray

from kokoro_onnx import Kokoro

SUPPORTED_LANGUAGES = ["en-us"]


def create(
    kokoro: Kokoro,
    text: str,
    voice: str,
    language: str,
    blend_voice_name: str | None = None,
):
    if not text.strip():
        raise gr.Error("Enter some text to synthesize.")
    phonemes = kokoro.tokenizer.phonemize(text, lang=language)

    style: str | NDArray[np.float32] = voice
    if blend_voice_name:
        first_voice = kokoro.get_voice_style(voice)
        second_voice = kokoro.get_voice_style(blend_voice_name)
        style = np.add(first_voice * 0.5, second_voice * 0.5)
    samples, sample_rate = kokoro.create(
        phonemes, voice=style, speed=1.0, is_phonemes=True
    )
    return [(sample_rate, samples), phonemes]


def create_app(kokoro: Kokoro) -> gr.Blocks:
    def synthesize(text: str, voice: str, language: str, blend_voice_name: str | None):
        return create(kokoro, text, voice, language, blend_voice_name)

    voices = sorted(kokoro.get_voices())
    with gr.Blocks() as ui:
        text_input = gr.TextArea(
            label="Input Text",
            rtl=False,
            value="Kokoro TTS. Turning words into emotion, one voice at a time!",
        )
        language_input = gr.Dropdown(
            label="Language",
            value="en-us",
            choices=SUPPORTED_LANGUAGES,
        )
        voice_input = gr.Dropdown(label="Voice", value="af_sky", choices=voices)
        blend_voice_input = gr.Dropdown(
            label="Blend Voice (Optional)",
            value=None,
            choices=[*voices, ("None", "")],
        )
        submit_button = gr.Button("Create")
        phonemes_output = gr.Textbox(label="Phonemes")
        audio_output = gr.Audio()
        submit_button.click(
            fn=synthesize,
            inputs=[text_input, voice_input, language_input, blend_voice_input],
            outputs=[audio_output, phonemes_output],
            api_name="create",
        )
    return ui


def main() -> None:
    kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
    ui = create_app(kokoro)
    ui.launch(
        debug=True,
        theme=gr.themes.Soft(
            primary_hue="violet",
            secondary_hue="cyan",
            neutral_hue="slate",
            font=["Calibri", "Candara", "Trebuchet MS", "sans-serif"],
            font_mono=["Consolas", "Liberation Mono", "monospace"],
        ).set(
            block_label_text_color="*primary_700",
            block_label_text_color_dark="*neutral_50",
            block_info_text_color="*primary_700",
            block_info_text_color_dark="*neutral_50",
        ),
    )


if __name__ == "__main__":
    main()
