import os
import torch
import se_extractor
from api import BaseSpeakerTTS, ToneColorConverter
import requests


def download_reference_speaker(url):

    # URL of the voice file
    reference_speaker_url = url

    # Local directory where the file will be saved
    local_dir = 'processed'
    os.makedirs(local_dir, exist_ok=True)

    # Local file path
    local_file_path = os.path.join(local_dir, 'speaker_1.mp3')

    # Download and save the file
    response = requests.get(reference_speaker_url)
    if response.status_code == 200:
        with open(local_file_path, 'wb') as file:
            file.write(response.content)
        print(f'File downloaded successfully and saved as {local_file_path}')
        return local_file_path
    else:
        print(f'Failed to download the file. Status code: {response.status_code}')
        return None


def get_reference_speaker_from_folder():
    # Local directory where the file will be saved
    local_dir = 'phonks'
    os.makedirs(local_dir, exist_ok=True)

    # Local file path
    local_file_path = os.path.join(local_dir, '1.wav')
    return local_file_path


async def create_custom_voice_over(text, speaker, reference_speaker, language):
    ckpt_base = 'checkpoints/base_speakers/EN'
    ckpt_converter = 'checkpoints/converter'
    device="cuda:0" if torch.cuda.is_available() else "cpu"
    output_dir = 'outputs'

    base_speaker_tts = BaseSpeakerTTS(f'{ckpt_base}/config.json', device=device)
    base_speaker_tts.load_ckpt(f'{ckpt_base}/checkpoint.pth')

    tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
    tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

    os.makedirs(output_dir, exist_ok=True)

    source_se = torch.load(f'{ckpt_base}/en_default_se.pth').to(device)

    # Download the reference speaker
    # ref_speaker = download_reference_speaker(reference_speaker)
    ref_speaker = get_reference_speaker_from_folder()

    reference_speaker = ref_speaker
    target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, target_dir='processed', vad=True)
    
    source_se = torch.load(f'{ckpt_base}/en_style_se.pth').to(device)
    save_path = f'{output_dir}/output_whispering.wav'

    # Run the base speaker tts
    src_path = f'{output_dir}/tmp.wav'
    base_speaker_tts.tts(text, src_path, speaker=speaker, language=language, speed=0.9)

    # Run the tone color converter
    encode_message = "@MyShell"
    tone_color_converter.convert(
        audio_src_path=src_path, 
        src_se=source_se, 
        tgt_se=target_se, 
        output_path=save_path,
        message=encode_message)
    
    return save_path

