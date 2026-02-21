"""
Cache Cleaner Module
Cleans up old audio files from the cache directory.
Can be run manually or scheduled to run automatically.
"""

import time
from pathlib import Path


class CacheCleaner:

    @staticmethod
    def get_cache_dir():
        """Get the cache directory path"""
        bot_root = Path(__file__).parent.parent
        cache_dir = bot_root / 'cache'
        return cache_dir

    @staticmethod
    def clean_cache(max_age_hours=24):
        """
        Remove cache files older than specified hours

        Args:
            max_age_hours (int): Maximum age of cache files in hours (default: 24)

        Returns:
            tuple: (files_removed, space_freed_mb)
        """
        cache_dir = CacheCleaner.get_cache_dir()

        if not cache_dir.exists():
            print(f"Cache directory does not exist: {cache_dir}")
            return 0, 0

        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        files_removed = 0
        space_freed = 0

        # Get all media files in cache
        media_extensions = ['.webm', '.m4a', '.opus', '.mp3', '.mp4']

        for file_path in cache_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in media_extensions:
                file_age = current_time - file_path.stat().st_mtime

                if file_age > max_age_seconds:
                    try:
                        file_size = file_path.stat().st_size
                        file_path.unlink()
                        files_removed += 1
                        space_freed += file_size
                        print(f"Removed: {file_path.name} (age: {file_age/3600:.1f}h)")
                    except Exception as e:
                        print(f"Error removing {file_path.name}: {e}")

        space_freed_mb = space_freed / (1024 * 1024)
        print(f"\nCache cleanup complete:")
        print(f"  Files removed: {files_removed}")
        print(f"  Space freed: {space_freed_mb:.2f} MB")

        return files_removed, space_freed_mb

    @staticmethod
    def clean_all_cache():
        """Remove all cache files regardless of age"""
        cache_dir = CacheCleaner.get_cache_dir()

        if not cache_dir.exists():
            print(f"Cache directory does not exist: {cache_dir}")
            return 0, 0

        files_removed = 0
        space_freed = 0

        # Get all media files in cache
        media_extensions = ['.webm', '.m4a', '.opus', '.mp3', '.mp4']

        for file_path in cache_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in media_extensions:
                try:
                    file_size = file_path.stat().st_size
                    file_path.unlink()
                    files_removed += 1
                    space_freed += file_size
                    print(f"Removed: {file_path.name}")
                except Exception as e:
                    print(f"Error removing {file_path.name}: {e}")

        space_freed_mb = space_freed / (1024 * 1024)
        print(f"\nAll cache cleared:")
        print(f"  Files removed: {files_removed}")
        print(f"  Space freed: {space_freed_mb:.2f} MB")

        return files_removed, space_freed_mb

    @staticmethod
    def get_cache_info():
        """Get information about cache directory"""
        cache_dir = CacheCleaner.get_cache_dir()

        if not cache_dir.exists():
            print(f"Cache directory does not exist: {cache_dir}")
            return

        total_files = 0
        total_size = 0
        file_types = {}

        for file_path in cache_dir.iterdir():
            if file_path.is_file():
                total_files += 1
                file_size = file_path.stat().st_size
                total_size += file_size

                ext = file_path.suffix.lower()
                if ext not in file_types:
                    file_types[ext] = {'count': 0, 'size': 0}
                file_types[ext]['count'] += 1
                file_types[ext]['size'] += file_size

        total_size_mb = total_size / (1024 * 1024)

        print(f"Cache Directory: {cache_dir}")
        print(f"Total files: {total_files}")
        print(f"Total size: {total_size_mb:.2f} MB")
        print(f"\nBreakdown by type:")
        for ext, info in sorted(file_types.items()):
            size_mb = info['size'] / (1024 * 1024)
            print(f"  {ext}: {info['count']} files, {size_mb:.2f} MB")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == 'clean':
            # Clean cache older than 24 hours (or custom hours)
            hours = 24
            if len(sys.argv) > 2:
                try:
                    hours = int(sys.argv[2])
                except ValueError:
                    print("Invalid hours value, using default (24)")
            CacheCleaner.clean_cache(hours)

        elif command == 'cleanall':
            # Clean all cache
            CacheCleaner.clean_all_cache()

        elif command == 'info':
            # Show cache info
            CacheCleaner.get_cache_info()

        else:
            print("Usage:")
            print("  python -m bin.cache_cleaner info          # Show cache information")
            print("  python -m bin.cache_cleaner clean [hours] # Clean files older than X hours (default: 24)")
            print("  python -m bin.cache_cleaner cleanall      # Clean all cache files")
    else:
        print("Usage:")
        print("  python -m bin.cache_cleaner info          # Show cache information")
        print("  python -m bin.cache_cleaner clean [hours] # Clean files older than X hours (default: 24)")
        print("  python -m bin.cache_cleaner cleanall      # Clean all cache files")
