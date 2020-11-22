import torch
from transformers import BertTokenizer

MAX_LEN = 256


class ClassificationModel:
    """
    Model used to predict probabilities on emotions
    """
    def __init__(self):
        """
        Load tokenizer and model, setting it to eval mode
        """
        self.tokenizer = BertTokenizer.from_pretrained("tokenizer")
        self.model = torch.load('model/final_model.pt',
                                map_location=torch.device('cpu'))
        self.model.eval()

    def predict_emotions(self, tweets: list) -> list:
        """
        Method that predicts emotion likelihood for each tweet
        :param tweets:
        :return: emotion likelihood
        """
        # Tokenize each tweet and compute its attention mask
        input_ids = [self.tokenizer.encode(tweet, add_special_tokens=True,
                                           max_length=MAX_LEN,
                                           pad_to_max_length=True) for tweet in
                     tweets]
        attention_masks = [[float(i > 0) for i in seq] for seq in input_ids]

        # PyTorch model is fed by torch.tensor
        input_ids = torch.tensor(input_ids)
        attention_masks = torch.tensor(attention_masks)
        # Avoid waisting memory and time computing gradients
        with torch.no_grad():
            output = self.model(input_ids, token_type_ids=None,
                                attention_mask=attention_masks)

        return output[0].tolist()
