import unittest
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_links,
    split_nodes_images,
    text_to_textnodes,
)
from block_markdown import markdown_to_blocks, block_to_block_type
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_italic_with_bold(self):
        node = TextNode("This is text with **bold** and *italics*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("bold", TextType.TEXT),
                TextNode(" and ", TextType.TEXT),
                TextNode("italics", TextType.ITALIC)
            ],
            new_nodes,
        )

class TestExtractLinkMarkdown(unittest.TestCase):
    def test_links_when_no_link(self):
        text = "This is text with no link"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with no link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_multiple_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            new_nodes,
        )

class TestExtractImageMarkdown(unittest.TestCase):
    def test_links_when_no_image(self):
        text = "This is text with no image"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with no image", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_images(self):
        text = "This is text with an image ![to boot dev](https://www.boot.dev)"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_multiple_images(self):
        text = "This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev")
            ],
            new_nodes,
        )

class TestExtractImageAndLinkMarkdown(unittest.TestCase):
    def test_image_and_link(self):
        text = "This is text with an image ![to boot dev](https://www.boot.dev) and a link [to youtube](https://www.youtube.com/@bootdotdev)"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_images([node])
        new_nodes = split_nodes_links(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                TextNode(" and a link ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            new_nodes,
        )

class TestExtractAll(unittest.TestCase):
    def test_all(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

class TestMarkdownToBlock(unittest.TestCase):
    def test_all(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n\n\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n"
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ],
            blocks
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        markdown = "## This is a headering"
        block_type = block_to_block_type(markdown)
        self.assertEqual("heading", block_type)

    def test_incorrect_heading(self):
        markdown = "##1"
        block_type = block_to_block_type(markdown)
        self.assertEqual("paragraph", block_type)

    def test_code(self):
        markdown = "```This is code ```"
        block_type = block_to_block_type(markdown)
        self.assertEqual("code", block_type)

    def test_empty_code(self):
        markdown = "``````"
        block_type = block_to_block_type(markdown)
        self.assertEqual("code", block_type)

    def test_quotes(self):
        markdown = "> This is a quote\n> and another \n>and another\n>"
        block_type = block_to_block_type(markdown)
        self.assertEqual("quote", block_type)

    def test_unordered_list(self):
        markdown = "* item1 \n- item2\n- item3"
        block_type = block_to_block_type(markdown)
        self.assertEqual("unordered_list", block_type)

    def test_ordered_list(self):
        markdown = "1. item1 \n2. item2\n3. item3"
        block_type = block_to_block_type(markdown)
        self.assertEqual("ordered_list", block_type)
    
    def test_paragraph(self):
        markdown = "1.item1 \n2. item2\n3. item3"
        block_type = block_to_block_type(markdown)
        self.assertEqual("paragraph", block_type)

    def test_paragraph_text(self):
        markdown = "this is just text"
        block_type = block_to_block_type(markdown)
        self.assertEqual("paragraph", block_type)

if __name__ == "__main__":
    unittest.main()
