from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from app.models import (
    MediaTypes,
    Sources,
)


class MediaSearchViewTests(TestCase):
    """Test the media search view."""

    def setUp(self):
        """Create a user and log in."""
        self.credentials = {"username": "test", "password": "12345"}
        self.user = get_user_model().objects.create_user(**self.credentials)
        self.client.login(**self.credentials)

    def test_media_search_view(self):
        """Test the media search page view (initial page load)."""
        response = self.client.get(
            reverse("search") + "?media_type=movie&q=test",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/search.html")

        self.user.refresh_from_db()
        self.assertEqual(self.user.last_search_type, MediaTypes.MOVIE.value)

        # Check context has the search parameters
        self.assertEqual(response.context["media_type"], MediaTypes.MOVIE.value)
        self.assertEqual(response.context["query"], "test")

    @patch("app.providers.services.search")
    def test_media_search_results_view(self, mock_search):
        """Test the media search results HTMX endpoint."""
        mock_search.return_value = {
            "page": 1,
            "total_results": 1,
            "total_pages": 1,
            "results": [
                {
                    "media_id": "238",
                    "title": "Test Movie",
                    "media_type": MediaTypes.MOVIE.value,
                    "source": Sources.TMDB.value,
                    "image": "http://example.com/image.jpg",
                },
            ],
        }

        response = self.client.get(
            reverse("search_results") + "?media_type=movie&q=test&page=1&source=tmdb",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/components/search_grid_items.html")

        mock_search.assert_called_once_with(
            MediaTypes.MOVIE.value,
            "test",
            1,
            Sources.TMDB.value,
        )
