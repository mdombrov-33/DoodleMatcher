class DoodleMatcherException(Exception):
    """Base exception class for DoodleMatcher errors."""

    pass


class UnsplashServiceError(DoodleMatcherException):
    """Exception raised for errors in the Unsplash service."""

    pass


class QdrantServiceError(DoodleMatcherException):
    """Exception raised for errors in the Qdrant service."""

    pass


class ClipServiceError(DoodleMatcherException):
    """Exception raised for errors in the CLIP service."""

    pass


class SearchRequestError(DoodleMatcherException):
    """Exception raised for errors in the search request."""

    pass
