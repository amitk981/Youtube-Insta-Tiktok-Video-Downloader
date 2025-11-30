import os
import typing
import time
import asyncio

class ProgressFileReader(typing.BinaryIO):
    def __init__(self, path: str, progress_callback: typing.Callable[[int, int], typing.Awaitable[None]]):
        self.file = open(path, 'rb')
        self.total_size = os.path.getsize(path)
        self.bytes_read = 0
        self.progress_callback = progress_callback
        self.last_update_time = 0

    def read(self, size: int = -1) -> bytes:
        chunk = self.file.read(size)
        self.bytes_read += len(chunk)
        
        # Trigger callback (non-blocking)
        current_time = time.time()
        if current_time - self.last_update_time > 3 or self.bytes_read == self.total_size:
            self.last_update_time = current_time
            try:
                # We can't await here easily because read is sync.
                # But we can schedule a task on the running loop.
                loop = asyncio.get_running_loop()
                if loop.is_running():
                    loop.create_task(self.progress_callback(self.bytes_read, self.total_size))
            except RuntimeError:
                pass
                
        return chunk

    def close(self):
        self.file.close()

    # Proxy other methods
    def seek(self, offset, whence=0): return self.file.seek(offset, whence)
    def tell(self): return self.file.tell()
    def fileno(self): return self.file.fileno()
    def flush(self): return self.file.flush()
    def isatty(self): return self.file.isatty()
    def readable(self): return self.file.readable()
    def readline(self, size=-1): return self.file.readline(size)
    def readlines(self, hint=-1): return self.file.readlines(hint)
    def seekable(self): return self.file.seekable()
    def truncate(self, size=None): return self.file.truncate(size)
    def writable(self): return self.file.writable()
    def write(self, b): return self.file.write(b)
    def writelines(self, lines): return self.file.writelines(lines)
    def __enter__(self): return self
    def __exit__(self, *args): self.close()
