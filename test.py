from pydub import AudioSegment
from pydub.playback import play
from pytube import YouTube

yt=YouTube("https://www.youtube.com/watch?v=REmZhFKmOmo".format(id))
slow_stream = yt.streams.get_audio_only(subtype="mp4").download(filename="wokeuplikethis.mp4")

sound = AudioSegment.from_file('wokeuplikethis.mp4')

# shift the pitch up by half an octave (speed will increase proportionally)
octaves = -0.5

new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))

# keep the same samples but tell the computer they ought to be played at the 
# new, higher sample rate. This file sounds like a chipmunk but has a weird sample rate.
hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

# now we just convert it to a common sample rate (44.1k - standard audio CD) to 
# make sure it works in regular audio players. Other than potentially losing audio quality (if
# you set it too low - 44.1k is plenty) this should now noticeable change how the audio sounds.
hipitch_sound = hipitch_sound.set_frame_rate(44100)

#Play pitch changed sound
# play(hipitch_sound)

#export / save pitch changed sound
hipitch_sound.export("./media/wokeuplikethisfast.mp3", format="mp3")