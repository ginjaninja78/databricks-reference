# Contributing to The Ultimate Databricks Reference Library

Thank you for your interest in contributing to this project! This repository aims to be the most comprehensive, exhaustive resource for Databricks developers, and your contributions help make that vision a reality.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Style Guidelines](#style-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Repository Structure](#repository-structure)

---

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

---

## How Can I Contribute?

### Reporting Bugs or Issues

If you find an error in the documentation, a broken link, or incorrect code:

1. Check if the issue already exists in [GitHub Issues](https://github.com/ginjaninja78/databricks-reference/issues)
2. If not, create a new issue with:
   - A clear, descriptive title
   - The location of the error (file path and line number if applicable)
   - A description of the problem
   - Suggested fix (if you have one)

### Suggesting Enhancements

Have an idea for a new section, example, or improvement?

1. Open a [GitHub Discussion](https://github.com/ginjaninja78/databricks-reference/discussions) to propose your idea
2. Describe the enhancement and its value to the community
3. If approved, you can proceed with implementation

### Adding New Content

We welcome new documentation, code examples, and notebooks! Here's how:

1. **Fork the repository**
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Add your content** following the [Style Guidelines](#style-guidelines)
4. **Test your changes** (ensure all code examples run successfully)
5. **Commit your changes** following the [Commit Message Guidelines](#commit-message-guidelines)
6. **Push to your fork** and submit a Pull Request

---

## Style Guidelines

### Documentation Style

- **Format**: Use GitHub-flavored Markdown (`.md`)
- **Tone**: Professional, clear, and instructional
- **Structure**: Use headers (`##`, `###`) to organize content hierarchically
- **Code Blocks**: Always specify the language for syntax highlighting:
  ````markdown
  ```python
  # Your code here
  ```
  ````
- **Links**: Use descriptive link text (not "click here")
- **Examples**: Provide real-world, practical examples wherever possible

### Code Style

#### Python/PySpark
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use meaningful variable names
- Include docstrings for functions and classes
- Add inline comments for complex logic

Example:
```python
def read_bronze_table(table_name: str, spark_session) -> DataFrame:
    """
    Read a Bronze layer Delta table.
    
    Args:
        table_name: Name of the Bronze table
        spark_session: Active Spark session
        
    Returns:
        DataFrame containing the Bronze table data
    """
    return spark_session.table(f"bronze.{table_name}")
```

#### SQL
- Use uppercase for SQL keywords: `SELECT`, `FROM`, `WHERE`
- Use meaningful table and column aliases
- Format complex queries with proper indentation

Example:
```sql
SELECT 
    customer_id,
    SUM(order_amount) AS total_spent,
    COUNT(order_id) AS order_count
FROM gold.customer_orders
WHERE order_date >= '2024-01-01'
GROUP BY customer_id
ORDER BY total_spent DESC;
```

#### R
- Follow [Tidyverse Style Guide](https://style.tidyverse.org/)
- Use `<-` for assignment
- Use `snake_case` for variable names

#### Scala
- Follow [Scala Style Guide](https://docs.scala-lang.org/style/)
- Use `camelCase` for variable names
- Use `PascalCase` for class names

### Notebook Guidelines

- **File Format**: Save notebooks as `.ipynb` (Jupyter format) or `.dbc` (Databricks archive)
- **Structure**:
  - Start with a markdown cell explaining the notebook's purpose
  - Use markdown cells to separate and explain each section
  - Include expected inputs and outputs
- **Naming**: Use descriptive, lowercase names with underscores: `01_bronze_ingestion_example.ipynb`

---

## Commit Message Guidelines

Use clear, descriptive commit messages following this format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature or content
- `fix`: Bug fix or correction
- `docs`: Documentation-only changes
- `style`: Formatting changes (no code logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(pillar_ii): Add PySpark window functions tutorial

Added comprehensive guide on using window functions in PySpark,
including rank(), dense_rank(), and lead()/lag() examples.

Closes #42
```

```
fix(pillar_iv): Correct Power BI connection string example

Fixed the JDBC connection string format for SQL Warehouse connections.
Previous example was missing the HTTP path parameter.
```

---

## Pull Request Process

1. **Ensure your PR addresses a single concern** (one feature, one bug fix, etc.)
2. **Update documentation** if you're changing functionality
3. **Add yourself to CONTRIBUTORS.md** (if this is your first contribution)
4. **Ensure all code examples are tested** and working
5. **Link related issues** in the PR description using `Closes #issue-number`
6. **Request review** from maintainers
7. **Address feedback** promptly and professionally

### PR Checklist

Before submitting, verify:

- [ ] Code follows the style guidelines
- [ ] All examples have been tested
- [ ] Documentation is clear and complete
- [ ] Commit messages follow the guidelines
- [ ] No merge conflicts with `main`
- [ ] Related issues are linked

---

## Repository Structure

Understanding the repository structure will help you place your contributions correctly:

```
databricks-reference/
├── .librAIrian/              # The LibrAIrian AI navigation system
├── pillar_i/                 # Core Concepts
│   ├── introduction/
│   ├── workspace_and_notebooks/
│   └── medallion_architecture/
├── pillar_ii/                # Developer's Toolkit
│   ├── pyspark_mastery/
│   ├── sql_on_lakehouse/
│   └── r_and_scala/
├── pillar_iii/               # MLOps & DevOps
│   ├── github_integration/
│   └── mlops_devops/
├── pillar_iv/                # Enterprise Readiness
│   ├── bi_power_platform/
│   ├── delta_lake/
│   ├── governance_security/
│   └── workflows/
├── sample_notebooks/         # Example notebooks
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── advanced/
├── sample_code/              # Example code
│   ├── python/
│   ├── r/
│   ├── scala/
│   └── sql/
└── docs/                     # GitHub Pages site content
```

### Where to Add Content

- **Conceptual documentation**: Place in the appropriate `pillar_*/` directory
- **Code examples**: Place in `sample_code/<language>/`
- **Notebooks**: Place in `sample_notebooks/<layer>/`
- **GitHub Copilot prompts**: Place in `pillar_iii/github_integration/copilot_prompts/`
- **LibrAIrian files**: Place in `.librAIrian/`

---

## Questions?

If you have questions about contributing, please:

1. Check existing [GitHub Discussions](https://github.com/ginjaninja78/databricks-reference/discussions)
2. Open a new discussion if your question hasn't been answered
3. Tag maintainers if you need urgent clarification

---

**Thank you for contributing to the Databricks community!** 🎉
