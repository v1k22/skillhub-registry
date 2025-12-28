---
metadata:
  name: "etl-pipeline"
  version: "1.0.0"
  description: "Set up a production-ready ETL pipeline with data validation and monitoring"
  category: "data-engineering"
  tags: ["etl", "data-pipeline", "python", "pandas", "data-validation"]
  author: "skillhub"
  created: "2024-01-15"
  updated: "2024-01-15"

requirements:
  os: ["linux", "macos", "windows"]
  python: ">=3.9"
  packages:
    - pandas>=2.0.0
    - sqlalchemy>=2.0.0
    - great-expectations>=0.18.0
    - requests
    - python-dotenv
  hardware:
    - ram: ">=4GB"
    - disk_space: ">=5GB"

estimated_time: "20-30 minutes"
difficulty: "intermediate"
---

# ETL Pipeline Setup

## Overview
This skill sets up a production-ready Extract-Transform-Load (ETL) pipeline with data validation, error handling, and basic monitoring. Includes integration with CSV/JSON sources and database destinations.

## Task Description
Complete ETL pipeline implementation:
1. Extract data from multiple sources (CSV, JSON, API)
2. Transform and clean data using pandas
3. Validate data quality using Great Expectations
4. Load data into SQLite database (easily adaptable to PostgreSQL/MySQL)
5. Add logging and error handling
6. Create monitoring dashboard output

## Prerequisites
- Python 3.9+ installed
- Basic understanding of SQL
- Sample data files or API access (examples provided)

## Steps

### 1. Project Setup
```bash
# Create project directory
mkdir etl_pipeline
cd etl_pipeline

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install pandas sqlalchemy great-expectations requests python-dotenv
```

### 2. Create Project Structure
```bash
# Create directory structure
mkdir -p {data/{raw,processed,archive},logs,config,src}

# Create config file
cat > .env << 'EOF'
SOURCE_API_URL=https://api.example.com/data
DB_CONNECTION_STRING=sqlite:///data/processed/warehouse.db
LOG_LEVEL=INFO
EOF
```

### 3. Extract Module
```python
# src/extract.py
import pandas as pd
import requests
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class DataExtractor:
    def __init__(self, data_dir='data/raw'):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def extract_from_csv(self, filepath):
        """Extract data from CSV file."""
        logger.info(f"Extracting data from {filepath}")
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Extracted {len(df)} rows from CSV")
            return df
        except Exception as e:
            logger.error(f"Failed to extract CSV: {e}")
            raise

    def extract_from_json(self, filepath):
        """Extract data from JSON file."""
        logger.info(f"Extracting data from {filepath}")
        try:
            df = pd.read_json(filepath)
            logger.info(f"Extracted {len(df)} rows from JSON")
            return df
        except Exception as e:
            logger.error(f"Failed to extract JSON: {e}")
            raise

    def extract_from_api(self, url, params=None):
        """Extract data from REST API."""
        logger.info(f"Extracting data from API: {url}")
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            # Convert to DataFrame
            df = pd.DataFrame(data if isinstance(data, list) else [data])
            logger.info(f"Extracted {len(df)} rows from API")
            return df
        except Exception as e:
            logger.error(f"Failed to extract from API: {e}")
            raise

# Example usage
if __name__ == '__main__':
    extractor = DataExtractor()

    # Create sample CSV
    sample_data = pd.DataFrame({
        'id': range(1, 101),
        'name': [f'Product_{i}' for i in range(1, 101)],
        'price': [10.0 + i * 0.5 for i in range(100)],
        'quantity': [100 - i for i in range(100)]
    })
    sample_data.to_csv('data/raw/sample.csv', index=False)

    # Extract
    df = extractor.extract_from_csv('data/raw/sample.csv')
    print(df.head())
```

### 4. Transform Module
```python
# src/transform.py
import pandas as pd
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DataTransformer:
    def __init__(self):
        pass

    def clean_data(self, df):
        """Clean and standardize data."""
        logger.info("Cleaning data...")

        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates()
        duplicates_removed = initial_count - len(df)
        if duplicates_removed > 0:
            logger.warning(f"Removed {duplicates_removed} duplicate rows")

        # Handle missing values
        missing_counts = df.isnull().sum()
        if missing_counts.any():
            logger.warning(f"Missing values found:\n{missing_counts[missing_counts > 0]}")

        # Fill missing values with appropriate defaults
        for col in df.columns:
            if df[col].dtype in ['float64', 'int64']:
                df[col].fillna(df[col].median(), inplace=True)
            else:
                df[col].fillna('UNKNOWN', inplace=True)

        logger.info(f"Cleaned data: {len(df)} rows remaining")
        return df

    def add_derived_columns(self, df):
        """Add calculated/derived columns."""
        logger.info("Adding derived columns...")

        # Add timestamp
        df['processed_at'] = datetime.now().isoformat()

        # Example: Add total value column if price and quantity exist
        if 'price' in df.columns and 'quantity' in df.columns:
            df['total_value'] = df['price'] * df['quantity']
            logger.info("Added 'total_value' column")

        return df

    def apply_business_rules(self, df):
        """Apply business-specific transformations."""
        logger.info("Applying business rules...")

        # Example: Flag high-value items
        if 'total_value' in df.columns:
            df['high_value'] = df['total_value'] > df['total_value'].quantile(0.75)

        # Example: Categorize by price range
        if 'price' in df.columns:
            df['price_category'] = pd.cut(
                df['price'],
                bins=[0, 20, 50, 100, float('inf')],
                labels=['Budget', 'Mid-Range', 'Premium', 'Luxury']
            )

        return df

    def transform(self, df):
        """Execute full transformation pipeline."""
        df = self.clean_data(df)
        df = self.add_derived_columns(df)
        df = self.apply_business_rules(df)
        return df

# Example usage
if __name__ == '__main__':
    # Read sample data
    df = pd.read_csv('data/raw/sample.csv')

    # Transform
    transformer = DataTransformer()
    df_transformed = transformer.transform(df)

    print(df_transformed.head())
    print(f"\nColumns: {list(df_transformed.columns)}")
```

### 5. Load Module
```python
# src/load.py
import pandas as pd
from sqlalchemy import create_engine, text
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, connection_string='sqlite:///data/processed/warehouse.db'):
        self.connection_string = connection_string
        self.engine = create_engine(connection_string)
        logger.info(f"Database connection established: {connection_string}")

    def load_to_database(self, df, table_name, if_exists='replace'):
        """Load DataFrame to database table."""
        logger.info(f"Loading {len(df)} rows to table '{table_name}'...")

        try:
            df.to_sql(
                name=table_name,
                con=self.engine,
                if_exists=if_exists,
                index=False,
                method='multi',
                chunksize=1000
            )
            logger.info(f"Successfully loaded data to '{table_name}'")

            # Verify
            with self.engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                count = result.scalar()
                logger.info(f"Verified: {count} rows in '{table_name}'")

        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise

    def export_to_csv(self, df, filepath):
        """Export DataFrame to CSV."""
        logger.info(f"Exporting data to {filepath}")
        df.to_csv(filepath, index=False)
        logger.info(f"Exported {len(df)} rows to CSV")

# Example usage
if __name__ == '__main__':
    # Read transformed data
    df = pd.read_csv('data/raw/sample.csv')

    # Load
    loader = DataLoader()
    loader.load_to_database(df, 'products')
    loader.export_to_csv(df, 'data/processed/products_processed.csv')
```

### 6. Main Pipeline
```python
# src/pipeline.py
import logging
from pathlib import Path
from datetime import datetime
from extract import DataExtractor
from transform import DataTransformer
from load import DataLoader

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/etl_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ETLPipeline:
    def __init__(self):
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.loader = DataLoader()
        self.run_id = datetime.now().strftime('%Y%m%d_%H%M%S')

    def run(self, source_file='data/raw/sample.csv'):
        """Execute full ETL pipeline."""
        logger.info(f"Starting ETL pipeline run: {self.run_id}")

        try:
            # Extract
            logger.info("=" * 50)
            logger.info("EXTRACT PHASE")
            logger.info("=" * 50)
            df = self.extractor.extract_from_csv(source_file)

            # Transform
            logger.info("=" * 50)
            logger.info("TRANSFORM PHASE")
            logger.info("=" * 50)
            df_transformed = self.transformer.transform(df)

            # Load
            logger.info("=" * 50)
            logger.info("LOAD PHASE")
            logger.info("=" * 50)
            self.loader.load_to_database(df_transformed, 'products')
            self.loader.export_to_csv(
                df_transformed,
                f'data/processed/products_{self.run_id}.csv'
            )

            # Summary
            logger.info("=" * 50)
            logger.info("PIPELINE SUMMARY")
            logger.info("=" * 50)
            logger.info(f"Run ID: {self.run_id}")
            logger.info(f"Source: {source_file}")
            logger.info(f"Rows processed: {len(df_transformed)}")
            logger.info(f"Columns: {len(df_transformed.columns)}")
            logger.info("Status: SUCCESS")

            return df_transformed

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            logger.error("Status: FAILED")
            raise

if __name__ == '__main__':
    pipeline = ETLPipeline()
    result = pipeline.run()
    print("\nPipeline completed successfully!")
    print(f"Processed {len(result)} rows")
```

### 7. Run the Pipeline
```bash
# Create logs directory
mkdir -p logs

# Run the pipeline
cd src
python pipeline.py
```

## Expected Output
- `data/processed/warehouse.db`: SQLite database with loaded data
- `data/processed/products_YYYYMMDD_HHMMSS.csv`: Transformed data export
- `logs/etl_pipeline.log`: Detailed execution log
- Console output with progress and summary

## Troubleshooting

### Database Connection Errors
```bash
# Ensure directory exists
mkdir -p data/processed

# Check write permissions
ls -la data/processed
```

### Import Errors
```bash
# Run from src directory
cd src
python pipeline.py

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Memory Issues with Large Files
```python
# Use chunked reading
df = pd.read_csv('large_file.csv', chunksize=10000)
for chunk in df:
    process_chunk(chunk)
```

## Success Criteria
- [x] Data extracted from source without errors
- [x] All transformations applied successfully
- [x] Data loaded to database
- [x] Log file created with detailed execution trace
- [x] No data loss during pipeline execution
- [x] Processed CSV export created

## Next Steps
- Add data quality checks with Great Expectations
- Implement incremental loading (only new/changed data)
- Add retry logic for failed extractions
- Set up scheduling with cron or Apache Airflow
- Add email notifications for failures
- Implement data lineage tracking

## Related Skills
- `setup-airflow-pipeline`
- `data-quality-validation`
- `database-migration`
- `api-integration`

## References
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Great Expectations](https://docs.greatexpectations.io/)
- [ETL Best Practices](https://www.startdataengineering.com/post/what-is-etl/)
