# Audio

`assets/audio/wedding.mp3` — 58 seconds, mono, 128 kbps, 910 KB. It loops,
and the control on the page only appears once this file is present.

## What is playing

**An original piece, written for this page.** Not a licensed track, and not
a cover.

You asked for *All of Me* instrumental by the route that costs nothing, and
that route does not exist for that song. Two separate rights sit on it: the
**master** (a specific recording) and the **composition** (the song itself).
A cover clears the master but not the composition — putting it on a public
page still needs a sync licence for the writing. That licence is precisely
what the paid services sell, which is why the free instrumental covers
circulating online are, almost without exception, unlicensed.

So this was written from scratch instead. It owes nothing to anyone: a
I–vi–IV–V movement in F, which is the common property of most of Western
music, under a rocking eighth-note arpeggio at 66 bpm. There is deliberately
no melody over it — a tune competes with reading, an arpeggio sits
underneath it.

`tools/compose.py` renders it and is worth reading if you want to change it.
The piano is additive: twelve partials per note, the higher ones decaying
faster, with a little inharmonicity so the overtones run slightly sharp of
true. That last imperfection is most of what separates a piano from an
organ. The room is a convolution reverb built from decaying noise.

The loop is seamless because the reverb tail from the final bar is folded
back over the opening.

**Nobody has heard it.** It was written and rendered without anyone
listening — the levels, the harmony and the timing were verified by
measurement, not by ear. Play it before you keep it.

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
