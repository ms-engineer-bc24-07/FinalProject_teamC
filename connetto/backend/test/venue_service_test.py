import unittest
from unittest.mock import patch, Mock
from backend.api.services.venue_service import VenueService

class TestVenueService(unittest.TestCase):

    @patch('requests.get')
    def test_search_izakayas(self, mock_get):
        """
        Test the search_restaurants method for fetching izakaya data.
        """
        # 東京駅の座標 (緯度: 35.681236, 経度: 139.767125)
        midpoint = [35.681236, 139.767125]  
        venue_preference = "居酒屋"  # 居酒屋を指定

        # Mock response from the Hot Pepper API
        mock_response_data = {
            "results": [
                {
                    "name": "居酒屋A",
                    "genre": {"name": "居酒屋"},
                    "address": "東京都千代田区",
                },
                {
                    "name": "居酒屋B",
                    "genre": {"name": "居酒屋"},
                    "address": "東京都千代田区",
                },
                {
                    "name": "居酒屋C",
                    "genre": {"name": "居酒屋"},
                    "address": "東京都千代田区",
                }
            ]
        }

        # Configure mock behavior
        mock_get.return_value = Mock(status_code=200, json=Mock(return_value=mock_response_data))

        # Call the method to test
        result = VenueService.search_restaurants(midpoint, venue_preference)

        # Assert that the results match expectations
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['name'], "居酒屋A")
        self.assertEqual(result[1]['name'], "居酒屋B")
        self.assertEqual(result[2]['name'], "居酒屋C")
        mock_get.assert_called_once()  # Ensure the API call was made once

    @patch('openai.ChatCompletion.create')
    def test_recommend_top_venues(self, mock_openai):
        """
        Test the recommend_top_venues method for recommending top venues.
        """
        # Mock response from OpenAI API
        mock_openai.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "1. 居酒屋A\n2. 居酒屋B\n3. 居酒屋C"
                    }
                }
            ]
        }

        # Venue list to recommend from
        shops = [
            {"name": "居酒屋A", "genre": {"name": "居酒屋"}, "address": "東京都千代田区"},
            {"name": "居酒屋B", "genre": {"name": "居酒屋"}, "address": "東京都千代田区"},
            {"name": "居酒屋C", "genre": {"name": "居酒屋"}, "address": "東京都千代田区"}
        ]

        # Call the method to test
        recommendations = VenueService.recommend_top_venues(shops)

        # Assert that all expected recommendations are included
        self.assertIn("居酒屋A", recommendations)
        self.assertIn("居酒屋B", recommendations)
        self.assertIn("居酒屋C", recommendations)
        mock_openai.assert_called_once()  # Ensure OpenAI API was called once

if __name__ == '__main__':
    unittest.main()
