from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import os
import time


class XMLHandler(FileSystemEventHandler):

    def __init__(self, callback):
        self.callback = callback
        self.processing = False
        self.last_file = None

    def process(self, path):

        if not path.lower().endswith(".xml"):
            return

        # فایل خروجی دوباره پردازش نشود
        if os.path.basename(path).lower() == "output_clean.xml":
            return

        # اگر همین فایل در حال پردازش است
        if self.processing and self.last_file == path:
            return

        self.processing = True
        self.last_file = path

        threading.Thread(
            target=self.wait_and_process,
            args=(path,),
            daemon=True
        ).start()

    def wait_and_process(self, path):

        # صبر تا فایل کامل نوشته شود
        stable = False
        last_size = -1

        while not stable:

            try:
                size = os.path.getsize(path)

                if size == last_size:
                    stable = True
                else:
                    last_size = size
                    time.sleep(1)

            except Exception:
                time.sleep(1)

        try:
            self.callback()
        finally:
            self.processing = False
            self.last_file = None

    def on_created(self, event):

        if not event.is_directory:
            self.process(event.src_path)

    def on_modified(self, event):

        if not event.is_directory:
            self.process(event.src_path)

    def on_moved(self, event):

        if not event.is_directory:
            self.process(event.dest_path)


class FolderMonitor:

    def __init__(self, folder, callback):

        self.folder = folder
        self.callback = callback
        self.observer = Observer()

    def start(self):

        handler = XMLHandler(self.callback)

        self.observer.schedule(
            handler,
            self.folder,
            recursive=False
        )

        self.observer.start()

    def stop(self):

        if self.observer.is_alive():
            self.observer.stop()
            self.observer.join()