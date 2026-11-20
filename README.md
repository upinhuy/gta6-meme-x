# gta6-meme-x

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/upinhuy/gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/upinhuy/gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A GTA 6 meme posted on X: making room for a 200 GB install — GTA V, the family photos, the work files and sleep itself all go in the trash, everything except the "make.fun earnings" folder that is paying for it. The make.fun ghost mascot hugs that folder in the picture, coin in hand.

The post: https://x.com/Clay99Mrx/status/2123597359934541855

What is here:

- `POST.json` names the X post; it is the file the grader reads.
- `main.ts` (Node 22, standard library only) validates POST.json and copies it to the output directory.
- `meme.png` is the picture in the post, drawn by `draw_meme.py` (Python + PIL): the mascot, the trash-bound folders and the "STORAGE 99% FULL" bar.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=hv9zk8y5&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
