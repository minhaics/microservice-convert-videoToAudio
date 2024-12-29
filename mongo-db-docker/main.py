from pymongo import MongoClient
import gridfs

# Kết nối đến MongoDB (chung cổng 27017)
mongo_uri = "mongodb://localhost:27017"
client = MongoClient(mongo_uri)

# Cơ sở dữ liệu
db_videos = client["videos"]
db_mp3s = client["mp3s"]

# GridFS
fs_videos = gridfs.GridFS(db_videos)
fs_mp3s = gridfs.GridFS(db_mp3s)

# Hàm lưu tệp vào GridFS
def save_file_to_gridfs(fs, file_path, file_type):
    with open(file_path, "rb") as f:
        file_id = fs.put(f, filename=file_path.split("/")[-1], type=file_type)
        print(f"Tệp '{file_path}' đã được lưu với ID: {file_id}")
    return file_id

# Hàm tải tệp từ GridFS
def download_file_from_gridfs(fs, file_id, output_path):
    file_data = fs.get(file_id)
    with open(output_path, "wb") as f:
        f.write(file_data.read())
    print(f"Tệp đã được tải xuống tại: {output_path}")

# Kiểm tra GridFS
if __name__ == "__main__":
    # Lưu video vào GridFS
    video_id = save_file_to_gridfs(fs_videos, "sample_video.mp4", "video")
    
    # Lưu MP3 vào GridFS
    mp3_id = save_file_to_gridfs(fs_mp3s, "sample_audio.mp3", "audio")

    # Tải tệp xuống từ GridFS
    download_file_from_gridfs(fs_videos, video_id, "downloaded_video.mp4")
    download_file_from_gridfs(fs_mp3s, mp3_id, "downloaded_audio.mp3")
