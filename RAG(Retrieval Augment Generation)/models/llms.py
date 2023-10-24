from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Define a Language Model class
class LLM:
    def __init__(self, model_name):
        # Determine the device to use (GPU if available, otherwise CPU)
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        
        # Load the pre-trained language model with specific settings
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,  # Set the data type to float16
            load_in_8bit=True,         # Load in 8-bit format if available
            device_map='auto'          # Automatically select the device
        ).bfloat16()  # Convert the model to bfloat16 for lower precision
        
        # Initialize the tokenizer for the same model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Set custom padding token and padding side
        self.tokenizer.pad_token = "[PAD]"
        self.tokenizer.padding_side = "left"

    def generate_response(self, messages, max_tokens=100, do_sample=True):
        # Tokenize the input messages and move them to the selected device (GPU or CPU)
        input_ids = self.tokenizer(
            messages,
            max_length=512,
            padding=True,
            truncation=True,
            return_tensors='pt'
        ).input_ids.cuda()
        
        with torch.no_grad():
            # Generate a response using the loaded model
            generated_ids = self.model.generate(
                input_ids,
                pad_token_id=self.tokenizer.pad_token_id,
                max_new_tokens=max_tokens,
                do_sample=do_sample,
                temperature=0.3  # Adjust the sampling temperature
            )
            # Decode the generated tokens into a human-readable response
            response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=False)[0]
        
        return response

# Main program
if __name__ == '__main__':
    # Specify the model name to use
    model_name = "mistralai/Mistral-7B-Instruct-v0.1"
    
    # Create an instance of the Language Model class with the specified model
    llm = LLM(model_name)
