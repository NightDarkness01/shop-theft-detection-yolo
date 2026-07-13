import datetime
import os
from ultralytics import YOLO

# 1. Загружаем модель
model = YOLO("best.pt")

# 2. Указываем видеофайл
video_source = "video.mp4"

# 3. Создаём папку для скриншотов, если её нет
screenshots_dir = "screenshots"
os.makedirs(screenshots_dir, exist_ok=True)

print("Система мониторинга запущена. Анализ видео...")

# 4. Запускаем распознавание (порог можно оставить 0.25)
results = model.predict(source=video_source, conf=0.25)

# 5. Открываем файл журнала
with open("security_log.txt", "a", encoding="utf-8") as log_file:
    for frame_idx, r in enumerate(results):
        if len(r.boxes) > 0:
            for box in r.boxes:
                confidence = float(box.conf)
                current_time = datetime.datetime.now()
                
                # Формируем запись в лог
                log_entry = f"{current_time:%Y-%m-%d %H:%M:%S} | Обнаружено подозрение | Уверенность: {confidence:.2f}\n"
                print(log_entry.strip())
                log_file.write(log_entry)
                
                # Сохраняем скриншот кадра с рамкой
                timestamp = current_time.strftime("%Y%m%d_%H%M%S_%f")[:-3]  # до миллисекунд
                screenshot_filename = f"{screenshots_dir}/theft_{timestamp}_conf{confidence:.2f}.jpg"
                r.save(screenshot_filename)  # сохраняет изображение с аннотациями
                print(f"  Скриншот сохранён: {screenshot_filename}")

print("\nАнализ видео завершен. Все инциденты записаны в security_log.txt")
print(f"Скриншоты сохранены в папку '{screenshots_dir}/'")