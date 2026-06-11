# Vim

## Modes

| Mode | How to enter | Purpose |
|------|-------------|---------|
| **Normal** | `Esc` | Navigate, run commands |
| **Insert** | `i` / `a` / `o` | Type text |
| **Visual** | `v` / `V` / `Ctrl+v` | Select text |
| **Command** | `:` | Run ex commands |

---

## Quit & save

```
:w          write (save)
:q          quit
:wq         save + quit
:q!         quit without saving
:wqa        save + quit all windows
ZZ          save + quit (normal mode shorthand)
ZQ          quit without saving
```

---

## Navigation (normal mode)

```
h j k l     ← ↓ ↑ →
w / b       next / previous word
e           end of word
0           start of line
^           first non-blank character
$           end of line
gg          first line
G           last line
:42         go to line 42
Ctrl+d      scroll half page down
Ctrl+u      scroll half page up
Ctrl+f / b  page down / up
%           jump to matching bracket
```

---

## Insert mode entry points

```
i           insert before cursor
a           insert after cursor
I           insert at start of line
A           insert at end of line
o           new line below
O           new line above
s           delete char + insert
S           delete line + insert
```

---

## Edit (normal mode)

```
x           delete character under cursor
dd          delete (cut) line
d$          delete to end of line
dw          delete word
D           delete to end of line
yy          yank (copy) line
yw          yank word
p           paste after cursor
P           paste before cursor
u           undo
Ctrl+r      redo
.           repeat last change
r<char>     replace character
~           toggle case
```

---

## Visual mode

```
v           character selection
V           line selection
Ctrl+v      block selection (column mode)

# Once selected:
d           delete
y           yank (copy)
>  /  <     indent / de-indent
~           toggle case
```

---

## Search & replace

```
/pattern        search forward
?pattern        search backward
n / N           next / previous match
*               search word under cursor

# Replace
:s/foo/bar/         replace first on current line
:s/foo/bar/g        replace all on current line
:%s/foo/bar/g       replace all in file
:%s/foo/bar/gc      replace all, confirm each
```

---

## Multiple files & splits

```
:e file         open file
:vs file        vertical split
:sp file        horizontal split
Ctrl+w w        cycle between splits
Ctrl+w h/j/k/l  move between splits
Ctrl+w =        equalize split sizes
:tabnew file    open in new tab
gt / gT         next / previous tab
```

---

## Command mode tips

```
:!<cmd>         run shell command (e.g. :!ls)
:r file         insert file content below cursor
:r !<cmd>       insert command output below cursor
:set number     show line numbers
:set nonumber   hide line numbers
:set paste      disable auto-indent for pasting
:syntax on/off  toggle syntax highlighting
```

---

## Useful `~/.vimrc` defaults

```vim
set number           " line numbers
set relativenumber   " relative line numbers
set tabstop=4
set shiftwidth=4
set expandtab        " spaces instead of tabs
set incsearch        " incremental search
set hlsearch         " highlight search results
set ignorecase
set smartcase
set autoindent
syntax on
```
