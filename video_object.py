import cv2
import torch

# Загрузка предобученной модели YOLOv5s
model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)

# Загрузка видео
video_path = "video.mp4"  # Укажите путь к вашему видео
cap = cv2.VideoCapture(video_path)




# Проверка, открылось ли видео
if not cap.isOpened():
    print("Ошибка: Не удалось открыть видео.")
    exit()

# Цикл обработки каждого кадра видео
while True:
    # Чтение кадра
    ret, frame = cap.read()
    if not ret:
        break  # Если кадры закончились, выходим из цикла

    # Преобразование кадра из BGR в RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Передача кадра в модель для детекции объектов
    results = model(frame_rgb)

    # Отображение результатов на кадре
    results.render()  # Добавляет bounding boxes и метки на кадр
    frame_with_detections = cv2.cvtColor(results.ims[0], cv2.COLOR_RGB2BGR)  # Обратно в BGR для OpenCV

    # Отображение кадра с детекциями
    cv2.imshow("YOLOv5 Video Detection", frame_with_detections)

    # Выход по нажатию клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Получение информации о найденных объектах (опционально)
    detections = results.pandas().xyxy[0]
    print(detections)  # Вывод информации в консоль

# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()




