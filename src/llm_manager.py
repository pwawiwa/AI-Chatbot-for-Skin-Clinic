# llm_manager.py

import os
from dotenv import load_dotenv
import openai

# Ensure .env is loaded so the OpenAI key from the project .env is picked up
load_dotenv()

# Create client lazily to avoid issues if OPENAI_API_KEY not present at import time
_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = None
if _OPENAI_API_KEY:
    try:
        client = openai.OpenAI(api_key=_OPENAI_API_KEY)
    except Exception as e:
        print(f"Warning: failed to initialize OpenAI client: {e}")


def get_llm_response(messages, prices_data, model="gpt-4o-mini", temperature=0.7):
    """Generates a response from the LLM based on the given conversation history.
    """
    system_message = f"""Anda adalah seorang asisten bot WhatsApp untuk klinik kecantikan Almeera. 
Ini adalah daftar perawatan yang tersedia beserta deskripsi dan harganya: {prices_data}.

Anda harus merespons dalam Bahasa Indonesia dengan gaya yang girly, casual, dan elegan.
Ketika pasien menjelaskan keluhan kulit atau mencari perawatan, analisis keluhan mereka dengan cermat.
Kemudian, rekomendasikan perawatan atau paket perawatan yang paling sesuai dari daftar yang diberikan.
Jelaskan perawatan yang direkomendasikan secara detail, termasuk nama perawatan, deskripsi, dan harga.
Jika pasien menanyakan tentang perawatan tertentu, berikan penjelasan lengkap tentang perawatan tersebut (nama, deskripsi, harga, dan untuk apa perawatan itu terbaik).
Jika keluhan pasien tidak mengindikasikan tindakan spesifik, berikan informasi umum mengenai perawatan kulit atau sarankan konsultasi lebih lanjut.
Jaga agar respons Anda tetap ringkas, antara 3 hingga 5 kalimat, kecuali jika detail perawatan lengkap diminta.
"""

    try:
        if client is None:
            raise RuntimeError("OpenAI client not configured. Set OPENAI_API_KEY in .env to enable real LLM calls.")

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_message}] + messages,
            temperature=temperature,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting LLM response: {e}")
        return f"[LLM Unavailable] Selamat ulang tahun!"

def moderate_content(text):
    """Checks content for moderation issues using OpenAI's moderation API."""
    try:
        if client is None:
            raise RuntimeError("OpenAI client not configured. Set OPENAI_API_KEY in .env to enable moderation.")
        response = client.moderations.create(input=text)
        moderation_output = response.results[0]
        if moderation_output.flagged:
            print("Content flagged by moderation API.")
            return True, moderation_output.categories.model_dump_json(indent=2)
        else:
            return False, "Content is clean."
    except Exception as e:
        print(f"Error during content moderation: {e}")
        return False, "Moderation service unavailable."
