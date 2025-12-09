# main.py

from .config import OPENAI_API_KEY
from .data_loader import load_prices_data
import openai
# from .sheets_manager import get_google_sheet_client, open_spreadsheet, get_worksheet_data, append_row_to_worksheet, find_patient_by_rm_number, get_upcoming_treatments, get_upcoming_birthdays
from .llm_manager import get_llm_response, moderate_content

PRICES_FILE = "data/prices_august.json"
# GOOGLE_SHEET_NAME = "WhatsApp Chatbot Data"
# PATIENT_WORKSHEET_NAME = "Patients"
# CONSULTATION_WORKSHEET_NAME = "Consultations"
# ORDER_WORKSHEET_NAME = "Orders"

def main():
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY not found in .env file.")
        return

    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    print("OpenAI client initialized.")

    prices_data = load_prices_data(PRICES_FILE)
    if prices_data:
        print(f"Successfully loaded {len(prices_data)} treatment prices.")
    else:
        print("Failed to load prices data.")
        return # Exit if prices data is critical and not loaded

    # Temporary direct LLM interaction for testing
    print("\n--- LLM Chat Test ---")
    messages = [] # Initialize conversation history

    while True:
        user_input = input("You (type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        flagged, categories = moderate_content(user_input)
        if flagged:
            print(f"Bot: Warning! Input contains inappropriate content: {categories}. Please rephrase.")
            continue

        messages.append({"role": "user", "content": user_input}) # Add user message to history

        llm_response = get_llm_response(messages, prices_data)
        print("Bot:", llm_response)
        messages.append({"role": "assistant", "content": llm_response}) # Add bot response to history

if __name__ == "__main__":
    main()
