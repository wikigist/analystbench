from unittest.mock import patch, Mock

from rag.generation import generate_text


def test_generate_text_returns_stripped_response():
    with patch("rag.generation.OpenAI") as mock_openai:

        mock_client = mock_openai.return_value

        mock_response = Mock()
        mock_response.output_text = "  Refunds within 30 days.  "

        mock_client.responses.create.return_value = mock_response

        result = generate_text("What is the refund period?")

        assert result == "Refunds within 30 days."


def test_generate_text_passes_correct_api_arguments():
    with patch("rag.generation.OpenAI") as mock_openai:
        mock_client = mock_openai.return_value

        mock_response = Mock()
        mock_response.output_text = "Test answer."

        mock_client.responses.create.return_value = mock_response

        generate_text("Test question", model="test-model")

        mock_client.responses.create.assert_called_once_with(
            model="test-model",
            input="Test question",
            max_output_tokens=400,
            store=False
        )