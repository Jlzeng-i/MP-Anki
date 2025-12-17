import requests
import json
import re

ANKI_CONNECT_URL = "http://localhost:8765"

def anki_request(action, **params):
    return requests.post(ANKI_CONNECT_URL, json={
        "action": action,
        "version": 6,
        "params": params
    }).json()

# Step 1: Find all cards with reps > 0 (reviewed at least once)
reviews = anki_request("findCards", query="prop:reps>0")
reviewed_card_ids = reviews.get("result", [])

print("Number of reviewed cards:", len(reviewed_card_ids))
print("Reviewed card IDs:", reviewed_card_ids[:10])

if not reviewed_card_ids:
    print("No reviewed cards found. Exiting.")
    exit()

# Step 2: Get card info for those cards
cards_info_resp = anki_request("cardsInfo", cards=reviewed_card_ids)
cards_info = cards_info_resp.get("result", [])

# Step 3: Detect deck name from first card
deck_name = cards_info[0].get("deckName", "anki_deck")

# Step 4: Make filename safe (remove OS-illegal characters)
safe_filename = re.sub(r'[\\/*?:"<>|]', "_", deck_name) + ".json"

# Step 5: Save JSON to file
with open(safe_filename, "w", encoding="utf-8") as f:
    json.dump(cards_info, f, ensure_ascii=False, indent=2)

print(f"\n Saved {len(cards_info)} reviewed cards to: {safe_filename}")
print("\nSample reviewed card:")
print(json.dumps(cards_info[0], indent=2, ensure_ascii=False))