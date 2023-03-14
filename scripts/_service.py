"""data file for browser."""

from collections import OrderedDict

_SERVICE = OrderedDict({
    "prompthero": {
        "name": "PromptHero",
        "url_find": "https://prompthero.com/api/v1/search?q=",
        # key to look for if successful response
        "key_out": "results",
        "key_img": "main_image",
        # key with error message, if any
        "err": "errors",
        "map": OrderedDict({
            "prompt": "*",
            "negative_prompt": "Negative prompt",
            "width": "*",
            "height": "*",
            "sampler": "Sampler",
            "num_inference_steps": "Steps",
            "guidance_scale": "CFG scale",
            "c": "CFG scale",
            "seed": "Seed",
            # "model_used": "Model",
            # "model_used_version": "version",
            "replicate_model_version": "Model hash",
            "clipckip": "Clip skip"
        })
    },
    "lexica": {
        "name": "Lexica",
        "url_find": "https://lexica.art/api/v1/search?q=",
        "key_out": "images",
        "key_img": "src",
        "err": "errors",
        "map": OrderedDict({
            "prompt": "*",
            "negative_prompt": "Negative prompt",
            "width": "*",
            "height": "*",
            "sampler": "Sampler",
            "steps": "Steps",
            "guidance": "CFG scale",
            "seed": "Seed",
            "model": "Model"
        })
    },
})
