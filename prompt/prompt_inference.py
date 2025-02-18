from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

def build_prompt(context: str, user_question: str) -> str:
    """
    Build a prompt string that includes the retrieved context.
    """
    prompt = f"""You are a helpful assistant. Use the following context to answer questions.
Context:
{context}

Question: {user_question}

Answer (please include citations like [1], [2] if relevant):
"""
    return prompt

class LocalLLMInference:
    def __init__(self, model_name="tiiuae/falcon-7b-instruct", device_map="auto", torch_dtype=torch.float16):
        """
        Loads a local LLM model from Hugging Face. 
        Adjust parameters for your hardware (M2 might need float16 on 'mps').
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=device_map,       # "mps" or "auto"
            torch_dtype=torch_dtype
        )
        self.model.eval()
        
        self.generator = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_length=512
        )
    
    def generate_answer(self, prompt: str, temperature=0.7, top_p=0.9):
        output = self.generator(prompt, temperature=temperature, top_p=top_p, num_return_sequences=1)
        return output[0]["generated_text"]
