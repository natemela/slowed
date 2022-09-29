from flask import Flask
from flask_api import status
from pytube import YouTube
from pydub import AudioSegment
import os

app = Flask(__name__)
media_folder = "./media"


@app.route('/send_video_id/<id>', methods=['POST'])
def send_video_url(id):
    if id.isalnum():
        download_sound(
            video_id=id,
            output_path="{}/".format(media_folder))
        slow_sound(input_path="{}/sound.mp4".format(media_folder),
                   output_path="{}/".format(media_folder))
        os.remove("{}/sound.mp4".format(media_folder))

        return "Success", status.HTTP_200_OK
    return "Bad Request", status.HTTP_400_BAD_REQUEST


def download_sound(video_id, output_path, filename="sound.mp4"):
    yt = YouTube("https://www.youtube.com/watch?v={}".format(video_id))
    yt.streams.get_audio_only(subtype="mp4").download(output_path, filename)


def slow_sound(
        input_path,
        output_path,
        filename="slow_sound.mp3",
        octaves=-0.5):
    sound = AudioSegment.from_file(input_path)
    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
    slow_sound = sound._spawn(
        sound.raw_data, overrides={
            'frame_rate': new_sample_rate})
    slow_sound = slow_sound.set_frame_rate(44100)
    slow_sound.export("{}{}".format(output_path, filename), format="mp3")


if __name__ == '__main__':
    app.run()
