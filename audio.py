from pygame import mixer


def play_track():
    mixer.music.load("assets/audio/song.ogg")
    mixer.music.set_volume(0.1)
    mixer.music.play(loops=-1)


class Audio:
    def __init__(self):
        mixer.init()
