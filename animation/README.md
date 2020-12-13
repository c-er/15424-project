# Animations

These animations were created using the [manim framework](https://github.com/3b1b/manim) (also
used by 3blue1brown for his youtube videos). The code that generates the animations is in
`code`. High quality (1440p, 60fps) renders of the animations are available in `mp4` format under
`hq`. The GIFs embedded in the main webpage were sampled from these animations at 600x338, 30fps,
and are located in `gif`.

To generate the animations from the code, you will need to install `manim`, following the
instructions in the link above. Don't use the community version; it doesn't seem to be compatible.
Then, run `manim -l file.py` to quickly generate a lower-quality
`mp4`, or remove the `-l` switch to get a higher quality render that will take longer.