from functools import partial
import gzip
import os

import brotli

from django.contrib.staticfiles.storage import StaticFilesStorage


class PostProcessCompressionStorage(StaticFilesStorage):
    COMPRESS_EXTENSIONS = {"css", "gif", "html", "jpg", "js", "png", "svg", "txt", "webp"}
    COMPRESSION_METHODS = (
        ("gz", partial(gzip.compress, compresslevel=9), gzip.decompress),
        ("br", partial(brotli.compress, quality=11), brotli.decompress),
    )

    def _file_contents_post_process(self, path, cache=None):
        if cache is not None:
            return cache
        with self.open(path, "rb") as file:
            return file.read()

    def post_process(self, paths, **options):
        if options.get("dry_run"):
            return

        for path in paths:
            processed = False
            extension = os.path.splitext(path)[1].removeprefix(".")
            if extension in self.COMPRESS_EXTENSIONS:
                file_contents = None

                for compressed_extension, compress, decompress in self.COMPRESSION_METHODS:
                    compressed_path = f"{path}.{compressed_extension}"
                    should_compress = True

                    # Compare the decompressed contents with existing contents
                    if self.exists(compressed_path):
                        decompressed_contents = decompress(self._file_contents_post_process(compressed_path))
                        file_contents = self._file_contents_post_process(path, cache=file_contents)
                        should_compress = file_contents != decompressed_contents

                    if should_compress:
                        file_contents = self._file_contents_post_process(path, cache=file_contents)

                        with self.open(compressed_path, "wb") as file:
                            file.write(compress(file_contents))

                        processed = True

            yield path, path, processed
