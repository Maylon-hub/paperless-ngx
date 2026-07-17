from unittest import mock

import pytest
from django.core.exceptions import ValidationError

from documents.validators import uri_validator
from documents.validators import url_validator


class TestValidators:
    def test_uri_validator_valid(self) -> None:
        uri_validator("http://example.com")
        uri_validator("https://example.com/path")
        uri_validator("ftp://example.com", allowed_schemes={"ftp", "http"})

    def test_uri_validator_missing_scheme(self) -> None:
        with pytest.raises(ValidationError, match="missing scheme"):
            uri_validator("example.com")

    def test_uri_validator_missing_netloc_and_path(self) -> None:
        with pytest.raises(ValidationError, match="missing net location or path"):
            uri_validator("http://")

    def test_uri_validator_not_allowed_scheme(self) -> None:
        with pytest.raises(ValidationError, match="scheme 'ftp' is not allowed"):
            uri_validator("ftp://example.com", allowed_schemes={"http", "https"})

    def test_url_validator_valid(self) -> None:
        url_validator("http://example.com")
        url_validator("https://example.com")

    def test_url_validator_invalid_scheme(self) -> None:
        with pytest.raises(ValidationError, match="scheme 'ftp' is not allowed"):
            url_validator("ftp://example.com")

    @mock.patch("documents.validators.urlparse")
    def test_uri_validator_general_exception(
        self,
        mock_urlparse: mock.MagicMock,
    ) -> None:
        # Mock urlparse to raise an arbitrary exception to test the catch-all block
        mock_urlparse.side_effect = Exception("Test exception")
        with pytest.raises(
            ValidationError,
            match=r"Unable to parse URI http://example\.com",
        ):
            uri_validator("http://example.com")
