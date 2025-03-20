from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, model_name: str = "gpt2"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._load_model()

    def _load_model(self):
        """Load the model and tokenizer."""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            self.model.to(self.device)
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def generate_response(self, 
                         prompt: str, 
                         max_length: int = 100,
                         temperature: float = 0.7,
                         top_p: float = 0.9) -> Dict[str, Any]:
        """Generate a response from the model."""
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=temperature,
                    top_p=top_p,
                    pad_token_id=self.tokenizer.eos_token_id
                )

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            tokens_used = len(outputs[0])

            return {
                "response": response,
                "tokens_used": tokens_used,
                "model": self.model_name
            }
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text."""
        return len(self.tokenizer.encode(text))

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        return {
            "name": self.model_name,
            "device": str(self.device),
            "parameters": sum(p.numel() for p in self.model.parameters())
        } 