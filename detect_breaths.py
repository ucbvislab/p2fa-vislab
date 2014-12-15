try:
    import simplejson as json
except:
    import json
import os
import re
import subprocess

import click
from radiotool.composer import Speech, Segment, Composition

from align import do_alignment

ac_re = re.compile(r"\[Ac=(-?\d+)")

def alignment_with_breaths(speech_file, alignment_file, out_alignment_file=None):
    pause_idx = 0
    subprocess.call('rm tmpaudio/*.wav', shell=True)

    with open(alignment_file, 'r') as af:
        alignment = json.load(af)["words"]

    new_alignment = []
    for x in alignment:
        if x["alignedWord"] == "sp":
            comp = Composition(channels=1)
            speech = Speech(speech_file, "p")
            comp.add_track(speech)
            start = x["start"]
            end = x["end"]
            # ignore super-short pauses
            if end - start <= .05:
                new_alignment.append(x)
                pause_idx += 1
                continue
            # print "pause", pause_idx-1, "start:", start, "end", end
            # print "len", end - start
            print "Creating pause", start, end - start
            seg = Segment(speech, 0.0, start, end - start)
            comp.add_segment(seg)
            comp.export(
                adjust_dynamics=False,
                filename="tmpaudio/p%06d" % pause_idx,
                channels=1,
                filetype='wav',
                samplerate=speech.samplerate,
                separate_tracks=False)
            print "# classifying p%06d.wav" % pause_idx
            print "# segment length:", x["end"] - x["start"]
            
            cls = classify_htk(
                'tmpaudio/p%06d.wav' % pause_idx)
            
            # cls = breath_classifier.classify(
            #     'tmp/pauses/p%06d.wav' % pause_idx)

            for word in cls:
                word["start"] = round(word["start"] + x["start"], 5)
                word["end"] = round(word["end"] + x["start"], 5)
            cls[-1]["end"] = x["end"]
            new_alignment.extend(cls)
            pause_idx += 1
        else:
            new_alignment.append(x)


    if out_alignment_file is None:
        out_alignment_file = os.path.splitext(alignment_file)[0] + "-breaths.json"

    with open(out_alignment_file, 'w') as new_af:
        json.dump({"words": new_alignment}, new_af, indent=4)

    return 0


def classify_htk(audio_file):
    MIN_BREATH_DUR = 0.1
    MIN_AC = 500

    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    
    transcript = "breath.transcript"
    output = "breath-classify-output.json"
    results = "tmp/aligned.results"

    with open(transcript, 'w') as f:
        f.write("""[{"speaker": "speaker", "line": "{BR}"}]""")

    do_alignment(audio_file, transcript, output, json=True, textgrid=False)

    os.remove(transcript)

    # subprocess.call('python ../p2fa/align.py ../%s %s %s' %
    #     (audio_file, transcript, output), shell=True)
    
    final_words = [{
        "start": 0.0,
        "end": 0.0,
        "alignedWord": "sp",
        "word": "{p}"
    }]
    
    with open(results, 'r') as res:
        match = ac_re.search(res.read())
        if match:
            ac = int(match.group(1))
            print "Ac:", ac
            if ac > MIN_AC:
                print "Breath!"
    
                with open(output, 'r') as out:
                    words = json.load(out)["words"]
                    breath = filter(
                        lambda x: x["alignedWord"] == "{BR}",
                        words)[0]
                    breath_dur = breath["end"] - breath["start"]
                    print "breath len", breath_dur
                    if breath_dur > MIN_BREATH_DUR:
                        final_words = words
                        final_words[0]["start"] = 0.0
                        for word in final_words:
                            if word["alignedWord"] == "{BR}":
                                word["likelihood"] = ac

    os.chdir(cwd)

    return final_words


@click.command()
@click.argument("wavfile")
@click.argument("alignment_json")
def do_detect_breaths(wavfile, alignment_json):
    return alignment_with_breaths(wavfile, alignment_json)


if __name__ == '__main__':
    do_detect_breaths()