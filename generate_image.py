from util.oss_util import OSSUtil 
oss = OSSUtil()

def upload_image_and_generate_thumbnail(png_path):
    """根据截图上传图片"""
    image_key = oss.get_default_file_key(png_path)
    original_image_key = oss.upload_file_to_r2(png_path, image_key)

    thumbnail_key = oss.generate_thumbnail_image(original_image_key,image_key)

    return original_image_key, thumbnail_key

original_image_key, thumbnail_key = upload_image_and_generate_thumbnail("./images/openai-codex.png")
print(f"Original image uploaded to: {original_image_key}")
print(f"Thumbnail generated: {thumbnail_key}")