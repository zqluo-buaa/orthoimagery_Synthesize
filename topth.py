import pytorch_lightning as pl
from tutorial_dataset import MyDataset
from cldm.logger import ImageLogger
from cldm.model import create_model, load_state_dict
import torch

def save_model_state_dict():
    ckpt_path = '/media/ziqing/Q/ControlNet-v1-1-nightly/lightning_logs/version_7/checkpoints/epoch=13-step=432963.ckpt'
    
    try:
        # Ensure all operations are on CPU
        device = torch.device('cpu')
        
        # Create and load the model
        model = create_model('./models/cldm_v15.yaml').to(device)
        model.load_state_dict(load_state_dict(ckpt_path, location=device))
        print("Model loaded successfully.")

        # Save the model state dictionary
        torch.save(model.state_dict(), "./ckpt/last.pth")
        print("Model state dictionary saved successfully to ./ckpt/last.pth")

        # Empty cache if using GPU (though we're using CPU here)
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    save_model_state_dict()

