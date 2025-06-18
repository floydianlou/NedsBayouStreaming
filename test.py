import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="dliev5zuy",
    api_key="427978424534537",
    api_secret="6hkZwHzJHI8DqJMTv1tyi5ZNTHY",
)

result = cloudinary.uploader.upload("test.jpg")  # assicurati che 'test.jpg' esista nella stessa cartella
print("✅ Upload riuscito! Risultato Cloudinary:")
print(result)