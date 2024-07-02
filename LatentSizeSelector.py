import os
import json
import comfy
import torch


class LatentSizeSelector:
    def __init__(self):
        self.device = comfy.model_management.intermediate_device()

    @classmethod
    def INPUT_TYPES(cls):
        cls.size_latent, cls.size_dict = cls.read_sizes()
        return {
            'required': {
                'size_selected': (cls.size_latent,),
                'batch_size': ("INT", {"default": 1, "min": 1, "max": 4096})
            }
        }

    RETURN_TYPES = ("INT", "INT", "LATENT")
    RETURN_NAMES = ("Width", "Height", "Latent")
    FUNCTION = "return_res"
    OUTPUT_NODE = True
    CATEGORY = "AILab"

    def return_res(self, size_selected, batch_size):
        # Extract resolution name and dimensions using the key
        selected_info = self.size_dict[size_selected]
        width = int(selected_info["width"])
        height = int(selected_info["height"])
        latent = torch.ones([batch_size, 16, height // 8, width // 8], device=self.device) * 0.0609
        return {"Width": width}, {"Height": height}, {"Latent": latent},

    @staticmethod
    def read_sizes():
        p = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(p, 'latentsize.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        size_latent = [f"{key}" for key, value in data['latentsize'].items()]
        size_dict = {f"{key}": value for key, value in data['latentsize'].items()}
        return size_latent, size_dict


NODE_CLASS_MAPPINGS = {
    "LatentSizeSelector": LatentSizeSelector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LatentSizeSelector": "Laten Size Selector 🖼️"
}


