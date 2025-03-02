# import cv2
# import torch
#
# # Загрузка предобученной модели YOLOv5s
# model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
#
# # Загрузка изображения
# image_path = "images.jpg"
# image = cv2.imread(image_path)
#
# # Преобразование изображения из BGR в RGB
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#
# # Передача изображения в модель для детекции объектов
# results = model(image)
#
# # Отображение результатов
# results.show()
#
# # Получение информации о найденных объектах
# detections = results.pandas().xyxy[0]
# print(detections)



import cv2
import torch

# Загрузка предобученной модели YOLOv5s
model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)

# Загрузка изображения
image_path = "images.jpg"
image = cv2.imread(image_path)

# Преобразование изображения из BGR в RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Передача изображения в модель для детекции объектов
results = model(image)

# Сохранение результатов в файл
results.save("output.jpg")