import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from data_processor import load_master_dataset

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_podcast_transcript(df, selected_district="Central"):
    """
    Synthesizes data from df_master and prompts the LLM to return a 
    strict JSON-formatted 2-person podcast script focusing on a selected district.
    """
    print(f"Synthesizing content for district: {selected_district}...")
    
    sample_texts = []
    for source_name in df["source"].unique():
        source_rows = df[df["source"] == source_name].head(4) 
        source_blob = f"\n--- Source: {source_name} ---\n" + "\n".join(source_rows["raw_text"].tolist())
        sample_texts.append(source_blob)
    
    combined_corpus = "\n".join(sample_texts)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are an expert podcast producer and scriptwriter. "
                        f"Transform the provided Hong Kong travel guide text into an engaging, conversational 2-person podcast script focusing specifically on the district: {selected_district}. "
                        "Return a JSON object with a single key 'dialogue' containing a list of objects. "
                        "Each object must have: 'speaker' ('Chris' or 'Isabella'), 'voice' ('onyx' for Chris, 'shimmer' for Isabella), "
                        "and 'text' (the spoken dialogue line). Chris is the male host and Isabella is the female host. "
                        "Include an enthusiastic intro welcoming listeners, natural back-and-forth banter, a breakdown of the district, and a smooth outro."
                    )
                },
                {
                    "role": "user", 
                    "content": f"Here is the multi-source travel data:\n\n{combined_corpus}"
                }
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        json_content = json.loads(response.choices[0].message.content)
        return json_content
    
    except Exception as e:
        print(f"❌ Error generating JSON podcast script: {e}")
        return None

if __name__ == "__main__":
    df_master = load_master_dataset()
    podcast_data = generate_podcast_transcript(df_master)
    
    if podcast_data:
        with open("podcast_transcript.json", "w", encoding="utf-8") as f:
            json.dump(podcast_data, f, indent=4, ensure_ascii=False)
        print("\n✅ Success! Updated JSON transcript saved to 'podcast_transcript.json'.")