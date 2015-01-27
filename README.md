p2fa-vislab
===========

Fork of [p2fa.](http://www.ling.upenn.edu/phonetics/p2fa/) This python script computes an alignment between a speech audio file and a verbatim text transcript. It also calls on the CMU Sphinx [lmtool](http://www.speech.cs.cmu.edu/tools/lmtool-new.html) to get pronunciations for words that are not in default dictionary (so internet access is required to run the script).

I've made a bunch of changes to the output and input formats, and also to finding pronunciations for words that aren't in the dictionary.

See the original ``readme.txt`` in the repo for more details.

This script was used in my research project: [Content-Based Tools for Editing Audio Stories](http://vis.berkeley.edu/papers/audiostories) [UIST 2013]. 

Setup
-----


### Install HTK 3.4. Note: 3.4.1 *will not work*. [Get HTK here.](http://htk.eng.cam.ac.uk/)

On OSX this can be a pain. Here's one method that works:

`./configure --without-x --disable-hslab CFLAGS='-I/usr/include/malloc'`

Then edit `HTKLib/esignal.c` and replace every occurence of `ARCH` with `"darwin"`.

Then run `make all && sudo make install`

### Install python dependencies:

``pip install -r requirements.txt``


### Install sox

On OSX, with homebrew:

``brew install sox``

### Initialize submodules

In the p2fa-vislab directory, run:

``git submodule init``

and

``git submodule update``

Usage
-----

``python align.py audio_file.wav transcript_input.json aligned_output.json``

The input ``audio_file.wav`` must be 16 bit and mono.

### Transcript format

The input transcript json must have the following [jsonschema](http://json-schema.org): 

```json
{
    "title": "Transcript Schema",
    "description": "A transcript of an audio file",
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "array",
    "items": {
        "title": "Line",
        "type": "object",
        "description": "An individual line or paragraph of the transcript",
        "properties": {
            "speaker": {
                "description": "Speaker of the line or paragraph",
                "type": "string"
            },
            "line": {
                "description": "Text of the line or paragraph",
                "type": "string"
            }
        },
        "required": ["line", "speaker"]
    }
}
```

For example:

```json
[
  {
    "speaker": "Steve",
    "line": "Hi, my name is Steve."
  },
  {
    "speaker": "Steve",
    "line": "What's your name?"
  }
]
```

(Although, there's no reason to list those two lines separately because they're the same speaker.) To convert a plain text transcript into a file that adheres to this schema, see [text\_to\_transcript.py](text_to_transcript.py).

### Alignment format

The output will be a json with the following jsonschema:

```json
{
    "title": "Alignment Schema",
    "description": "A alignment of a transcript to an audio file",
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "additionalProperties": true,
    "properties": {
        "words": {
            "type": "array",
            "items": {
                "title": "Word",
                "type": "object",
                "description": "An individual aligned word of the transcript and audio file",
                "properties": {
                    "word": {
                        "description": "Original word",
                        "type": "string"
                    },
                    "alignedWord": {
                        "description": "Word processed by the alignment algorithm",
                        "type": "string"
                    },
                    "start": {
                        "description": "Start time of the aligned word, in seconds",
                        "type": "number"
                    },
                    "end": {
                        "description": "End time of the aligned word, in seconds",
                        "type": "number"
                    },
                    "speaker": {
                        "description": "Speaker of the word",
                        "type": "string"
                    },
                    "line_idx": {
                        "description": "Index of input line that word came from",
                        "type": "integer"
                    }
                },
                "required": ["word", "alignedWord", "start", "end"]
            }
        }
    }
}
```

TextGrid output
---------------

You can also specifiy `--textgrid`  and `--no-json` on the command
line to get the output of the script as a Praat TextGrid file instead
of in the json format.
