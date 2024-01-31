import os


def get_storage_root():
    return os.getenv('STORAGE_ROOT', '/tmp')


def set_audio_content(token, content):
    with open(f'{get_storage_root()}/{token}.wav', 'wb') as f:
        f.write(content)
    return True