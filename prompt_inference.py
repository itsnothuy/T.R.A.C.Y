from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
print(torch.device("cpu"))  # Should print: cpu


# def build_prompt(context: str, user_question: str) -> str:
#     """
#     Build a prompt string that includes the retrieved context.
#     """
#     prompt = f"""You are a helpful assistant. Use the following context to answer questions.
# Context:
# {context}

# Question: {user_question}

# Answer (please include citations like [1], [2] if relevant):
# """
#     return prompt

# class LocalLLMInference:
#     def __init__(self, model_name="tiiuae/falcon-7b-instruct", device_map="auto", torch_dtype=torch.float32):
#         """
#         Loads a local LLM model from Hugging Face. 
#         Adjust parameters for your hardware (M2 might need float16 on 'mps').
#         """
#         self.tokenizer = AutoTokenizer.from_pretrained(model_name)
#         self.model = AutoModelForCausalLM.from_pretrained(
#             model_name,
#             device_map={"": "cpu"},       # "mps" or "auto"
#             torch_dtype=torch_dtype
#         )
#         self.model.eval()
        
#         self.generator = pipeline(
#             "text-generation",
#             model=self.model,
#             tokenizer=self.tokenizer,
#             max_length=512
#         )
    
#     def generate_answer(self, prompt: str, temperature=0.7, top_p=0.9):
#         output = self.generator(prompt, temperature=temperature, top_p=top_p, num_return_sequences=1)
#         return output[0]["generated_text"]



from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
# import torch

def build_prompt(context: str, user_question: str) -> str:
    """
    A simpler prompt string that includes the retrieved context.
    """
    prompt = f"""You are a helpful assistant. Use the following context to answer questions.
Context:
{context}

Question: {user_question}

Answer (please include citations like [1], [2] if relevant):
"""
    return prompt

def build_prompt_with_examples(context: str, user_question: str) -> str:
    """
    A more advanced prompt that provides examples of Q/A style,
    encouraging the model to produce more structured answers.
    """
    base_prompt = f"""
You are a helpful assistant. You have been given the following context to answer the user's question:
{context}

Here are some example Q&A formats to emulate:

Example 1:
Q: "What are the fat-soluble vitamins?"
A: "They include Vitamins A, D, E, and K, which can be stored in body fat..."

Example 2:
Q: "What are the causes of type 2 diabetes?"
A: "Type 2 diabetes is often caused by..."

Now, please provide a clear, concise, and well-cited answer to the user's query below.

User Query: {user_question}

Answer (with citations referencing [1], [2], etc.):
"""
    return base_prompt

class LocalLLMInference:
    def __init__(self, model_name="tiiuae/falcon-7b-instruct", device_map="auto", torch_dtype=torch.float32):
        """
        Loads a local LLM model from Hugging Face. 
        Adjust parameters for your hardware (M2 might need float16 on 'mps').
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, truncation=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=device_map,       # "mps", "cuda", or "auto"
            torch_dtype=torch_dtype
        )
        self.model.eval()
        
        self.generator = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_length=1500
        )
    
    def generate_answer(self, prompt: str, temperature=0.7, top_p=0.9):
        output = self.generator(prompt, temperature=temperature, top_p=top_p, num_return_sequences=1)
        return output[0]["generated_text"]
