import os
import json
import torch

class LatentSizeSelector:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        cls.size_sizes, cls.size_dict = cls.read_sizes()  # cls.read_sizes()
        return {
            'required': {
                'size_selected': (cls.size_sizes,),  
                'multiply_factor': ("INT", {"default": 1, "min": 1}),  # multple
                'manual_width': ("INT", {
                    "default": 0,  # default
                    "min": 0,  # min
                }),
                'manual_height': ("INT", {
                    "default": 0,  # default
                    "min": 0,  # min
                }),
                'batch_size': ("INT", {
                "default": 1, "min": 1, "max": 4096})
            }
        }

    RETURN_TYPES = ("INT", "INT", "LATENT")
    RETURN_NAMES = ("width", "height", "samples")
    FUNCTION = "return_res"
    OUTPUT_NODE = True
    CATEGORY = "AILab 🧪"

    def return_res(self, size_selected, multiply_factor, manual_width, manual_height,batch_size):
        print(f"size_selected: {size_selected}, multiply_factor: {multiply_factor}, manual_width: {manual_width}, manual_height: {manual_height}")

        # Initialize width and height from the manual input if provided
        if manual_width > 0 and manual_height > 0:
            width = manual_width * multiply_factor
            height = manual_height * multiply_factor
            latent = torch.ones([batch_size, 16, height // 8, width // 8], device='cpu') * 0.0609  # batch_size = 1
            return {"width": width}, {"height": height}, {"samples": latent}
        else:
            # Extract resolution name and dimensions using the key
            selected_info = self.size_dict[size_selected]
            width = selected_info["width"] * multiply_factor
            height = selected_info["height"] * multiply_factor
            latent = torch.ones([batch_size, 16, height // 8, width // 8], device='cpu') * 0.0609  # batch_size = 1
            return {"width": width}, {"height": height}, {"samples": latent}

    @staticmethod
    def read_sizes():
        p = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(p, 'latentsizes.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
            size_sizes = [f"{key} - {value['name']}" for key, value in data['sizes'].items()]
            size_dict = {f"{key} - {value['name']}": value for key, value in data['sizes'].items()}
        return size_sizes, size_dict

NODE_CLASS_MAPPINGS = {
    "LatentSizeSelector": LatentSizeSelector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LatentSizeSelector": "Latent Size Selector 🖼️"
}
