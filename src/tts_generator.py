import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_multi_voice_podcast(
    json_path=r"C:\Users\Helen\Desktop\Chris Ironhack\Week 4\Lesson 3\podcast_transcript.json", 
    output_path=r"C:\Users\Helen\Desktop\Chris Ironhack\Week 4\Lesson 3\hong_kong_podcast.mp3"
):
    """
    Reads the JSON podcast script, generates separate TTS audio clips for 
    Chris (onyx) and Isabella (shimmer), and stitches them into a final podcast MP3.
    """
    if not os.path.exists(json_path):
        print(f"⚠️ Error: '{json_path}' not found. Please run your LLM processor first!")
        return None

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if isinstance(data, dict):
        dialogue_turns = data.get("dialogue", [])
    elif isinstance(data, list):
        dialogue_turns = data
    else:
        dialogue_turns = []

    if not dialogue_turns:
        print("⚠️ Error: No dialogue turns found in JSON.")
        return None

    print(f"🎙️ Generating distinct multi-voice audio for {len(dialogue_turns)} dialogue turns...")
    
    combined_audio = AudioSegment.empty()
    temp_files = []

    try:
        for i, turn in enumerate(dialogue_turns):
            speaker = turn.get("speaker", "Chris")
            voice = turn.get("voice", "onyx")
            text = turn.get("text", "")
            
            print(f"[{i+1}/{len(dialogue_turns)}] Generating audio for {speaker} (Voice: {voice})...")
            
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            
            temp_filename = f"temp_chunk_{i}.mp3"
            response.stream_to_file(temp_filename)
            temp_files.append(temp_filename)
            
            segment = AudioSegment.from_mp3(temp_filename)
            combined_audio += segment
            
            # Add a natural 400ms conversational pause between speakers
            pause = AudioSegment.silent(duration=400)
            combined_audio += pause

        combined_audio.export(output_path, format="mp3")
        print(f"\n🎉 Success! Distinct host podcast saved to: {output_path}")

    except Exception as e:
        print(f"❌ Error during multi-voice audio stitching: {e}")
        output_path = None

    finally:
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    return output_path

if __name__ == "__main__":
    generate_multi_voice_podcast()