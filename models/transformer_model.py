import torch
import torch.nn as nn
from transformers import PreTrainedModel, PretrainedConfig

class TransformerConfig(PretrainedConfig):
    model_type = "code_intelligen"
    
    def __init__(
        self,
        vocab_size=50257,
        n_positions=1024,
        n_ctx=1024,
        n_embd=768,
        n_layer=12,
        n_head=12,
        **kwargs
    ):
        self.vocab_size = vocab_size
        self.n_positions = n_positions
        self.n_ctx = n_ctx
        self.n_embd = n_embd
        self.n_layer = n_layer
        self.n_head = n_head
        super().__init__(**kwargs)

class TransformerModel(PreTrainedModel):
    config_class = TransformerConfig
    
    def __init__(self, config):
        super().__init__(config)
        self.config = config
        
        self.transformer = nn.Transformer(
            d_model=config.n_embd,
            nhead=config.n_head,
            num_encoder_layers=config.n_layer,
            num_decoder_layers=config.n_layer,
            dim_feedforward=config.n_embd * 4
        )
        
        self.embedding = nn.Embedding(config.vocab_size, config.n_embd)
        self.output = nn.Linear(config.n_embd, config.vocab_size)
    
    def forward(self, input_ids, attention_mask=None, labels=None):
        embeddings = self.embedding(input_ids)
        
        transformer_output = self.transformer(
            embeddings,
            embeddings
        )
        
        logits = self.output(transformer_output)
        
        loss = None
        if labels is not None:
            loss_fct = nn.CrossEntropyLoss()
            loss = loss_fct(logits.view(-1, self.config.vocab_size), labels.view(-1))
        
        return {
            'logits': logits,
            'loss': loss
        }
    
    def generate(self, input_ids, max_length=100, temperature=1.0):
        self.eval()
        
        with torch.no_grad():
            for _ in range(max_length - input_ids.shape[1]):
                outputs = self.forward(input_ids)
                next_token_logits = outputs['logits'][:, -1, :] / temperature
                
                next_token = torch.multinomial(
                    torch.softmax(next_token_logits, dim=-1),
                    num_samples=1
                )
                
                input_ids = torch.cat([input_ids, next_token], dim=1)
        
        return input_ids