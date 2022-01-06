from functools import partial
import gzip
import os

import brotli

from django.contrib.staticfiles.storage import StaticFilesStorage


class PostProcessCompressionStorage(StaticFilesStorage):
    COMPRESS_EXTENSIONS = {"css", "gif", "html", "jpg", "js", "png", "svg", "txt", "webp"}
    COMPRESS_METHODS = (
        ("gz", partial(gzip.compress, compresslevel=9)),
        ("br", partial(brotli.compress, quality=11)),
    )

    def post_process(self, paths, dry_run=False, **options):
        if dry_run:
            return

        for path in paths:
            processed = False
            ext = os.path.splitext(path)[1][1:]  # strip '.'
            if ext in self.COMPRESS_EXTENSIONS:
                contents = None
                modified = self.get_modified_time(path)

                for compressed_ext, compress_func in self.COMPRESS_METHODS:
                    compressed_path = f"{path}.{compressed_ext}"
                    if not self.exists(compressed_path) or modified >= self.get_modified_time(compressed_path):
                        if contents is None:
                            with self.open(path, "rb") as file:
                                contents = file.read()

                        with self.open(compressed_path, "wb") as file:
                            file.write(compress_func(contents))

                        processed = True

            yield path, path, processed
