from textnode import TextNode, TextType

def main():
    node = TextNode("this is text", TextType.BOLD, "https://www.boo.dev")
    print(node)
main()
