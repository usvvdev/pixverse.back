#!/bin/bash

# Проверка, указан ли путь к директории
if [ -z "$1" ]; then
  echo "❌ Укажите путь к папке с видео."
  echo "Пример: ./normalize_videos.sh /путь/к/папке"
  exit 1
fi

# Каталог с видео
INPUT_DIR="$1"
OUTPUT_DIR="${INPUT_DIR%/}/normalized"
TARGET_WIDTH=1080
TARGET_HEIGHT=1920

mkdir -p "$OUTPUT_DIR"

echo "🎬 Начинается обработка видео в папке: $INPUT_DIR"
echo "📁 Результат будет в папке: $OUTPUT_DIR"

# Обработка всех mp4 файлов
for VIDEO in "$INPUT_DIR"/*.mp4; do
  FILENAME=$(basename "$VIDEO")
  OUTPUT_PATH="$OUTPUT_DIR/$FILENAME"

  echo "🔧 Обработка: $FILENAME"

  ffmpeg -i "$VIDEO" \
    -vf "scale=w=iw*min($TARGET_WIDTH/iw\,${TARGET_HEIGHT}/ih):h=ih*min($TARGET_WIDTH/iw\,${TARGET_HEIGHT}/ih),pad=$TARGET_WIDTH:$TARGET_HEIGHT:($TARGET_WIDTH-iw*min($TARGET_WIDTH/iw\,${TARGET_HEIGHT}/ih))/2:($TARGET_HEIGHT-ih*min($TARGET_WIDTH/iw\,${TARGET_HEIGHT}/ih))/2:black" \
    -c:a copy "$OUTPUT_PATH" -y
done

echo "✅ Обработка завершена."
