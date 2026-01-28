import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json

# Simulated data store (in production, this would be a database)
SALES_CACHE = {}


async def analyze_customer_segment(
    segment: str,
    time_period: str = "30d",
    metrics: Optional[List[str]] = None
) -> dict:
    """
    Analyze customer segment with async data fetching.
    
    Args:
        segment: Customer segment ('enterprise', 'smb', 'consumer')
        time_period: Analysis period ('7d', '30d', '90d')
        metrics: Optional list of metrics to calculate
    
    Returns:
        dict: Analysis results with metrics
    """
    # Validate parameters
    valid_segments = ["enterprise", "smb", "consumer"]
    if segment not in valid_segments:
        return {
            "status": "error",
            "error": f"Invalid segment. Must be one of: {', '.join(valid_segments)}"
        }
    
    valid_periods = ["7d", "30d", "90d"]
    if time_period not in valid_periods:
        return {
            "status": "error",
            "error": f"Invalid period. Must be one of: {', '.join(valid_periods)}"
        }
    
    # Default metrics if none provided
    if metrics is None:
        metrics = ["revenue", "growth", "retention"]
    
    try:
        # Simulate async data fetching
        print(f"  📊 Fetching {segment} data for {time_period}...")
        await asyncio.sleep(0.5)  # Simulate API call
        
        # Simulate data processing
        results = {
            "segment": segment,
            "time_period": time_period,
            "timestamp": datetime.now().isoformat(),
            "metrics": {}
        }
        
        # Calculate requested metrics
        for metric in metrics:
            if metric == "revenue":
                results["metrics"]["revenue"] = {
                    "total": 125000 + (5000 * len(segment)),
                    "currency": "USD"
                }
            elif metric == "growth":
                results["metrics"]["growth"] = {
                    "percentage": 15.5,
                    "trend": "increasing"
                }
            elif metric == "retention":
                results["metrics"]["retention"] = {
                    "rate": 0.92,
                    "cohort_size": 450
                }
        
        results["status"] = "success"
        return results
        
    except Exception as e:
        # Graceful error handling
        return {
            "status": "error",
            "error": str(e),
            "fallback_data": await get_cached_segment_data(segment)
        }


async def get_cached_segment_data(segment: str) -> dict:
    """Fallback function to retrieve cached data."""
    await asyncio.sleep(0.1)
    return {
        "cached": True,
        "segment": segment,
        "last_updated": (datetime.now() - timedelta(hours=1)).isoformat()
    }


async def calculate_forecast(
    product: str,
    months: int = 3,
    include_confidence: bool = True
) -> dict:
    """
    Calculate sales forecast with confidence intervals.
    
    Args:
        product: Product name
        months: Number of months to forecast
        include_confidence: Include confidence intervals
    
    Returns:
        dict: Forecast results
    """
    # Validate parameters
    if months < 1 or months > 12:
        return {
            "status": "error",
            "error": "Months must be between 1 and 12"
        }
    
    try:
        print(f"  🔮 Calculating {months}-month forecast for {product}...")
        await asyncio.sleep(0.3)
        
        # Simulate forecast calculation
        base_value = 10000
        forecast = []
        
        for month in range(1, months + 1):
            prediction = {
                "month": month,
                "predicted_units": base_value + (month * 500),
                "predicted_revenue": (base_value + (month * 500)) * 50
            }
            
            if include_confidence:
                prediction["confidence_interval"] = {
                    "lower": prediction["predicted_units"] * 0.85,
                    "upper": prediction["predicted_units"] * 1.15
                }
            
            forecast.append(prediction)
        
        return {
            "status": "success",
            "product": product,
            "forecast": forecast,
            "model": "linear_regression",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


async def process_sales_pipeline(data: Dict) -> dict:
    """
    Chain multiple analysis functions together.
    
    Args:
        data: Input data with segments and products
    
    Returns:
        dict: Combined analysis results
    """
    try:
        print("  🔄 Processing sales pipeline...")
        
        # Step 1: Analyze segments (parallel)
        segments = data.get("segments", ["enterprise", "smb"])
        segment_tasks = [
            analyze_customer_segment(seg, "30d")
            for seg in segments
        ]
        segment_results = await asyncio.gather(*segment_tasks)
        
        # Step 2: Calculate forecasts (parallel)
        products = data.get("products", ["Widget A", "Widget B"])
        forecast_tasks = [
            calculate_forecast(prod, 3)
            for prod in products
        ]
        forecast_results = await asyncio.gather(*forecast_tasks)
        
        # Step 3: Combine results
        return {
            "status": "success",
            "pipeline_completed": datetime.now().isoformat(),
            "segment_analysis": segment_results,
            "forecasts": forecast_results,
            "recommendations": generate_recommendations(
                segment_results,
                forecast_results
            )
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def generate_recommendations(segments, forecasts) -> List[str]:
    """Generate actionable recommendations based on analysis."""
    recommendations = []
    
    # Check growth trends
    for seg in segments:
        if seg.get("status") == "success":
            metrics = seg.get("metrics", {})
            growth = metrics.get("growth", {})
            if growth.get("percentage", 0) > 10:
                recommendations.append(
                    f"Strong growth in {seg['segment']} segment - consider expanding"
                )
    
    # Check forecast trends
    for forecast in forecasts:
        if forecast.get("status") == "success":
            predictions = forecast.get("forecast", [])
            if len(predictions) > 0:
                last_month = predictions[-1]["predicted_revenue"]
                if last_month > 600000:
                    recommendations.append(
                        f"High revenue forecast for {forecast['product']} - increase inventory"
                    )
    
    return recommendations if recommendations else ["Continue monitoring trends"]


# For testing
async def test_functions():
    """Test all async functions."""
    print("\n=== Testing Async Functions ===\n")
    
    # Test 1: Segment analysis
    result1 = await analyze_customer_segment("enterprise", "30d")
    print(f"✅ Segment analysis: {result1['status']}")
    
    # Test 2: Forecast
    result2 = await calculate_forecast("Widget A", 3)
    print(f"✅ Forecast: {result2['status']}")
    
    # Test 3: Pipeline
    result3 = await process_sales_pipeline({
        "segments": ["enterprise", "smb"],
        "products": ["Widget A", "Widget B"]
    })
    print(f"✅ Pipeline: {result3['status']}")
    print(f"\nRecommendations:")
    for rec in result3.get("recommendations", []):
        print(f"  • {rec}")


if __name__ == "__main__":
    asyncio.run(test_functions())
