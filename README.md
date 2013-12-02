p2fa-steve
==========

Fork of [p2fa.](http://www.ling.upenn.edu/phonetics/p2fa/) This python script computes an alignment between a speech audio file and a verbatim text transcript. It also calls on the CMU Sphinx [lmtool](http://www.speech.cs.cmu.edu/tools/lmtool-new.html) to get pronunciations for words that are not in default dictionary (so internet access is required to run the script).

I've made a bunch of changes to the output and input formats, and also to finding pronunciations for words that aren't in the dictionary.

See the original ``readme.txt`` in the repo for more details.

This script was used in my research project: [Content-Based Tools for Editing Audio Stories](http://vis.berkeley.edu/papers/audiostories) [UIST 2013]. 

Setup
-----

Install HTK 3.4. Note: 3.4.1 *will not work*. [Get HTK here.](http://htk.eng.cam.ac.uk/)

Install python dependencies:

``pip install -r requirements.txt``


Usage
-----

``python align.py audio_file.wav transcript_input.json aligned_output.json``

The input ``audio_file.wav`` must have a samplerate of 16 Khz.

The input transcript json must have the following format: 

```
TRANSCRIPT = [LINE+]
LINE = { "speaker": NAME_OF_SPEAKER, "line": TRANSCRIPT_LINE }
NAME_OF_SPEAKER = string
TRANSCRIPT_LINE = string
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

(Although, there's no reason to list those two lines separately because they're the same speaker.)

The output will be a json with the following format:

```
ALIGNMENT = [WORD+]
WORD = { "word": ORIGINAL_WORD, 
         "alignedWord": WORD_PROCESSED_BY_SYSTEM,
         "start": TIME,
         "end": TIME,
         "speaker": NAME_OF_SPEAKER,
         "line_idx": LINE_IDX }
ORIGINAL_WORD = string
WORD_PROCESSED_BY_SYSTEM = string (all caps, sanitized)
TIME = Number (in seconds)
NAME_OF_SPEAKER = string
LINE_IDX = Integer (index of input line that word came from)
```
