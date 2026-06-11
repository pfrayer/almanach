# awk

```bash
# Print a specific column (field separator is whitespace by default)
awk '{print $1}' file.txt
awk '{print $1, $3}' file.txt

# Custom field separator
awk -F: '{print $1}' /etc/passwd        # colon-separated
awk -F, '{print $2}' file.csv

# Filter lines (like grep)
awk '/pattern/ {print}' file.txt
awk '$3 > 100 {print $1, $3}' file.txt

# Count lines matching a pattern
awk '/ERROR/ {count++} END {print count}' app.log

# Sum a column
awk '{sum += $5} END {print sum}' file.txt

# Print with custom format
awk '{printf "%-20s %s\n", $1, $2}' file.txt

# BEGIN / END blocks
awk 'BEGIN {print "start"} {print $0} END {print "end"}' file.txt

# NR (line number), NF (number of fields)
awk 'NR==5 {print}'         # print line 5
awk 'NF > 3 {print}'        # lines with more than 3 fields
awk 'END {print NR}' file   # count total lines

# Print lines between two patterns
awk '/START/,/END/ {print}' file.txt

# Extract and count unique IPs (Apache logs)
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head 20

# Count HTTP status codes
awk '{print $9}' access.log | sort | uniq -c | sort -rn
```
