from flask import Flask
from flask_api import status
from pytube import YouTube
from pydub import AudioSegment
from pedalboard import Pedalboard, Reverb
from pedalboard.io import AudioFile
import os

app = Flask(__name__)
media_folder = "./media"


@app.route('/send_video_id/<id>', methods=['POST'])
def send_video_url(id):
    if id.isalnum():
        download_sound(id, "{}/sound.mp3".format(media_folder))
        reverb_sound("{}/sound.mp3".format(media_folder))
        slow_sound("{}/sound.mp3".format(media_folder))

        return "Success", status.HTTP_200_OK
    return "Bad Request", status.HTTP_400_BAD_REQUEST


def download_sound(video_id, output_path):
    mp4_file = "{}/sound.mp4".format(media_folder)
    yt = YouTube("https://www.youtube.com/watch?v={}".format(video_id))
    yt.streams.get_audio_only(
        subtype="mp4").download(
        media_folder,
        "sound.mp4")
    AudioSegment.from_file(mp4_file).export(output_path, format="mp3")
    os.remove(mp4_file)


def reverb_sound(sound_path, room_size=0.25, wet_level=0.2, dry_level=0.1):
    with AudioFile(sound_path) as f:
        audio = f.read(f.frames)
        samplerate = f.samplerate
    board = Pedalboard([Reverb(room_size, wet_level, dry_level)])
    effected = board(audio, samplerate)
    with AudioFile(sound_path, 'w', samplerate, effected.shape[0]) as f:
        f.write(effected)


def slow_sound(sound_path, octaves=-0.5):
    sound = AudioSegment.from_file(sound_path)
    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
    slow_sound = sound._spawn(
        sound.raw_data, overrides={
            'frame_rate': new_sample_rate})
    slow_sound = slow_sound.set_frame_rate(44100)
    slow_sound.export(sound_path, format="mp3")


if __name__ == '__main__':
    app.run()
