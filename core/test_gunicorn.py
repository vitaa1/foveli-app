"""Regressao da correcao HTTP/1 do Gunicorn 26.2.1, com entradas finitas."""
from types import SimpleNamespace

from django.test import SimpleTestCase
from gunicorn.http.body import ChunkedReader
from gunicorn.http.errors import InvalidChunkSize, LimitRequestHeaders
from gunicorn.http.unreader import IterUnreader


class GunicornParserRegressionTests(SimpleTestCase):
    def test_unterminated_chunk_line_is_bounded(self):
        request = SimpleNamespace(limit_request_field_size=32, max_buffer_headers=64)
        reader = ChunkedReader(request, IterUnreader([b"1;" + b"a" * 40]))
        with self.assertRaises(InvalidChunkSize):
            reader.read(1)

    def test_unterminated_trailers_are_bounded(self):
        request = SimpleNamespace(limit_request_field_size=32, max_buffer_headers=64)
        reader = ChunkedReader(request, IterUnreader([b"0\r\nX: " + b"a" * 70]))
        with self.assertRaises(LimitRequestHeaders):
            reader.read(1)
