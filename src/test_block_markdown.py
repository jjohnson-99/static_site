import unittest

from block_markdown import markdown_to_blocks,block_to_block_type

from textnode import TextNode

class TestBlockMarkdown(unittest.TestCase):
    def test_block_tag(self):
        block = "# This is a heading"
        return True
                

if __name__ == "__main__":
    unittest.main()
