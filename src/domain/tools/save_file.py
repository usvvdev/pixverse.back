# coding utf-8

from fastapi import UploadFile

from pathlib import Path

from tempfile import NamedTemporaryFile

from shutil import copyfileobj


def save_temp_file(
    file: UploadFile,
) -> str:
    """
    Сохраняет загруженный файл во временную директорию на диске.

    Аргументы:
        file (UploadFile): Загруженный файл, переданный пользователем.

    Возвращает:
        Path: Абсолютный путь к сохранённому временному файлу.
    """
    suffix: str = Path(file.filename).suffix

    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        copyfileobj(file.file, tmp)
        return str(Path(tmp.name).resolve())
