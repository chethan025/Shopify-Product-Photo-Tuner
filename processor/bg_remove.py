import torch
from PIL import Image
from torchvision import transforms
from transformers import AutoModelForImageSegmentation

# --- CONFIG ---
LOCAL_MODEL_PATH = "./processor/BiRefNet"
TARGET_RATIO = 1.0
INTERNAL_PADDING = 0.08
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load model once
model = AutoModelForImageSegmentation.from_pretrained(
    LOCAL_MODEL_PATH,
    trust_remote_code=True,
    local_files_only=True
).to(device).eval()

transform_image = transforms.Compose([
    transforms.Resize((1024, 1024)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225]),
])

def process_to_portrait_with_crop(img, target_ratio, padding_pct):
    bbox = img.getbbox()
    if not bbox:
        return img

    obj_only = img.crop(bbox)
    obj_w, obj_h = obj_only.size

    pad_w = int(obj_w * padding_pct)
    pad_h = int(obj_h * padding_pct)

    padded_obj_w = obj_w + (pad_w * 2)
    padded_obj_h = obj_h + (pad_h * 2)

    padded_obj = Image.new("RGBA", (padded_obj_w, padded_obj_h), (0, 0, 0, 0))
    padded_obj.paste(obj_only, (pad_w, pad_h))

    current_ratio = padded_obj_w / padded_obj_h

    if current_ratio > target_ratio:
        canvas_h = int(padded_obj_w / target_ratio)
        canvas_w = padded_obj_w
    else:
        canvas_w = int(padded_obj_h * target_ratio)
        canvas_h = padded_obj_h

    final_canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    offset = ((canvas_w - padded_obj_w) // 2,
              (canvas_h - padded_obj_h) // 2)
    final_canvas.paste(padded_obj, offset)

    return final_canvas


def remove_background(input_image: Image.Image) -> Image.Image:
    input_image = input_image.convert("RGB")

    with torch.no_grad():
        input_tensor = transform_image(input_image).unsqueeze(0).to(device)

        with torch.cuda.amp.autocast(enabled=device == "cuda"):
            preds = model(input_tensor)[-1].sigmoid().cpu()

        mask = transforms.ToPILImage()(preds[0].squeeze())
        mask = mask.resize(input_image.size, Image.BILINEAR)

        input_image.putalpha(mask)

        result = process_to_portrait_with_crop(
            input_image,
            TARGET_RATIO,
            INTERNAL_PADDING
        )

        del input_tensor
        if device == "cuda":
            torch.cuda.empty_cache()

    return result