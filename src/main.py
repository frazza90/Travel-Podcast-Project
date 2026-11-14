import gradio as gr
import os
import json
from data_processor import load_master_dataset
from llm_processor import generate_podcast_transcript
from tts_generator import generate_multi_voice_podcast

def run_podcast_pipeline(selected_district):
    print(f"🚀 Generating podcast for district: {selected_district}")
    df_master = load_master_dataset()
    
    podcast_data = generate_podcast_transcript(df_master, selected_district=selected_district)
    if not podcast_data:
        return None, "❌ Error: Failed to generate script."
    
    json_path = "podcast_transcript.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(podcast_data, f, indent=4, ensure_ascii=False)
        
    output_mp3 = r"C:\Users\Helen\Desktop\Chris Ironhack\Week 4\Lesson 3\hong_kong_podcast.mp3"
    generated_audio_path = generate_multi_voice_podcast(json_path=json_path, output_path=output_mp3)
    
    return output_mp3, json.dumps(podcast_data, indent=2, ensure_ascii=False)

# --- Build the Gradio Web Interface ---
with gr.Blocks() as demo:
    gr.Markdown("# 🎙️ AI Podcast Studio: Hong Kong Travel Guide")
    
    with gr.Row():
        district_dropdown = gr.Dropdown(
            choices=["Central", "Tsim Sha Tsui", "Mong Kok", "Sheung Wan", "Causeway Bay"],
            value="Central",
            label="Select a Hong Kong District"
        )
        generate_btn = gr.Button("🚀 Generate Podcast", variant="primary")
        
    with gr.Row():
        audio_output = gr.Audio(label="🎧 Listen to Podcast", type="filepath")
        script_output = gr.Textbox(label="📝 Transcript", lines=14)
            
    generate_btn.click(
        fn=run_podcast_pipeline,
        inputs=[district_dropdown],
        outputs=[audio_output, script_output]
    )

if __name__ == "__main__":
    # Changed port to 7861 to bypass the port conflict
    demo.launch(theme=gr.themes.Soft(), server_name="127.0.0.1", server_port=7861)