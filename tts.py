
import subprocess
import os

def speak_text_cli(
    text,
    model_name="F5-TTS",
    model_cfg="/Users/huy/Desktop/training/F5-TTS/src/f5_tts/configs/F5TTS_Base_train.yaml",
    ckpt_file="/Users/huy/Desktop/training/F5-TTS/ckpts/F5TTS_Base_vocos_custom_my_speak_custom/model_last.pt",
    vocab_file="/Users/huy/Desktop/training/F5-TTS/data/my_speak_custom_custom/vocab.txt",
    output_dir=".",
    output_file="assistant_reply.wav"
):
    """
    Calls f5-tts_infer-cli to generate speech and ensures correct WAV format.
    """

    # Step 1: Run f5-tts_infer-cli to generate audio
    cmd = [
        "f5-tts_infer-cli",
        "--model", model_name,
        "--model_cfg", model_cfg,
        "--ckpt_file", ckpt_file,
        "--vocab_file", vocab_file,
        "--gen_text", text,
        "--output_dir", output_dir,
        "--output_file", output_file
    ]

    print("Running command:", " ".join(cmd))
    subprocess.run(cmd, check=True)

    # Step 2: Convert the WAV file to 16-bit PCM, 44.1 kHz (for compatibility)
    fixed_output_file = os.path.join(output_dir, "fixed_" + output_file)
    convert_cmd = [
        "ffmpeg", "-i", os.path.join(output_dir, output_file),
        "-acodec", "pcm_s16le", "-ar", "44100", fixed_output_file, "-y"
    ]
    
    print("Converting to standard WAV format...")
    subprocess.run(convert_cmd, check=True)

    # Step 3: Play the converted audio
    print(f"✅ Playing audio: {fixed_output_file}")
    subprocess.run(["afplay", fixed_output_file])

    return fixed_output_file


# import torch
# import torchaudio
# import os

# from f5_tts.model import DiT
# from f5_tts.infer.utils_infer import (
#     load_model,
#     load_vocoder,
#     infer_process,
#     device as default_device
# )

# F5TTS_BASE_CONFIG = dict(
#     dim=1024,
#     depth=22,
#     heads=16,
#     ff_mult=2,
#     text_dim=512,
#     conv_layers=4,
#     checkpoint_activations=False
# )

# class MyDirectTTS:
#     def __init__(
#         self,
#         ckpt_file="/Users/huy/Desktop/training/F5-TTS/ckpts/F5TTS_Base_vocos_custom_my_speak_custom/model_last.pt",
#         vocab_file="/Users/huy/Desktop/training/F5-TTS/data/my_speak_custom_custom/vocab.txt",
#         device="cpu"
#     ):
#         # Let the code in utils_infer see the device
#         global default_device
#         default_device = device
#         self.device = device

#         # 1) Load diffusion model
#         self.model = load_model(
#             model_cls=DiT,
#             model_cfg=F5TTS_BASE_CONFIG,
#             ckpt_path=ckpt_file,
#             mel_spec_type="vocos",
#             vocab_file=vocab_file,  # << absolute path
#             ode_method="euler",
#             use_ema=True,
#             device=self.device
#         )

#         # 2) Load vocoder
#         self.vocoder = load_vocoder(
#             vocoder_name="vocos",
#             is_local=False,
#             local_path="",
#             device=self.device
#         )

#     def speak_text_direct(self, text, ref_audio=None, ref_text=None, out_path="assistant_reply.wav"):
#         if not ref_audio:
#             # if your model requires an actual reference wave, set this to an existing .wav
#             ref_audio = "/Users/huy/Desktop/training/F5-TTS/data/my_speak_custom_custom/wavs/some_short_ref.wav"
#         if not ref_text:
#             ref_text = "Hello reference text."

#         final_wave, sr, _ = infer_process(
#             ref_audio=ref_audio,
#             ref_text=ref_text,
#             gen_text=text,
#             model_obj=self.model,
#             vocoder=self.vocoder,
#             mel_spec_type="vocos",
#             device=self.device
#         )

#         waveform = torch.from_numpy(final_wave).unsqueeze(0)
#         torchaudio.save(out_path, waveform, sample_rate=sr)
#         return out_path
