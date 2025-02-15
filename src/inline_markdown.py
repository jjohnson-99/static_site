from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    alt_text = re.findall(r"!\[(.*?)\]", text)
    url = re.findall(r"\((.*?)\)", text)
    return list(zip(alt_text, url))

def extract_markdown_links(text):
    alt_text = re.findall(r"\[(.*?)\]", text)
    url = re.findall(r"\((.*?)\)", text)
    return list(zip(alt_text,url))

def split_nodes_links(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        link_text_url = extract_markdown_links(old_node.text)
        split_nodes = []
        sections = re.split(r"\[.*?\]\(.*?\)", old_node.text)
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            else:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            if i < len(link_text_url):
                split_nodes.append(TextNode(link_text_url[i][0], TextType.LINK, link_text_url[i][1]))
        new_nodes.extend(split_nodes) 
    return new_nodes

def split_nodes_images(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
 
        image_text_url = extract_markdown_images(old_node.text)
        split_nodes = []
        sections = re.split(r"!\[.*?\]\(.*?\)", old_node.text)
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            else:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            if i < len(image_text_url):
                split_nodes.append(TextNode(image_text_url[i][0], TextType.IMAGE, image_text_url[i][1]))
        new_nodes.extend(split_nodes) 
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '*', TextType.ITALIC)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes

def markdown_to_blocks(markdown):
    return [section.strip() for section in markdown.split('\n\n') if section != '']
