import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import warnings
warnings.filterwarnings("ignore")


class NlgModel:
    def __init__(self, model_path, tokenizer_path, device=None):
        """
        Initialize the NlgModel with the specified model and tokenizer paths.
        
        Args:
            model_path (str): Path to the pytorch model weights (e.g., pytorch_model.bin).
            tokenizer_path (str): Path to the tokenizer model (e.g., spiece.model).
            device (torch.device): Device to load the model onto (e.g., 'cuda' or 'cpu').
        """
        try:
            # Load the tokenizer
            self.tokenizer = T5Tokenizer.from_pretrained(tokenizer_path, legacy=False)
        except Exception as e:
            print(f"Error loading tokenizer: {e}")
            raise

        try:
            # Load the model
            self.model = T5ForConditionalGeneration.from_pretrained("t5-small")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
        
        # Resize embeddings to include new tokens (if applicable)
        self.model.resize_token_embeddings(len(self.tokenizer), mean_resizing=False)
        
        # Move model to the correct device
        device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.device = torch.device(device)
        self.model.to(self.device)
        
        # Load the fine-tuned weights
        state_dict = torch.load(f"{model_path}\\pytorch_model.bin", map_location=self.device, weights_only=True)
        self.model.load_state_dict(state_dict)
        
        # Set the model to evaluation mode
        self.model.eval()

    def generate_response(self, input_text, max_length=50):
        """
        Generate a response from the model for a given input text.
        
        Args:
            input_text (str): The input string for the model to generate a response for.
            max_length (int): The maximum length of the response.
        
        Returns:
            str: The generated response from the model.
        """
        # Tokenize the input text
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt").to(self.device)
        # Generate a response
        output_ids = self.model.generate(input_ids, max_length=max_length)
        # Decode the output and return the response
        response = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return response
    
    def respond_to_input(self, input_string):
        """
        Receives an input string and prints the model's response.
        
        Args:
            input_string (str): The input string for the model to generate a response for.
        """
        # Get the model's response
        response = self.generate_response(input_string)
        
        # Resutn the response
        return response
