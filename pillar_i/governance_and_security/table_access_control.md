---
title: Table Access Control (ACLs)
nav_order: 2
parent: Data Governance & Security
grand_parent: Pillar I The Databricks Universe
---

# Securing Data: Table Access Control Lists (ACLs)

While Unity Catalog provides the high-level framework for governance, **Table Access Control Lists (ACLs)** are the mechanism for implementing fine-grained security on your data assets. This is how you control precisely who can see and interact with specific tables and views.

In modern Databricks environments, Table ACLs are managed exclusively through Unity Catalog using standard SQL `GRANT` and `REVOKE` commands. This approach provides a consistent, auditable, and powerful way to manage permissions.

## The Privilege Model

Unity Catalog defines a clear set of privileges that can be granted on different securable objects. For tables, the most common privileges are:

| Privilege | Description |
|---|---|
| `SELECT` | Allows the user to read data from the table or view. Required for any query that accesses the data. |
| `MODIFY` | Allows the user to insert, update, and delete data in the table. |
| `CREATE TABLE` | (On a schema) Allows the user to create new tables or views within the schema. |
| `ALL PRIVILEGES` | Grants all privileges applicable to the object. Use with caution. |

Permissions are granted to **principals**, which can be individual users, groups, or service principals (for automated jobs).

**Best Practice**: Always grant permissions to **groups** rather than individual users. This simplifies administration immensely. When a user changes roles, you simply move them to a different group, and their permissions are automatically updated without having to alter any `GRANT` statements.

## Dynamic Views for Row-Level and Column-Level Security

Unity Catalog enables powerful fine-grained security patterns like row-level security and column-level masking through the use of **dynamic views**.

A dynamic view is a view that can display different data to different users based on their identity or group membership.

### Row-Level Security

Imagine you have a `sales_transactions` table with data from all regions, but you want sales representatives to only see transactions from their own region.

1.  **Create a mapping table** that associates users or groups with their allowed regions.
2.  **Create a dynamic view** that joins the data table with the mapping table and filters based on the current user.

```sql
-- Step 1: (Optional) A mapping table for more complex rules
-- For this example, we'll assume user emails contain the region, e.g., 'sales.us@company.com'

-- Step 2: Create the secure dynamic view
CREATE VIEW gold.secure_sales_transactions AS
SELECT
  transaction_id,
  product_id,
  -- The region column is filtered, so we can show it
  region,
  amount,
  transaction_date
FROM silver.sales_transactions
WHERE
  -- The is_member() function checks the current user's group membership
  -- Or, for a simpler rule based on name:
  region = SPLIT(current_user(), '[.@]')[1]; -- Extracts 'us' from 'sales.us@company.com'
```

3.  **Grant `SELECT` permissions on the view**, not the underlying table.

Now, when a user from the US team queries `gold.secure_sales_transactions`, they will only see rows where `region = 'us'`. The filtering is applied automatically and transparently.

### Column-Level Masking

Similarly, you may want to prevent certain users from seeing sensitive columns, like Personally Identifiable Information (PII).

Let's say you have a `customers` table with a `ssn` column. You want HR managers to see the full SSN, but you want to mask it for all other analysts.

```sql
-- Create a dynamic view that masks the 'ssn' column based on group membership
CREATE VIEW gold.secure_customers AS
SELECT
  customer_id,
  first_name,
  last_name,
  CASE
    WHEN is_member('hr_managers') THEN ssn
    ELSE '***-**-****'
  END AS ssn,
  address
FROM silver.customers;
```

-   **Grant `SELECT` access** to `gold.secure_customers` to both the `hr_managers` and `analysts` groups.
-   **Revoke all access** to the underlying `silver.customers` table.

When a member of the `hr_managers` group queries the view, they will see the actual Social Security Number. When a member of the `analysts` group queries the exact same view, they will see the masked value `'***-**-****'`.

By leveraging dynamic views, you can implement sophisticated security rules directly within the database layer, ensuring that the rules are consistently applied regardless of the tool or application used to access the data. This is a far more robust approach than relying on application-level security, which can be inconsistent and easy to bypass.
