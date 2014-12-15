# This is a simple script to turn a a text file of lines or paragraphs
# into a transcript file that can be used for the forced alignment.
# '#' is the comment character in the text files

import sys
import simplejson as json
import os.path

import click
import jsonschema


@click.command()
@click.argument('text_file')
@click.option('--output-file', default=None, help="Output transcript file")
@click.option('--speaker-name', default="Narrator", help="The name of the speaker")
def text_to_transcript(text_file, output_file, speaker_name):
    text = open(text_file).read()

    filedir = os.path.dirname(os.path.realpath(__file__))
    schema_path = os.path.join(
        filedir, "alignment-schemas/transcript_schema.json")

    transcript_schema = json.load(open(schema_path))

    paragraphs = text.split("\n\n")
    out = []
    for para in paragraphs:
        para = para.replace("\n", " ")
        if para == "" or para.startswith("#"):
            continue

        line = {
            "speaker": speaker_name,
            "line": para
        }
        out.append(line)

    jsonschema.validate(out, transcript_schema)
    if output_file is None:
        print json.dumps(out, indent=4)
    else:
        with open(output_file, 'w') as f:
            f.write(json.dumps(out, indent=4))
    return

if __name__ == "__main__":
    text_to_transcript()
