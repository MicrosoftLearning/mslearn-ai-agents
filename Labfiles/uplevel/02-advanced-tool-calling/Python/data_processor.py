import csv
import json
from typing import List, Dict
from pathlib import Path
from datetime import datetime


def load_csv_file(file_path: str) -> List[Dict]:
    """
    Load CSV file and return as list of dictionaries.
    
    Args:
        file_path: Path to CSV file
    
    Returns:
        List of dictionaries with CSV data
    """
    try:
        data = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        
        print(f"✅ Loaded {len(data)} rows from {Path(file_path).name}")
        return data
        
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        return []
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return []


def transform_sales_data(data: List[Dict]) -> Dict:
    """
    Transform sales data with aggregations and calculations.
    
    Args:
        data: List of sales records
    
    Returns:
        Transformed data with summaries
    """
    if not data:
        return {"error": "No data to transform"}
    
    try:
        # Initialize aggregators
        by_region = {}
        by_product = {}
        by_rep = {}
        
        # Process each record
        for record in data:
            region = record.get("Region", "Unknown")
            product = record.get("Product", "Unknown")
            rep = record.get("Sales_Rep", "Unknown")
            
            # Convert numeric values
            units = int(record.get("Units_Sold", 0))
            revenue = float(record.get("Revenue", 0))
            
            # Aggregate by region
            if region not in by_region:
                by_region[region] = {"units": 0, "revenue": 0, "count": 0}
            by_region[region]["units"] += units
            by_region[region]["revenue"] += revenue
            by_region[region]["count"] += 1
            
            # Aggregate by product
            if product not in by_product:
                by_product[product] = {"units": 0, "revenue": 0, "count": 0}
            by_product[product]["units"] += units
            by_product[product]["revenue"] += revenue
            by_product[product]["count"] += 1
            
            # Aggregate by rep
            if rep not in by_rep:
                by_rep[rep] = {"units": 0, "revenue": 0, "count": 0}
            by_rep[rep]["units"] += units
            by_rep[rep]["revenue"] += revenue
            by_rep[rep]["count"] += 1
        
        # Calculate averages
        for region_data in by_region.values():
            region_data["avg_revenue"] = region_data["revenue"] / region_data["count"]
        
        return {
            "status": "success",
            "total_records": len(data),
            "by_region": by_region,
            "by_product": by_product,
            "by_sales_rep": by_rep,
            "processed_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"error": str(e)}


def process_multiple_files(file_paths: List[str]) -> Dict:
    """
    Process multiple CSV files and combine results.
    
    Args:
        file_paths: List of paths to CSV files
    
    Returns:
        Combined analysis
    """
    print(f"\n🔄 Processing {len(file_paths)} file(s)...\n")
    
    all_data = []
    file_summaries = []
    
    for file_path in file_paths:
        # Load file
        data = load_csv_file(file_path)
        if data:
            all_data.extend(data)
            
            # Transform individual file
            transformed = transform_sales_data(data)
            file_summaries.append({
                "file": Path(file_path).name,
                "records": len(data),
                "summary": transformed
            })
    
    # Transform combined data
    combined_transform = transform_sales_data(all_data)
    
    return {
        "status": "success",
        "files_processed": len(file_paths),
        "total_records": len(all_data),
        "individual_files": file_summaries,
        "combined_analysis": combined_transform
    }


def export_results(data: Dict, output_path: str, format: str = "json") -> bool:
    """
    Export analysis results to file.
    
    Args:
        data: Data to export
        output_path: Output file path
        format: Export format ('json' or 'csv')
    
    Returns:
        Success status
    """
    try:
        if format == "json":
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✅ Exported to {output_path}")
            return True
            
        elif format == "csv":
            # Export summary as CSV
            with open(output_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Metric", "Value"])
                
                if "combined_analysis" in data:
                    writer.writerow(["Total Records", data["total_records"]])
                    writer.writerow(["Files Processed", data["files_processed"]])
            
            print(f"✅ Exported to {output_path}")
            return True
        else:
            print(f"❌ Unsupported format: {format}")
            return False
            
    except Exception as e:
        print(f"❌ Export failed: {e}")
        return False


# For testing
def main():
    """Test data processing functions."""
    print("\n=== Testing Data Processing ===\n")
    
    # Test with sales_data.csv if it exists
    if Path("sales_data.csv").exists():
        # Test 1: Load and transform
        data = load_csv_file("sales_data.csv")
        if data:
            transformed = transform_sales_data(data)
            print(f"\n📊 Analysis Complete:")
            print(f"  • Total records: {transformed.get('total_records', 0)}")
            print(f"  • Regions: {len(transformed.get('by_region', {}))}")
            print(f"  • Products: {len(transformed.get('by_product', {}))}")
            
            # Test 2: Export results
            export_results(
                transformed,
                "analysis_results.json",
                "json"
            )
    else:
        print("⚠️  sales_data.csv not found. Create it first.")


if __name__ == "__main__":
    main()
