## usage

```shell
# help
python main.py -h
```

### convert pdf to images

It's for saving time, and the pdf is too large (>100 MB), which would be refused by GitHub.

So the file would not be included in this repo on the cloud.

### (core) split problems from an image via pillow

```shell
python main.py split-problems data/images/5.jpg
```

result:

![split-problems-5](.imgs/split-problems-5.png)
