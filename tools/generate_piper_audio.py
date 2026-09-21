#!/usr/bin/env python3
"""Generate the static English pronunciation files used by Verb Room."""

from __future__ import annotations

import argparse
import re
import subprocess
import tempfile
import unicodedata
import wave
from pathlib import Path

import numpy as np
from piper import PiperVoice, SynthesisConfig


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
DEFAULT_OUTPUT = ROOT / "audio" / "tts"
LEADING_AUDIO_FILTER = (
    "silenceremove=start_periods=1:start_duration=0.05:start_threshold=0.01"
)

# A few consonant/vowel contrasts are too easy to lose in isolated words.
# These explicit phonemes keep the learner-facing forms distinguishable while
# retaining the same Aru speaker as the rest of the vocabulary.
PHONEME_OVERRIDES = {
    "build": ["b", "ˈ", "ɪ", "l", "d", "d", "."],
    "ran": ["ɹ", "ˈ", "æ", "ˑ", "n", "."],
    "stand": ["s", "t", "ʰ", "ˈ", "æ", "n", "d", "."],
    "stick": ["s", "t", "t", "ˈ", "ɪ", "k", "."],
    "stuck": ["s", "t", "t", "ˈ", "ʌ", "k", "."],
}


def audio_slug(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text.lower())
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    return normalized.strip("-")


def read_verbs() -> list[tuple[str, str]]:
    source = INDEX.read_text(encoding="utf-8")
    return re.findall(r"\{ infinitive: '([^']*)', simplePast: '([^']*)'", source)


def split_forms(text: str) -> list[str]:
    return [part.strip() for part in text.split(",") if part.strip()]


def speech_text(text: str, form: str) -> str:
    # The displayed form remains "read", but only the past-tense audio needs
    # the homophone "red" so the two forms are distinguishable.
    return "red" if form == "past" and text == "read" else text


def synthesis_text(text: str) -> str:
    # A sentence-final mark makes isolated words clearer, especially for final
    # consonants such as the /t/ in "went".
    return text if text.endswith((".", "!", "?")) else f"{text}."


def requested_audio(verbs: list[tuple[str, str]]) -> list[str]:
    texts: list[str] = []
    seen: set[str] = set()
    for infinitive, simple_past in verbs:
        for form, form_name in ((infinitive, "infinitive"), (simple_past, "past")):
            for part in split_forms(form):
                text = synthesis_text(speech_text(part, form_name))
                if text not in seen:
                    seen.add(text)
                    texts.append(text)
    return texts


def override_for(text: str) -> list[str] | None:
    key = re.sub(r"[.!?]+$", "", text).strip().lower()
    return PHONEME_OVERRIDES.get(key)


def write_wav(voice: PiperVoice, text: str, speaker: int, path: Path) -> None:
    config = SynthesisConfig(speaker_id=speaker)
    override = override_for(text)
    with wave.open(str(path), "wb") as wav_file:
        if override:
            audio = voice.phoneme_ids_to_audio(voice.phonemes_to_ids(override), config)
            peak = max(float(np.max(np.abs(audio))), 1e-8)
            audio = np.clip(audio / peak, -1.0, 1.0)
            wav_file.setframerate(voice.config.sample_rate)
            wav_file.setsampwidth(2)
            wav_file.setnchannels(1)
            wav_file.writeframes((audio * 32767).astype(np.int16).tobytes())
            return

        params_set = False
        for chunk in voice.synthesize(text, config):
            if not params_set:
                wav_file.setframerate(chunk.sample_rate)
                wav_file.setsampwidth(chunk.sample_width)
                wav_file.setnchannels(chunk.sample_channels)
                params_set = True
            wav_file.writeframes(chunk.audio_int16_bytes)


def generate_one(voice: PiperVoice, text: str, output_dir: Path, speaker: int) -> Path:
    output_path = output_dir / f"{audio_slug(text)}.mp3"
    if output_path.exists():
        return output_path

    with tempfile.NamedTemporaryFile(suffix=".wav") as wav_file:
        write_wav(voice, text, speaker, Path(wav_file.name))
        subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-i",
                wav_file.name,
                "-af",
                LEADING_AUDIO_FILTER,
                "-codec:a",
                "libmp3lame",
                "-q:a",
                "4",
                str(output_path),
            ],
            check=True,
        )
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--speaker", type=int, default=3)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    verbs = read_verbs()
    if not verbs:
        raise SystemExit("Keine Vokabeln in index.html gefunden.")

    texts = requested_audio(verbs)
    voice = PiperVoice.load(str(args.model))
    generated = 0
    for text in texts:
        path = args.output / f"{audio_slug(text)}.mp3"
        if args.force and path.exists():
            path.unlink()
        generate_one(voice, text, args.output, args.speaker)
        generated += 1
        print(f"[{generated:03d}/{len(texts):03d}] {text} -> {path.relative_to(ROOT)}", flush=True)

    print(f"Fertig: {len(texts)} Audiodateien in {args.output}")


if __name__ == "__main__":
    main()
