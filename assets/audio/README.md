# Audio

The page looks for **`assets/audio/wedding.mp3`**. Drop the file in with that
name and the control appears by itself — no code change needed. Until then the
button stays hidden and the page is silent.

## The recommendation

**"Turning Page" (Instrumental) — Sleeping At Last.**

Piano and strings, no drums, patient. It matches what this page is doing:
restrained, unhurried, one thing at a time. The instrumental version matters
because the track loops — vocals coming round again every ninety seconds get
noticed, and instrumental doesn't. It is also a very common first-dance and
ceremony choice, so it will feel familiar without being obvious.

Two alternatives if that one isn't right:

| Track | Why |
|---|---|
| *I Get to Love You* — Ruelle | Warmer and more cinematic. Vocal, so trim to an instrumental passage. |
| *Can't Help Falling in Love* — Kina Grannis | The stripped version. The most familiar option here; safe rather than distinctive. |

## What I could not do

I cannot fetch the recording — there's no source I can legitimately pull from,
and it's a licensed master either way. Getting the file is the one step that
has to be yours.

The page is served publicly, so the recording needs to be one you may publish
there. Buying the track is not a licence. The cleaner routes are a micro-sync
licence through the publisher, a clearing service that covers popular music
online, or a royalty-free cover — for an instrumental piano piece a cover
carries the whole feeling without touching the master.

In practice most personal wedding pages simply use the track. That is your
call to make, not mine.

## Trimming

Sixty to ninety seconds, mono, 128 kbps. It loops, so nobody hears the end,
and a four-megabyte file is four megabytes every guest pays for.

Pick a passage that loops without a seam — end it where the phrase resolves,
not mid-bar. Fade the last second to nothing and the join stops being audible.

```
ffmpeg -i source.mp3 -ss 00:00:24 -t 00:01:15 \
       -af "afade=t=in:st=0:d=2,afade=t=out:st=73:d=2" \
       -ac 1 -b:a 128k assets/audio/wedding.mp3
```

The volume is set in `wedding.js` (`TRACK.volume`, currently 0.45) and ramps
up rather than cutting in.
