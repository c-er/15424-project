# Animations

These animations were created using the [manim framework](https://github.com/3b1b/manim) (also
used by 3blue1brown for his youtube videos). The code that generates the animations is in
`code`. The GIFs embedded in the main webpage are located in `gif`. Higher quality versions of these
animations are available as `mp4`s in `hq`.

To generate the animations from the code, you will need to install `manim`, following the
instructions in the link above. Don't use the community version; it doesn't seem to be compatible.
Then, run `manim -l file.py` to quickly generate a lower-quality
`mp4`, or remove the `-l` switch to get a higher quality render that will take longer.