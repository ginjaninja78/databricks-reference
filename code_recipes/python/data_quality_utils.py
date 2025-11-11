"""
Data Quality Utilities for Databricks

This module provides reusable functions for implementing data quality checks
and validations in Databricks pipelines.

Usage:
    from data_quality_utils import DataQualityChecker
    
    checker = DataQualityChecker(spark)
    results = checker.check_completeness(df, ["customer_id", "transaction_id"])
"""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, count, when, isnan, sum as spark_sum
from typing import List, Dict, Any
import json


class DataQualityChecker:
    """
    A comprehensive data quality checker for Spark DataFrames.
    
    Provides methods for common data quality checks including:
    - Completeness (null checks)
    - Uniqueness (duplicate detection)
    - Validity (data type and range checks)
    - Consistency (cross-column validation)
    """
    
    def __init__(self, spark: SparkSession):
        """
        Initialize the DataQualityChecker.
        
        Args:
            spark: Active SparkSession
        """
        self.spark = spark
        
    def check_completeness(
        self, 
        df: DataFrame, 
        columns: List[str],
        threshold: float = 0.95
    ) -> Dict[str, Any]:
        """
        Check completeness (non-null percentage) for specified columns.
        
        Args:
            df: Input DataFrame
            columns: List of column names to check
            threshold: Minimum acceptable completeness rate (0.0 to 1.0)
            
        Returns:
            Dictionary with completeness metrics and pass/fail status
        """
        total_rows = df.count()
        results = {
            "total_rows": total_rows,
            "threshold": threshold,
            "columns": {},
            "passed": True
        }
        
        for column in columns:
            non_null_count = df.filter(col(column).isNotNull()).count()
            completeness_rate = non_null_count / total_rows if total_rows > 0 else 0.0
            
            column_result = {
                "non_null_count": non_null_count,
                "null_count": total_rows - non_null_count,
                "completeness_rate": round(completeness_rate, 4),
                "passed": completeness_rate >= threshold
            }
            
            results["columns"][column] = column_result
            
            if not column_result["passed"]:
                results["passed"] = False
                
        return results
    
    def check_uniqueness(
        self, 
        df: DataFrame, 
        columns: List[str]
    ) -> Dict[str, Any]:
        """
        Check for duplicate records based on specified columns.
        
        Args:
            df: Input DataFrame
            columns: List of column names that should be unique together
            
        Returns:
            Dictionary with uniqueness metrics
        """
        total_rows = df.count()
        distinct_rows = df.select(columns).distinct().count()
        duplicate_count = total_rows - distinct_rows
        
        results = {
            "total_rows": total_rows,
            "distinct_rows": distinct_rows,
            "duplicate_count": duplicate_count,
            "uniqueness_rate": round(distinct_rows / total_rows if total_rows > 0 else 0.0, 4),
            "passed": duplicate_count == 0
        }
        
        return results
    
    def check_numeric_range(
        self,
        df: DataFrame,
        column: str,
        min_value: float = None,
        max_value: float = None
    ) -> Dict[str, Any]:
        """
        Check if numeric values fall within an expected range.
        
        Args:
            df: Input DataFrame
            column: Column name to check
            min_value: Minimum acceptable value (inclusive)
            max_value: Maximum acceptable value (inclusive)
            
        Returns:
            Dictionary with range validation metrics
        """
        total_rows = df.count()
        
        # Build filter condition
        filter_condition = col(column).isNotNull()
        if min_value is not None:
            filter_condition = filter_condition & (col(column) >= min_value)
        if max_value is not None:
            filter_condition = filter_condition & (col(column) <= max_value)
            
        valid_count = df.filter(filter_condition).count()
        invalid_count = total_rows - valid_count
        
        results = {
            "total_rows": total_rows,
            "valid_count": valid_count,
            "invalid_count": invalid_count,
            "validity_rate": round(valid_count / total_rows if total_rows > 0 else 0.0, 4),
            "min_value": min_value,
            "max_value": max_value,
            "passed": invalid_count == 0
        }
        
        return results
    
    def check_referential_integrity(
        self,
        fact_df: DataFrame,
        dimension_df: DataFrame,
        fact_key: str,
        dimension_key: str
    ) -> Dict[str, Any]:
        """
        Check referential integrity between fact and dimension tables.
        
        Args:
            fact_df: Fact table DataFrame
            dimension_df: Dimension table DataFrame
            fact_key: Foreign key column in fact table
            dimension_key: Primary key column in dimension table
            
        Returns:
            Dictionary with referential integrity metrics
        """
        total_fact_rows = fact_df.count()
        
        # Find orphaned records (fact records with no matching dimension)
        orphaned_df = (
            fact_df
            .select(fact_key)
            .distinct()
            .join(
                dimension_df.select(dimension_key),
                fact_df[fact_key] == dimension_df[dimension_key],
                "left_anti"
            )
        )
        
        orphaned_count = orphaned_df.count()
        
        results = {
            "total_fact_rows": total_fact_rows,
            "orphaned_keys_count": orphaned_count,
            "integrity_rate": round(1 - (orphaned_count / total_fact_rows) if total_fact_rows > 0 else 1.0, 4),
            "passed": orphaned_count == 0
        }
        
        return results
    
    def generate_quality_report(
        self,
        df: DataFrame,
        checks: Dict[str, Any]
    ) -> str:
        """
        Generate a comprehensive data quality report.
        
        Args:
            df: Input DataFrame
            checks: Dictionary of check results
            
        Returns:
            Formatted quality report as a string
        """
        report = []
        report.append("=" * 60)
        report.append("DATA QUALITY REPORT")
        report.append("=" * 60)
        report.append(f"Total Rows: {df.count():,}")
        report.append(f"Total Columns: {len(df.columns)}")
        report.append("")
        
        for check_name, check_result in checks.items():
            report.append(f"Check: {check_name}")
            report.append(f"Status: {'✓ PASSED' if check_result.get('passed', False) else '✗ FAILED'}")
            report.append(json.dumps(check_result, indent=2))
            report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)


# Example usage function
def example_usage():
    """
    Example demonstrating how to use the DataQualityChecker.
    """
    from pyspark.sql import SparkSession
    
    # Initialize Spark (already available in Databricks notebooks as 'spark')
    # spark = SparkSession.builder.appName("DataQualityExample").getOrCreate()
    
    # Create sample data
    data = [
        (1, "Alice", 25, 50000),
        (2, "Bob", 30, 60000),
        (3, "Charlie", None, 55000),  # Missing age
        (4, "David", 35, 70000),
        (5, "Eve", 28, None),  # Missing salary
        (6, "Alice", 25, 50000),  # Duplicate
    ]
    
    df = spark.createDataFrame(data, ["id", "name", "age", "salary"])
    
    # Initialize checker
    checker = DataQualityChecker(spark)
    
    # Run checks
    checks = {}
    
    # Check completeness
    checks["completeness"] = checker.check_completeness(
        df, 
        columns=["id", "name", "age", "salary"],
        threshold=0.90
    )
    
    # Check uniqueness
    checks["uniqueness"] = checker.check_uniqueness(
        df,
        columns=["id"]
    )
    
    # Check numeric range
    checks["age_range"] = checker.check_numeric_range(
        df,
        column="age",
        min_value=18,
        max_value=65
    )
    
    # Generate report
    report = checker.generate_quality_report(df, checks)
    print(report)
    
    return checks


if __name__ == "__main__":
    # This will run when the module is executed directly
    example_usage()
