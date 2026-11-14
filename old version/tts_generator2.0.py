import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load environment variables from your .env file
load_dotenv()

# 2. Initialize the OpenAI client securely
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_audio_from_text(text_content, output_path="podcast_output.mp3"):
    """
    Takes text content (such as your podcast script), sends it to OpenAI's TTS API,
    and saves the resulting audio output as an MP3 file.
    """
    try:
        print("🎙️ Converting text to speech via OpenAI TTS...")
        
        # Call OpenAI's audio speech endpoint
        response = client.audio.speech.create(
            model="tts-1",          # Standard fast & cost-effective TTS model (or use "tts-1-hd" for higher fidelity)
            voice="alloy",          # Voice options: 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'
            input=text_content
        )
        
        # Save the binary audio stream to a local file
        response.stream_to_file(output_path)
        print(f"✅ Audio successfully generated and saved to: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ Error generating TTS audio: {e}")
        return None

# --- Testing Block (Runs only when executing this file directly) ---
if __name__ == "__main__":
    transcript_file = "podcast_transcript.txt"
    
    if os.path.exists(transcript_file):
        print(f"Reading transcript from {transcript_file}...")
        with open(transcript_file, "r", encoding="utf-8") as f:
            script_text = f.read()
        
        # Generate the audio file from the script
        generate_audio_from_text(script_text, output_path="hong_kong_podcast.mp3")
    else:
        print(f"⚠️ Warning: '{transcript_file}' not found. Please run your LLM processor script first to generate the script!")