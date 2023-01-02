import json
import tempfile
import os
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import PERSISTENT_DELIVERY_MODE
from gridfs import GridFS
from bson.objectid import ObjectId
import moviepy.editor


def start(message, fs_videos: GridFS, fs_mp3s: GridFS, channel: BlockingChannel):
    message = json.loads(message)

    # create a temp file in a temp directory and write video data to it
    temp_file = tempfile.NamedTemporaryFile()
    # video contents
    out = fs_videos.get(ObjectId(message["video_file_id"]))
    # add video content to empty file
    temp_file.write(out.read())
    # create audio from temp video file
    audio = moviepy.editor.VideoFileClip(temp_file.name).audio
    # After close, temp file is automatically deleted
    temp_file.close()

    # Write audio to the file
    temp_file_path = tempfile.gettempdir() + f"/{message['video_file_id']}.mp3"
    audio.write_audiofile(temp_file_path)

    # save file to mongo
    audio_file = open(temp_file_path, "rb")  # read in binary
    audio_data = audio_file.read()
    audio_file_id = fs_mp3s.put(audio_data)

    # clean up
    audio_file.close()
    os.remove(temp_file_path)

    # update the message with the gridfs audio file id
    message["mp3_file_id"] = str(audio_file_id)

    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=PERSISTENT_DELIVERY_MODE),
        )
    except Exception:
        # rollback saved mp3 file because it cannot be processed without the message
        fs_mp3s.delete(audio_file_id)
        return "failed to publish message"
