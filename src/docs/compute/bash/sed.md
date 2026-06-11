# sed

```bash
# Replace first occurrence on each line
sed 's/foo/bar/' file.txt

# Replace all occurrences
sed 's/foo/bar/g' file.txt

# In-place edit
sed -i 's/foo/bar/g' file.txt

# In-place edit with backup
sed -i.bak 's/foo/bar/g' file.txt

# Delete lines matching a pattern
sed '/pattern/d' file.txt

# Delete blank lines
sed '/^$/d' file.txt

# Print only matching lines (like grep)
sed -n '/pattern/p' file.txt

# Print line range
sed -n '10,20p' file.txt

# Insert line before match
sed '/pattern/i\new line' file.txt

# Append line after match
sed '/pattern/a\new line' file.txt

# Multiple expressions
sed -e 's/foo/bar/g' -e 's/baz/qux/g' file.txt

# Replace newlines with \n literal (e.g. for embedding in JSON/YAML)
sed ':a;N;$!ba;s/\n/\\n/g' file.txt

# Reverse: replace \n literal with real newlines
echo "line1\nline2\nline3" | sed 's/\\n/\n/g'
```
