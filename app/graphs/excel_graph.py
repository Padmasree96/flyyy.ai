import os
from typing import Type, Any
from loguru import logger
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from app.models.boq_schema import BOQList

class AITextExtractor:
    """
    A foundational, reusable class for extracting structured records from 
    unstructured or messy data (e.g., raw Excel text dumps) using Generative AI.
    """

    def __init__(self, model_name: str = None, temperature: float = 0.0):
        # Ensure no hardcoding: fallback to OS environment variables.
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
        self.temperature = temperature
        
        logger.info(f"Initializing AITextExtractor with model: {self.model_name}")
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=self.model_name, 
                temperature=self.temperature
            )
        except Exception as e:
            logger.error(f"Failed to initialize language model '{self.model_name}': {e}")
            raise

    def _build_prompt(self) -> ChatPromptTemplate:
        """
        Creates a structured prompt template optimized for dynamic industry injection.
        This provides generic applicability across all industries.
        """
        system_instruction = (
            "You are an expert data analyst specializing in the {industry} domain. "
            "Your objective is to carefully review raw, unstructured spreadsheet data and extract relevant items into a clean, structured array. "
            "Ensure you extract valid descriptions, quantities, units, and relevant categorization. "
            "Follow these rules:\n"
            "- If a brand or manufacturer is not obvious, use 'Generic'.\n"
            "- If a unit of measurement is not specified, use '-'.\n"
            "- Ignore irrelevant data like grand totals, document headers, or blank lines."
        )
        
        user_instruction = (
            "Please parse the following unstructured data:\n\n"
            "{messy_text}\n\n"
            "Extract the data strictly adhering to the requested structured format."
        )
        
        return ChatPromptTemplate.from_messages([
            ("system", system_instruction),
            ("human", user_instruction)
        ])

    def extract(
        self, 
        messy_text: str, 
        industry: str = "construction", 
        response_schema: Type[BaseModel] = BOQList
    ) -> Any:
        """
        Executes the extraction pipeline against the given text.
        
        Args:
            messy_text (str): The unstructured text dumped from the file.
            industry (str): The contextual industry to guide the AI's understanding.
            response_schema (Type[BaseModel]): Pydantic schema governing the output format.
            
        Returns:
            An instance of the provided response_schema containing the parsed data.
        """
        if not messy_text or not messy_text.strip():
            logger.warning("Empty text string provided for AI extraction.")
            # Return an empty schema gracefully
            return response_schema(items=[])

        try:
            logger.debug(f"Configuring structured output for schema: {response_schema.__name__}")
            structured_llm = self.llm.with_structured_output(response_schema)
            
            # Combine the dynamic prompt block with the bounded output model
            prompt_template = self._build_prompt()
            extraction_chain = prompt_template | structured_llm
            
            logger.info(f"Invoking AI extraction via {self.model_name} for industry: '{industry}', text length: {len(messy_text)}")
            result = extraction_chain.invoke({
                "industry": industry,
                "messy_text": messy_text
            })
            
            logger.info("Successfully extracted structured dataset using AI pipeline.")
            return result

        except Exception as e:
            logger.exception("AI Extraction pipeline encountered a critical error.")
            raise

# ─── Reusable Helper Interface ───

def extract_with_ai(messy_text: str, industry: str = "construction") -> BOQList:
    """
    A simplified, backwards-compatible helper function for immediate usage in route controllers.
    """
    extractor = AITextExtractor()
    return extractor.extract(
        messy_text=messy_text, 
        industry=industry, 
        response_schema=BOQList
    )
