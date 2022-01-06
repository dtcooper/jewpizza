from functools import partial
import gzip
import os

from django.contrib.staticfiles.storage import StaticFilesStorage
from django.contrib.staticfiles.management.commands import collectstatic

import brotli


class PostProcessCompressionStorage(StaticFilesStorage):
    COMPRESS_EXTENSIONS = {'css', 'gif', 'html', 'jpg', 'js', 'png', 'svg', 'txt', 'webp'}
    COMPRESSION_METHODS = (
        ('gz', partial(gzip.compress, compresslevel=9), gzip.decompress),
        ('br', partial(brotli.compress, quality=11), brotli.decompress),
    )

    def post_process(self, paths, **options):
        if options.get('dry_run'):
            return

        for path in paths:
            processed = False
            extension = os.path.splitext(path)[1].removeprefix('.')
            if extension in self.COMPRESS_EXTENSIONS:
                contents = None

                for compressed_extension, compress, decompress in self.COMPRESSION_METHODS:
                    compressed_path = f'{path}.{compressed_extension}'
                    should_compress = True

                    # Compare the decompressed contents with existing contents
                    if self.exists(compressed_path):
                        with self.open(compressed_path, 'rb') as file:
                            decompressed_contents = decompress(file.read())
                        if contents is None:  # Cached
                            with self.open(path, 'rb') as file:
                                contents = file.read()
                        should_compress = (contents != decompressed_contents)

                    if should_compress:
                        if contents is None:  # Cached
                            with self.open(path, 'rb') as file:
                                contents = file.read()

                        with self.open(compressed_path, 'wb') as file:
                            file.write(compress(contents))

                        processed = True

            yield path, path, processed
