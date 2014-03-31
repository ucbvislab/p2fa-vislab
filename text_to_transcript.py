# This is a simple script to turn a a text file of lines or paragraphs
# into a transcript file that can be used for the forced alignment.
# '#' is the comment character in the text files

import sys
import simplejson as json

import jsonschema


def text_to_transcript(text):
    transcript_schema = json.load(
        open("alignment-schemas/transcript_schema.json"))

    paragraphs = text.split("\n\n")
    out = []
    for para in paragraphs:
        para = para.replace("\n", " ")
        if para == "" or para.startswith("#"):
            continue

        line = {
            "speaker": "narrator",
            "line": para
        }
        out.append(line)

    jsonschema.validate(out, transcript_schema)
    return json.dumps(out, indent=4)


if __name__ == "__main__":
    print text_to_transcript(open(sys.argv[1]).read())
