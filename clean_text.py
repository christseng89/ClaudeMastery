#!/usr/bin/env python3
"""Clean ridiculous character patterns from text file."""

import re

def cleanText(inputFile, outputFile):
    """Remove garbage character patterns from the text."""

    with open(inputFile, 'r', encoding='utf-8') as f:
        content = f.read()

    # Multiple patterns to catch different types of garbage

    # Pattern 1: Sequences with special chars and mixed alphanumeric
    pattern1 = r'[#\$%\^\&\*\(\)\[\]\{\}\/\\|@~`][^。，！？\u4e00-\u9fff\n]*[a-zA-Z0-9#\$%\^\&\*\(\)\[\]\{\}\/\\|@~`][^。，！？\u4e00-\u9fff\n]*'

    # Pattern 2: Sequences at end of lines with numbers, letters, special chars (but not Chinese punctuation)
    # Like: "2 E; ?8 Q7 d" or "1 V+ y5 v; f5 R1" or "; H2 e" or "4 l"
    pattern2 = r'[0-9;:\.\s][0-9a-zA-Z\s;:_\+\-\!\?\$%\^\&\*\(\)\[\]\{\}\/\\|@~`,\.<>\'\"]{1,}[0-9a-zA-Z][^。，！？\u4e00-\u9fff\n]*(?=\n|$)'

    # Pattern 3: Single trailing digits or short garbage at line ends
    pattern3 = r'(?<=[。！？\u4e00-\u9fff])[0-9\s]{1,3}[a-zA-Z0-9\s;:_\+\-\!\?\$%\^\&\*\(\)\[\]\{\}\/\\|@~`,\.<>\'\"]+(?=\n|$)'

    # Pattern 4: Sequences like ". V" or "; L2" at line ends
    pattern4 = r'[\.;:,\!]\s*[A-Z0-9][^。，！？\u4e00-\u9fff\n]{0,30}(?=\n|$)'

    # Apply all patterns
    cleanedContent = content
    for pattern in [pattern1, pattern2, pattern3, pattern4]:
        cleanedContent = re.sub(pattern, '', cleanedContent)

    # Remove excessive spaces (more than 2 consecutive spaces)
    cleanedContent = re.sub(r' {3,}', ' ', cleanedContent)

    # Remove trailing spaces at end of lines
    cleanedContent = re.sub(r' +\n', '\n', cleanedContent)

    # Write cleaned content
    with open(outputFile, 'w', encoding='utf-8') as f:
        f.write(cleanedContent)

    print(f"✓ Cleaned text saved to: {outputFile}")

    # Show statistics
    originalLines = content.count('\n')
    cleanedLines = cleanedContent.count('\n')
    removedChars = len(content) - len(cleanedContent)

    print(f"  Original size: {len(content)} characters")
    print(f"  Cleaned size: {len(cleanedContent)} characters")
    print(f"  Removed: {removedChars} characters ({removedChars/len(content)*100:.1f}%)")

if __name__ == "__main__":
    inputFile = "test.txt"
    outputFile = "test_cleaned.txt"

    cleanText(inputFile, outputFile)
