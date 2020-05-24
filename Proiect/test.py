import text_to_text
import requests
import io, json

url = 'http://127.0.0.1:5000/image_to_text'
image_data = io.open("D:\Facultate\CC\Cloud\Tema3\Image\Kamina quote.jpg", "rb").read()
io.open("D:\Facultate\CC\image.txt","w").write(str(image_data))
to = "en"
image_data = "'" + str(bytes) + "'"
myobj = {'image_data': image_data,
         'to' : to}



result = requests.post(url, json = myobj)
print(result.text)
