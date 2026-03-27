# MongoDB

Practical `mongosh` cheatsheet for day-to-day queries.

## Connect and switch database

```bash
mongosh
show dbs
use mydb
db
```

```text
Current Mongosh Log ID: 67f...
Connecting to:          mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000
MongoDB server version: 8.0.0

admin   40.00 KiB
config  72.00 KiB
local   72.00 KiB

switched to db mydb
mydb
```

## Collections

```javascript
show collections
db.users.drop() // delete one collection
db.dropDatabase() // delete current database
```

## Insert documents

```javascript
db.users.insertOne({ name: "Alice", age: 29, city: "Paris", tags: ["pro", "beta"] })

db.users.insertMany([
    { name: "Bob", age: 35, city: "Lyon", score: 12 },
    { name: "Chloe", age: 22, city: "Paris", score: 18 }
])
```

```text
{
  acknowledged: true,
  insertedId: ObjectId("665000000000000000000001")
}
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId("665000000000000000000002"),
    '1': ObjectId("665000000000000000000003")
  }
}
```

## Find basics

### All documents

```javascript
db.users.find()
db.users.find().pretty()
```

```text
[
  {
    _id: ObjectId("665000000000000000000001"),
    name: 'Alice',
    age: 29,
    city: 'Paris',
    tags: [ 'pro', 'beta' ]
  },
  ...
]
```

### Filter (`where`)

```javascript
db.users.find({ city: "Paris" })
db.users.find({ age: { $gt: 30 } }) // > 30
db.users.find({ age: { $gte: 18, $lt: 30 } }) // 18 <= age < 30
db.users.find({ city: { $in: ["Paris", "Lyon"] } })
db.users.find({ city: { $ne: "Paris" } }) // !=
```

### Logical operators

```javascript
db.users.find({
    $and: [{ city: "Paris" }, { age: { $gte: 25 } }]
})

db.users.find({
    $or: [{ city: "Paris" }, { score: { $gte: 15 } }]
})
```

### Projection (select fields)

```javascript
db.users.find({ city: "Paris" }, { name: 1, age: 1, _id: 0 })
```

```text
[
  { name: 'Alice', age: 29 },
  { name: 'Chloe', age: 22 }
]
```

### Sort, limit, skip (pagination)

```javascript
db.users.find().sort({ age: -1 }) // desc
db.users.find().sort({ age: 1, name: 1 }) // asc
db.users.find().limit(10)
db.users.find().skip(20).limit(10) // page 3 with page size 10
```

### Find one

```javascript
db.users.findOne({ name: "Alice" })
```

```text
{
  _id: ObjectId("665000000000000000000001"),
  name: 'Alice',
  age: 29,
  city: 'Paris',
  tags: [ 'pro', 'beta' ]
}
```

## Count

```javascript
db.users.estimatedDocumentCount() // fast total estimate
db.users.countDocuments({ city: "Paris" }) // accurate with filter
```

```text
3
2
```

## Update

```javascript
db.users.updateOne(
    { name: "Alice" },
    { $set: { city: "Marseille" } }
)

db.users.updateMany(
    { city: "Paris" },
    { $inc: { score: 1 } } // increment
)

db.users.updateOne(
    { name: "Bob" },
    { $unset: { oldField: "" } } // remove field
)

db.users.updateOne(
    { name: "Diane" },
    { $set: { city: "Nice", age: 31 } },
    { upsert: true } // insert if not found
)
```

```text
{ acknowledged: true, matchedCount: 1, modifiedCount: 1, upsertedId: null }
{ acknowledged: true, matchedCount: 2, modifiedCount: 2, upsertedId: null }
{ acknowledged: true, matchedCount: 1, modifiedCount: 1, upsertedId: null }
{
  acknowledged: true,
  matchedCount: 0,
  modifiedCount: 0,
  upsertedId: ObjectId("665000000000000000000004")
}
```

## Delete

```javascript
db.users.deleteOne({ name: "Alice" })
db.users.deleteMany({ age: { $lt: 18 } })
```

```text
{ acknowledged: true, deletedCount: 1 }
{ acknowledged: true, deletedCount: 0 }
```

## Useful aggregate pipelines

### Group and count by field

```javascript
db.users.aggregate([
    { $group: { _id: "$city", count: { $sum: 1 } } },
    { $sort: { count: -1 } }
])
```

```text
[
  { _id: 'Paris', count: 2 },
  { _id: 'Lyon', count: 1 }
]
```

### Average / min / max

```javascript
db.users.aggregate([
    {
        $group: {
            _id: "$city",
            avgAge: { $avg: "$age" },
            minAge: { $min: "$age" },
            maxAge: { $max: "$age" }
        }
    }
])
```

```text
[
  { _id: 'Paris', avgAge: 25.5, minAge: 22, maxAge: 29 },
  { _id: 'Lyon', avgAge: 35, minAge: 35, maxAge: 35 }
]
```

### Match + project + sort

```javascript
db.users.aggregate([
    { $match: { age: { $gte: 18 } } },
    { $project: { _id: 0, name: 1, city: 1, age: 1 } },
    { $sort: { age: -1 } },
    { $limit: 5 }
])
```

```text
[
  { name: 'Bob', city: 'Lyon', age: 35 },
  { name: 'Alice', city: 'Paris', age: 29 },
  { name: 'Chloe', city: 'Paris', age: 22 }
]
```

### Unwind array field

```javascript
db.users.aggregate([
    { $unwind: "$tags" },
    { $group: { _id: "$tags", count: { $sum: 1 } } },
    { $sort: { count: -1 } }
])
```

```text
[
  { _id: 'pro', count: 1 },
  { _id: 'beta', count: 1 }
]
```

## Distinct values

```javascript
db.users.distinct("city")
```

```text
[ 'Paris', 'Lyon' ]
```

## Index basics

```javascript
db.users.createIndex({ email: 1 }, { unique: true })
db.users.createIndex({ city: 1, age: -1 })
db.users.getIndexes()
db.users.dropIndex("city_1_age_-1")
```

```text
email_1
city_1_age_-1
[
  { v: 2, key: { _id: 1 }, name: '_id_' },
  { v: 2, key: { email: 1 }, name: 'email_1', unique: true },
  { v: 2, key: { city: 1, age: -1 }, name: 'city_1_age_-1' }
]
{ nIndexesWas: 3, ok: 1 }
```

## Quick introspection

```javascript
db.users.findOne() // inspect shape
db.users.stats()
```

```text
{
  _id: ObjectId("665000000000000000000002"),
  name: 'Bob',
  age: 35,
  city: 'Lyon',
  score: 12
}
{
  ns: 'mydb.users',
  count: 3,
  size: 312,
  avgObjSize: 104,
  storageSize: 4096,
  nindexes: 2
}
```

!!! tip
    Start simple: `find` + projection + sort + limit solves most daily needs.

!!! note
    Prefer `countDocuments()` for exact counts and `estimatedDocumentCount()` for quick totals.
