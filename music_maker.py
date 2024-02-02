import numpy as np
import av
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from torchvision.io import read_video
from transformers import AutoImageProcessor, AutoTokenizer, VisionEncoderDecoderModel



def make_music(model_loc, video_url):
  device = "cuda" if torch.cuda.is_available() else "cpu"

  image_processor = AutoImageProcessor.from_pretrained("MCG-NJU/videomae-base")
  tokenizer = AutoTokenizer.from_pretrained("gpt2")
  model = VisionEncoderDecoderModel.from_pretrained("Neleac/timesformer-gpt2-video-captioning").to(device)

  state_dict = torch.load(model_loc)
  model.load_state_dict(state_dict)

  model.eval()

  with torch.no_grad():
    video_path = video_url
    container = av.open(video_path)

    seg_len = container.streams.video[0].frames
    clip_len = model.config.encoder.num_frames
    indices = set(np.linspace(0, seg_len, num=clip_len, endpoint=False).astype(np.int64))
    frames = []
    container.seek(0)
    for i, frame in enumerate(container.decode(video=0)):
        if i in indices:
            frames.append(frame.to_ndarray(format="rgb24"))

    gen_kwargs = {
        "min_length": 10,
        "max_length": 20,
        "num_beams": 8,
    }
    pixel_values = image_processor(frames, return_tensors="pt").pixel_values.to(device)
    tokens = model.generate(pixel_values, **gen_kwargs)
    caption = tokenizer.batch_decode(tokens, skip_special_tokens=True)[0]
    print(caption)
    return caption