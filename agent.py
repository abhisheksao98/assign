"""
Main AI agent module that handles queries and generates responses.
"""
import os
import google.generativeai as genai
from typing import Dict, List, Optional
from database import PhoneDatabase
from prompt_engine import PromptEngine
from dotenv import load_dotenv

load_dotenv()


class ShoppingAgent:
    def __init__(self):
        self.db = PhoneDatabase()
        self.prompt_engine = PromptEngine()
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        #  use newer Gemini 2.5 models (as of Dec 2024)
        model_names = [
            'gemini-2.5-flash',      # Latest fast model (recommended)  
        ]
        
        self.model = None
        for model_name in model_names:
            try:
                self.model = genai.GenerativeModel(model_name)
                # Test if model works by checking if it's accessible
                print(f"✅ Using model: {model_name}")
                break
            except Exception as e:
                error_str = str(e)
                # Skip quota errors but log them
                if "429" in error_str or "quota" in error_str.lower():
                    print(f"⚠️  Model {model_name} - Quota exceeded, trying next...")
                else:
                    print(f"❌ Model {model_name} not available: {error_str[:100]}")
                continue
        
        if self.model is None:
            raise ValueError(
                "Could not initialize any Gemini model. Please check your API key and available models. "
                "Run 'python check_models.py' to see available models for your API key."
            )
        
    def handle_query(self, query: str) -> Dict:
        """Handle a user query and return response."""
        # Safety checks
        if self.prompt_engine.is_adversarial(query):
            return {
                "response": "I'm a shopping assistant for mobile phones. I can help you find and compare phones, but I cannot reveal internal system details or make inappropriate statements. How can I help you with mobile phone shopping?",
                "phones": [],
                "type": "safety_refusal"
            }
        
        if self.prompt_engine.is_irrelevant(query):
            return {
                "response": "I'm specialized in helping with mobile phone shopping. I can help you find phones, compare models, explain features, and make recommendations. What phone are you looking for?",
                "phones": [],
                "type": "redirect"
            }
        
        # Extract intent and filters
        filters = self.prompt_engine.extract_filters(query)
        comparison_models = self.prompt_engine.extract_comparison_models(query)
        
        # Get relevant phones
        phones_data = []
        
        if comparison_models:
            # Comparison mode
            phones_data = self.db.get_phones_by_names(comparison_models)
        elif filters:
            # Filtered search
            phones_data = self.db.search_phones(filters)
        else:
            # General query - get all phones for context
            phones_data = self.db.get_all_phones()
        
        # Build prompt
        system_prompt = self.prompt_engine.build_system_prompt()
        user_prompt = self.prompt_engine.build_user_prompt(query, phones_data)
        
        # Generate response
        try:
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            response = self.model.generate_content(full_prompt)
            
            response_text = response.text
            
            # Determine response type
            response_type = "comparison" if comparison_models else "recommendation" if filters else "general"
            
            return {
                "response": response_text,
                "phones": phones_data,
                "type": response_type
            }
        except Exception as e:
            error_msg = str(e)
            # Provide more helpful error messages
            if "404" in error_msg or "not found" in error_msg.lower():
                return {
                    "response": (
                        "I'm having trouble connecting to the AI service. The model may not be available in your region. "
                        "Please check:\n"
                        "1. Your API key is correct\n"
                        "2. The model is available in your region\n"
                        "3. Try restarting the server\n\n"
                        f"Technical error: {error_msg[:200]}"
                    ),
                    "phones": phones_data,
                    "type": "error"
                }
            return {
                "response": f"I encountered an error processing your query. Please try rephrasing it. Error: {error_msg[:200]}",
                "phones": phones_data,
                "type": "error"
            }
    
    def format_phone_for_display(self, phone: Dict) -> Dict:
        """Format phone data for frontend display."""
        return {
            "id": phone["id"],
            "name": phone["name"],
            "brand": phone["brand"],
            "price": phone["price"],
            "display": f"{phone['display_size']}\" {phone['display_type']}",
            "processor": phone["processor"],
            "ram": f"{phone['ram']}GB",
            "storage": f"{phone['storage']}GB",
            "camera_rear": phone["camera_rear"],
            "camera_front": phone["camera_front"],
            "battery": f"{phone['battery']}mAh",
            "charging": phone["charging"],
            "os": phone["os"],
            "weight": f"{phone['weight']}g",
            "dimensions": phone["dimensions"],
            "ois": "Yes" if phone["ois"] else "No",
            "eis": "Yes" if phone["eis"] else "No",
            "features": phone["features"],
            "image_url": phone["image_url"]
        }

