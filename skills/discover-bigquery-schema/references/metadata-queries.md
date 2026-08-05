# Metadata Query Patterns

Run these only in an allow-listed project and location. Replace placeholders before use.

```sql
SELECT table_name, table_type
FROM `PROJECT.DATASET.INFORMATION_SCHEMA.TABLES`
ORDER BY table_name;
```

```sql
SELECT table_name, column_name, data_type, is_nullable
FROM `PROJECT.DATASET.INFORMATION_SCHEMA.COLUMNS`
ORDER BY table_name, ordinal_position;
```

```sql
SELECT table_name, partition_id, total_rows, total_logical_bytes
FROM `PROJECT.DATASET.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'TABLE_NAME';
```

Do not query sample business rows as part of discovery. Capture dataset location before
using region-qualified metadata views.
