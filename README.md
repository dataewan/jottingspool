Tools for maintaining my markdown notes. Making sure that the notes are linked up correctly.

I've been working with [Zettelkasten](https://zettelkasten.de/posts/zettelkasten-improves-thinking-writing/) for a while, but I don't assume any particular structure.

# Installation

```
python setup.py install
```

# Usage

Check all the `.md` files in the current directory.

```
jottings-pool .
```

Check an individual file

```
jottings-pool <<PATH.md>>
```


## Checks performed

Check the markdown files for two things.

### Check that references aren't missing

If we have this situation where `file1.md` looks like this.

```markdown
# File 1

[reference to file 2](./file2.md)
```

but there is no `file2.md`. Prompt you to see if you want to create that file.

```
./file1.md references missing file ./file2.md create it? (yN)
```

If you choose to create the missing reference, create it and put a note about `TODO` in it.

### Look to see if there are backlinks between the files

If we have this situation:

```markdown
# File 1

[reference to file 2](./file2.md)
```

```markdown
# File 2

No backlink
```

It'll prompt you to let you know that the backlink is missing.

```
./file1.md is referenced by ./file2.md. Should I add the link in at the end of ./file2.md? (yN)
```

If you choose no, then you can choose to ignore in the future.

```
Would you like to ignore this warning in future? (yN)
```

(the links to ignore are held in `.ignore.json`)

If you choose to create the link then it will append it to the end of the file.
