import unittest
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../src/upload-worker")
    )
)

from src.core.upload_documents import upload_documents_workflow

# set any env varaibles up...
# os.environ["API_KEY"] = "xyz"


class TestCore(unittest.TestCase):
    """Test core functions."""

    def test_placeholder(self):
        """Test placeholder."""
        self.assertIsNotNone({})


if __name__ == "__main__":
    unittest.main()
