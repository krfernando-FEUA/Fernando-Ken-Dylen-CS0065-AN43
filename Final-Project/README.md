# LoopGuard: Friendship Fair

**CS0065 - AN43 | Intelligent Systems Final Project**

A Python, Streamlit, and KNIME expert system for a fictional Sanrio-themed
virtual economy. Written rules help a designer decide whether a profitable
exchange route should be corrected, preserved as an intentional reward, or
investigated for missing information.

Presenters: Ken, Maersk, Rey, Alvin, and Nads.

## Files

| Directory | Contents |
| --- | --- |
| [docs](docs) | Project design, demonstration guide, verification record, asset credits, speaking script, and PowerPoint |
| [knime](knime) | Importable workflow, unpacked node settings, baseline data, helper scripts, and execution evidence |
| [video](video) | Final 1920 × 1080 subtitled video and separate English subtitles |
| [python](python) | Complete Python source ZIP and setup instructions |

- [PowerPoint presentation](docs/LoopGuard-Friendship-Fair.pptx)
- [English speaking script](docs/LoopGuard-English-Script.md)
- [KNIME workflow](knime/LoopGuard_Friendship_Fair.knwf)
- [Python source ZIP](python/LoopGuard-Python-Source.zip)
- [Final subtitled video](https://media.githubusercontent.com/media/krfernando-FEUA/Fernando-Ken-Dylen-CS0065-AN43/main/Final-Project/video/LoopGuard-OneCut-1080p-Subtitled.mp4)
- [English subtitles](video/LoopGuard-Subtitles-English.srt)

## Run the system

Extract the [Python ZIP](python/LoopGuard-Python-Source.zip), open its
`loopguard-python` folder, and follow its README or the [setup guide](python/README.md).
Import `knime/LoopGuard_Friendship_Fair.knwf` in KNIME Analytics Platform to run
the supplied baseline. [KNIME instructions](knime/README.md) explain how to execute
its four nodes and compare the result with Python. Run the helper scripts from
the extracted Python project so their imports resolve.

## Presentation files

The video is exactly **8 minutes 20 seconds**, at **1920 × 1080 and 30 fps**, with
English subtitles included in the picture. The `.srt` is supplied separately for
reuse. The PowerPoint and Markdown script retain the full presentation and
optional appendix. The PDF script is excluded from this submission.

The MP4 is stored with Git LFS. GitHub's **Download raw file** action or the video
link above retrieves it. When cloning, install Git LFS and run `git lfs pull` to
download the video content.

## Verification

[The original verification record](docs/VERIFICATION.md) documents the 25 October
Python test run. The later native KNIME baseline execution is documented in
[KNIME instructions](knime/README.md) and [execution evidence](knime/evidence).
Python comments and docstrings were removed from this submission's source files;
runtime CLI help text and documentation were retained. After cleanup, **116 tests and 21 subtests passed**. Syntax, CLI help, and
archive integrity checks also passed.

[MANIFEST.json](MANIFEST.json) records file sizes and SHA-256 checksums for this
submission. Character artwork credits are in [ASSETS.md](docs/ASSETS.md).
