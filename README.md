# AI Podcast Studio: Hong Kong Travel Guide

This is a group project looking at generating an automated podcast, giving a travel overview of Hong Kong. It was necessary to have data input from multiple sources, integrate an LLM api to transform the raw data in a transcript, which then is converted to audio in podcast style, and finally presented in a webpage using gradio. 

---

# Key Features

* **Multi-Source PDF Ingestion**: Extracts and cleans text page-by-page from multiple reference documents and normalizes them into a master Pandas DataFrame[cite: 6].
* **LLM Scriptwriting**: Transforms dense travel corpus into an engaging, natural 2-person back-and-forth dialogue script outputted in strict JSON format.
* **Multi-Speaker TTS**: Leverages OpenAI's Text-to-Speech API to assign unique voices—**Chris (`onyx` / Male)** and **Isabella (`shimmer` / Female)**—and stitches audio turns together seamlessly using `pydub` and FFmpeg.
* **Interactive Web UI**: Built with Gradio to provide a clean dashboard where users can trigger the pipeline, view the generated JSON transcript, and play or download the final MP3.

---

## 🗂️ Project Architecture

```text
Week 4 Lesson 3/
│
├── src/
│   ├── data_processor.py     # Ingests, cleans, and standardizes local PDFs into df_master[cite: 6]
│   ├── llm_processor.py      # Prompts OpenAI to generate the JSON conversation script
│   ├── tts_generator.py      # Handles chunked voice generation and audio stitching via FFmpeg
│   └── main.py               # Gradio web application interface[cite: 7]
│
├── podcast_transcript.json   # Generated structured dialogue output
├── hong_kong_podcast.mp3     # Final synthesized multi-speaker audio output
└── requirements.txt          # Python package dependencies