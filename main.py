import argparse
import asyncio
from pathlib import Path
from aiopath import AsyncPath
import shutil
import logging

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="file_sorter.log",
)


async def read_folder(source: AsyncPath, destination: AsyncPath):
    if not await source.exists():
        logging.error(f"Source folder does not exist: {source}")
        print(f"Source folder does not exist: {source}")
        return

    if not await destination.exists():
        await destination.mkdir(parents=True)

    async for item in source.rglob("*"):
        if await item.is_file():
            await copy_file(item, destination)


async def copy_file(file: AsyncPath, destination: AsyncPath):
    try:
        extension = file.suffix[1:] or "unknown"

        target_folder = destination / extension
        if not await target_folder.exists():
            await target_folder.mkdir(parents=True)

        target_file = target_folder / file.name
        await asyncio.to_thread(shutil.copy2, file, target_file)

        print(f"Copied: {file} -> {target_file}")
    except Exception as e:
        logging.error(f"Error copying file {file} to {destination}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Sort files by extension into folders."
    )
    parser.add_argument("source", type=str, help="Path to the source folder.")
    parser.add_argument("destination", type=str, help="Path to the destination folder.")
    args = parser.parse_args()

    source = AsyncPath(args.source)
    destination = AsyncPath(args.destination)

    asyncio.run(read_folder(source, destination))


if __name__ == "__main__":
    main()
