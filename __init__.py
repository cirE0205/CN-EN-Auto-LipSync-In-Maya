from .auto_lip_sync import language_settings

def start():
    from . import auto_lip_sync
    return auto_lip_sync.start()
