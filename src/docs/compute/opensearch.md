# OpenSearch 2.x — Cluster Operations

Practical cheatsheet focused on **understanding and troubleshooting** a running OpenSearch cluster. All commands use the REST API via `curl`.

!!! tip
    Set a base variable to keep commands short:
    ```bash
    export OS="https://opensearch-node:9200"
    # with auth:
    export OS="https://admin:changeme@opensearch-node:9200"
    ```

---

## Cluster health

### Quick status check

```bash
curl -s "$OS/_cluster/health" | jq .
```

```json
{
  "cluster_name": "my-cluster",
  "status": "green",
  "number_of_nodes": 5,
  "number_of_data_nodes": 3,
  "active_primary_shards": 42,
  "active_shards": 84,
  "relocating_shards": 0,
  "initializing_shards": 0,
  "unassigned_shards": 0,
  "delayed_unassigned_shards": 0,
  "active_shards_percent_as_number": 100.0
}
```

| Status | Meaning |
|--------|---------|
| :green_circle: **green** | All primary and replica shards are assigned |
| :yellow_circle: **yellow** | All primaries OK, but some replicas are unassigned |
| :red_circle: **red** | Some **primary** shards are unassigned — data is missing |

### Per-index health

```bash
curl -s "$OS/_cluster/health?level=indices" | jq '.indices | to_entries[] | select(.value.status != "green")'
```

This filters to only show indices that are **not green** — the ones you care about during an incident.

---

## Nodes overview

### List all nodes

```bash
curl -s "$OS/_cat/nodes?v&h=name,ip,node.role,heap.percent,disk.used_percent,cpu,load_1m"
```

```
name          ip           node.role heap.percent disk.used_percent cpu load_1m
os-data-01    10.0.1.10    dimr              62                 71   8    1.23
os-data-02    10.0.1.11    dimr              55                 68   5    0.87
os-master-01  10.0.1.20    m                 34                 22   2    0.15
```

!!! warning
    Watch for `disk.used_percent` > **85%** — OpenSearch starts blocking writes at the high watermark (default 90%).

### Node roles cheatsheet

| Letter | Role |
|--------|------|
| `m` | master-eligible |
| `d` | data |
| `i` | ingest |
| `r` | remote cluster client |
| `c` | coordinating only (no letter shown) |

### Disk allocation detail

```bash
curl -s "$OS/_cat/allocation?v&h=node,shards,disk.indices,disk.used,disk.avail,disk.percent"
```

---

## Indices

### List all indices

```bash
curl -s "$OS/_cat/indices?v&h=index,health,status,pri,rep,docs.count,store.size&s=store.size:desc"
```

```
index               health status pri rep docs.count store.size
logs-2026.05.12     green  open     3   1    8234102     12.4gb
logs-2026.05.11     green  open     3   1    7891203     11.8gb
.opensearch-sap     green  open     1   1          4       24kb
```

| Column | Meaning |
|--------|---------|
| `pri` | Number of primary shards |
| `rep` | Number of replica copies per primary |
| `health` | Worst shard status for this index |
| `status` | `open` (serving requests) or `close` (not loaded) |

### Show only unhealthy indices

```bash
curl -s "$OS/_cat/indices?v&health=yellow"
curl -s "$OS/_cat/indices?v&health=red"
```

---

## Shards

### Understanding shards

An index is split into **primary shards** (the data) and **replica shards** (copies for HA). When a node goes down, replicas on surviving nodes get promoted to primary.

- **Yellow** = a replica can't be assigned (often: not enough nodes, or same-node restriction)
- **Red** = a primary shard has no copy anywhere — that data is unavailable

### List all shards

```bash
curl -s "$OS/_cat/shards?v&h=index,shard,prirep,state,docs,store,node&s=state"
```

```
index             shard prirep state         docs  store  node
logs-2026.05.12       0 p      STARTED    2745367  4.1gb  os-data-01
logs-2026.05.12       0 r      STARTED    2745367  4.1gb  os-data-02
logs-2026.05.12       1 p      STARTED    2744368  4.1gb  os-data-02
logs-2026.05.12       1 r      UNASSIGNED
```

| State | Meaning |
|-------|---------|
| `STARTED` | Shard is active and serving |
| `UNASSIGNED` | Shard has no node — **this is the problem** |
| `INITIALIZING` | Shard is being created or recovered |
| `RELOCATING` | Shard is moving to another node |

### Show only unassigned shards

```bash
curl -s "$OS/_cat/shards?v&h=index,shard,prirep,state,unassigned.reason&s=index" | grep UNASSIGNED
```

---

## Diagnosing unassigned shards

This is the most important section for incident response.

### Why is a shard unassigned?

```bash
curl -s "$OS/_cluster/allocation/explain" | jq .
```

This returns a detailed explanation for one unassigned shard. To ask about a specific shard:

```bash
curl -s -X POST "$OS/_cluster/allocation/explain" -H 'Content-Type: application/json' -d '{
  "index": "logs-2026.05.12",
  "shard": 1,
  "primary": false
}'  | jq '.deciders[] | select(.decision != "YES")'
```

### Common unassigned reasons

| Reason | Typical cause | Fix |
|--------|--------------|-----|
| `NODE_LEFT` | A node crashed or was removed | Bring the node back, or wait for replica promotion |
| `CLUSTER_RECOVERED` | Cluster just restarted | Wait — shards are recovering |
| `ALLOCATION_FAILED` | Disk full, corrupt shard | Check disk space, possibly delete old indices |
| `INDEX_CREATED` | New index, not enough nodes | Add nodes or reduce `number_of_replicas` |

### Force retry allocation

After fixing the root cause (disk space, node back up), nudge OpenSearch:

```bash
curl -s -X POST "$OS/_cluster/reroute?retry_failed=true"
```

---

## Common fix actions

### Free disk space (delete old indices)

```bash
curl -s -X DELETE "$OS/logs-2026.04.*"
```

!!! danger
    This **permanently deletes data**. Make sure you target the right indices.

### Reduce replicas on a yellow index

If you only have 1 data node, replicas can never be assigned. Reduce to 0:

```bash
curl -s -X PUT "$OS/logs-2026.05.12/_settings" -H 'Content-Type: application/json' -d '{
  "index.number_of_replicas": 0
}'
```

### Close an index to save resources

A closed index uses almost no heap or CPU but **cannot be searched**:

```bash
curl -s -X POST "$OS/old-index-2025.01/_close"
# reopen later:
curl -s -X POST "$OS/old-index-2025.01/_open"
```

---

## Cluster-level diagnostics

### Pending tasks

```bash
curl -s "$OS/_cluster/pending_tasks" | jq .
```

If this list is long, the master node is overwhelmed.

### Hot threads (find CPU-heavy operations)

```bash
curl -s "$OS/_nodes/hot_threads"
```

### Recovery progress

During shard recovery (node restart, replica allocation), track progress:

```bash
curl -s "$OS/_cat/recovery?v&active_only=true&h=index,shard,stage,bytes_percent,translog_ops_percent"
```

### Task list (running queries / operations)

```bash
curl -s "$OS/_tasks?actions=*search*&detailed&v"
```

---

## Quick reference card

| What | Command |
|------|---------|
| Cluster status | `GET _cluster/health` |
| Sick indices | `GET _cat/indices?v&health=yellow` |
| Unassigned shards | `GET _cat/shards?v` + grep `UNASSIGNED` |
| Why unassigned? | `GET _cluster/allocation/explain` |
| Node disk usage | `GET _cat/allocation?v` |
| Force re-allocate | `POST _cluster/reroute?retry_failed=true` |
| Recovery progress | `GET _cat/recovery?v&active_only=true` |
| Delete old data | `DELETE /index-pattern-*` |

!!! note
    All `_cat` APIs accept `?format=json` if you prefer JSON over the columnar format.
