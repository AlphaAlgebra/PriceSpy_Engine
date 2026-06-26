import pytest
from unittest.mock import MagicMock, patch
from pydantic import ValidationError

# Assuming your declarative system contracts live inside models.py
# Let's mock a standard enterprise product payload data schema for validation checks
from models import ProductPayload 

def test_pydantic_boundary_constraints_data_cleaning():
    """
    Validates that the High-Fidelity Domain Boundary Constraints successfully strip 
    corrupted currency strings and symbols to guarantee structural down-stream type safety.
    """
    raw_input = {
        "product_id": "SKU-99281",
        "title": " Premium Competitor Item  ",
        "raw_price": " $1,249.99 USD "
    }
    
    # Execute structural validation through your data model contract
    product = ProductPayload(**raw_input)
    
    assert product.product_id == "SKU-99281"
    assert product.title == "Premium Competitor Item" # Verifies string stripping
    assert product.price == 1249.99                 # Verifies translation to pure float
    assert isinstance(product.price, float)

def test_pydantic_invalid_data_rejection():
    """Ensures that corrupted data inputs fail fast at the boundary layer."""
    corrupted_input = {
        "product_id": "SKU-BROKEN",
        "title": "Invalid Item",
        "raw_price": "Price Hidden / Out of Stock"
    }
    with pytest.raises(ValidationError):
        ProductPayload(**corrupted_input)

@patch('scraper.extract_tier1_wire_api')
def test_multi_tier_fallback_matrix_tier1_success(mock_tier1):
    """Validates that Tier 1 (Wire-Level API Network Interception) processes clean JSON cleanly on hit."""
    mock_tier1.return_value = {"product_id": "SKU-1", "title": "API Item", "price": 49.99}
    
    # Simulate scraper central execution loop orchestration
    from scraper import run_defensive_extraction
    result = run_defensive_extraction("https://example-ecommerce.com")
    
    assert result["success"] is True
    assert result["tier_executed"] == 1
    assert result["data"].price == 49.99

@patch('scraper.extract_tier1_wire_api')
@patch('scraper.extract_tier2_seo_graph')
def test_multi_tier_fallback_matrix_tier2_activation(mock_seo, mock_tier1):
    """Validates that Tier 2 (Structured Metadata Graph Parsing) executes if the API endpoint is obscured."""
    # Force Tier 1 to encounter an intentional network or anti-bot exception
    mock_tier1.side_effect = Exception("Cloudflare API Interception Blocked")
    # Mock Tier 2 to successfully locate the application/ld+json metadata array
    mock_seo.return_value = {"product_id": "SKU-2", "title": "SEO Item", "price": 89.99}
    
    from scraper import run_defensive_extraction
    result = run_defensive_extraction("https://example-ecommerce.com")
    
    assert result["success"] is True
    assert result["tier_executed"] == 2
    assert "Cloudflare" not in str(result["data"])
    assert result["data"].price == 89.99
