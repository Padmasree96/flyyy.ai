import os
from langchain_google_genai import ChatGoogleGenerativeAI
from app.models.boq_schema import BOQList, BOQItem

def extract_with_ai(raw_text: str, industry: str = "construction"):
    print("🚀 Starting the Full Extraction Looper...")
    
    # 1. SETUP THE AI (Use your key here)
    my_key = os.getenv("GOOGLE_API_KEY") 
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=my_key, temperature=0)
    smart_ai = llm.with_structured_output(BOQList)

    all_extracted_items = []
    chunk_size = 3000  # We can try a slightly bigger bite now
    
    # 2. THE LOOP: Move through the text in steps
    for i in range(0, len(raw_text), chunk_size):
        print(f"📦 Processing section starting at character {i}...")
        
        current_chunk = raw_text[i : i + chunk_size]
        
        prompt = f"""
        Extract the BOQ items from this specific section of text in the {industry} industry. 
        If there are no items in this section, return an empty list.
        
        TEXT SECTION:
        {current_chunk}
        """
        
        try:
            result = smart_ai.invoke(prompt)
            if result and result.items:
                all_extracted_items.extend(result.items)
                print(f"✅ Found {len(result.items)} items in this section.")
        except Exception as e:
            print(f"⚠️ Skipping a small section due to error: {str(e)}")
            continue

    print(f"🎯 FINISHED! Total items found: {len(all_extracted_items)}")
    
    # Return everything we found as one big list
    return BOQList(items=all_extracted_items)
