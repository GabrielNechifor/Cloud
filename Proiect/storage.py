from google.cloud import storage

CLOUD_STORAGE_BUCKET = "storage_project_cloud"


def store_file(user_email, folder, filename, filedata):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)

    file_path = user_email + "/" + folder + "/" + filename

    blob = bucket.blob(file_path).upload_from_string(filedata)
    return bucket.blob(file_path).public_url


def delete_file(user_email, folder):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)

    folder_path = user_email + "/" + folder + "/"
    
    blobs = bucket.list_blobs(prefix=folder_path)
    for blob in blobs:
        blob.delete()


def get_file(user_email, folder, filename):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)

    file_path = user_email + "/" + folder + "/" + filename
    blob = bucket.blob(file_path)
    file_data = blob.download_as_string()
    return file_data




#data = open("D:\Facultate\CC\Cloud\Tema3\Image\Kamina quote.jpg", "rb").read()

#print(store_file("gabriel", "test_folder", "test_file", "test_data"))
#delete_file("gabriel", "test_folder")
#print(get_file("gabriel", "test_folder", "test_file"))