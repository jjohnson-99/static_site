
def markdown_to_blocks(markdown):
    return [section.strip() for section in markdown.split("\n\n") if section != '']

def block_to_block_type(markdown_block):
    max_num_headers = 6
    headings = ['#'*i + ' ' for i in range(1,max_num_headers+1)]
    for i in range(1, min(max_num_headers+1, len(markdown_block)+1)):
        if markdown_block[0:i] in headings:
            return "heading"

    if len(markdown_block) >= 6 and markdown_block[0:3] == '```' and markdown_block[-3:] == '```':
        return "code"
    
    lines = markdown_block.split('\n')
    if all([line[0] == '>' for line in lines]):
        return "quote"
    if len(markdown_block) > 1 and all([line[0:2] in ['* ', '- '] for line in lines]):
        return "unordered_list"
    if len(markdown_block) > 2 and all([line[0:3] in [f'{i+1}. '] for (i, line) in enumerate(lines)]):
        return "ordered_list"
    else:
        return "paragraph"
