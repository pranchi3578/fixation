# Audio

`assets/audio/wedding.mp3` — 60 seconds, mono, 128 kbps, 941 KB. It loops,
and the control on the page only appears once this file is present.

## What is playing

A lo-fi instrumental cover of **"I Do" — 911**, supplied by you and trimmed
here to a loop.

`tools/trim_track.py` did the trimming, and it is worth knowing what it does
rather than a plain cut. A page loop is not a fade-out: it comes round every
minute and any seam gets noticed on the third pass. So the script reads the
tempo off the onset envelope (95.7 BPM here, a 2.51-second bar), waits for
the track to settle rather than starting in the intro, cuts a whole number
of bars, and then folds the tail back over the head with equal-power curves.
The join is a continuous mix rather than a cut, which is why there is no
audible seam and no fade.

What shipped: enters at 50.2s of the source, 24 bars, 60.2 seconds, mono at
128 kbps, 941 KB. The first pass came out at 33 bars and 1.3 MB, which is a
lot to ask of a guest on mobile data for background music, so it was pulled
back to a minute.

**Nobody here has heard it.** Levels, tempo, loop seam and playback were all
verified by measurement. Play it before you keep it.

## Re-trimming

```
python3 tools/trim_track.py <source.mp3> [seconds]
```

The original composed piece is still reproducible with `tools/compose.py`
if you ever want to go back to something with no rights attached.

## Changing it

```
python3 tools/compose.py        # re-render after editing
```

Tempo, key and the chord sequence are constants at the top. The volume the
page plays it at is `TRACK.volume` in `wedding.js`, currently 0.45, and it
ramps up rather than cutting in.

## Replacing it

Drop any mp3 in at this path and it takes over — no code change. If you do
license *All of Me*, trim it to sixty or ninety seconds, mono, 128 kbps:

```
ffmpeg -i source.mp3 -ss 00:00:24 -t 00:01:15 \
       -af "afade=t=in:st=0:d=2,afade=t=out:st=73:d=2" \
       -ac 1 -b:a 128k assets/audio/wedding.mp3
```

End the excerpt where the phrase resolves rather than mid-bar, or the loop
join will be audible.
