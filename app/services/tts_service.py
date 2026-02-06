import base64
import hashlib
from typing import Dict, Optional

from google.cloud import texttospeech_v1

from app.core.config import GOOGLE_APPLICATION_CREDENTIALS, TTS_VOICE_NAME


class TTSService:
    """
    Text-to-Speech service using Google Cloud TTS.
    Converts Korean text to base64-encoded MP3 audio.
    """

    def __init__(self):
        """Initialize TTS client with optional in-memory cache"""
        self.client = texttospeech_v1.TextToSpeechClient()
        self.cache: Dict[str, str] = {}
        self.voice_name = TTS_VOICE_NAME

    async def text_to_speech(
        self,
        text: str,
        voice_name: Optional[str] = None,
        speaking_rate: float = 1.0
    ) -> str:
        """
        Convert text to base64-encoded MP3 audio.

        Args:
            text: The Korean text to convert
            voice_name: Optional voice name (default: ko-KR-Wavenet-A)
            speaking_rate: Speech speed (default: 1.0, range: 0.25-4.0)

        Returns:
            Base64-encoded MP3 audio string

        Raises:
            Exception: If TTS generation fails
        """
        voice = voice_name or self.voice_name

        # Check cache
        cache_key = self._generate_cache_key(text, voice)
        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            # Prepare TTS request
            synthesis_input = texttospeech_v1.SynthesisInput(text=text)

            voice_params = texttospeech_v1.VoiceSelectionParams(
                language_code="ko-KR",
                name=voice
            )

            audio_config = texttospeech_v1.AudioConfig(
                audio_encoding=texttospeech_v1.AudioEncoding.MP3,
                speaking_rate=speaking_rate,
                sample_rate_hertz=24000
            )

            # Generate audio
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice_params,
                audio_config=audio_config
            )

            # Convert to base64
            audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')

            # Cache the result
            self.cache[cache_key] = audio_base64

            return audio_base64

        except Exception as e:
            raise Exception(f"TTS 생성 실패: {str(e)}")

    def _generate_cache_key(self, text: str, voice: str) -> str:
        """Generate cache key from text and voice"""
        key_string = f"{text}:{voice}"
        return hashlib.md5(key_string.encode()).hexdigest()

    def clear_cache(self):
        """Clear the audio cache"""
        self.cache.clear()
