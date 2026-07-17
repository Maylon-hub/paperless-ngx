import pytest
from documents.utils import format_byte_size, safe_truncate


class TestFormatByteSize:
    def test_bytes(self):
        assert format_byte_size(500) == "500 B"
        assert format_byte_size(0) == "0 B"

    def test_kilobytes(self):
        assert format_byte_size(1024) == "1.0 KB"
        assert format_byte_size(1536) == "1.5 KB"

    def test_megabytes(self):
        assert format_byte_size(1048576) == "1.0 MB"
        assert format_byte_size(1572864) == "1.5 MB"

    def test_gigabytes(self):
        assert format_byte_size(1073741824) == "1.0 GB"

    def test_terabytes(self):
        assert format_byte_size(1099511627776) == "1.0 TB"

    def test_petabytes(self):
        assert format_byte_size(1125899906842624) == "1.0 PB"

    def test_negative_size(self):
        with pytest.raises(ValueError, match="Size cannot be negative"):
            format_byte_size(-1)


class TestSafeTruncate:
    def test_short_string(self):
        text = "short text"
        assert safe_truncate(text, 20) == "short text"
        assert safe_truncate(text, 10) == "short text"

    def test_truncate_with_spaces(self):
        text = "This is a longer string that needs truncation"
        # 20 chars max: "This is a longer str" -> nearest space is after "longer"
        assert safe_truncate(text, 20) == "This is a longer..."

    def test_truncate_without_spaces(self):
        text = "Supercalifragilisticexpialidocious"
        # 10 chars max: "Superca..."
        assert safe_truncate(text, 10) == "Superca..."

    def test_truncate_exact_boundary(self):
        text = "Hello World Test"
        # "Hello World" is 11 chars. Max length 14 -> "Hello World..."
        assert safe_truncate(text, 14) == "Hello World..."

    def test_invalid_max_length(self):
        with pytest.raises(ValueError, match="max_length must be at least 3"):
            safe_truncate("Test", 2)
