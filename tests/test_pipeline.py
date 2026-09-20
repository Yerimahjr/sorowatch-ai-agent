import pytest
import respx
from httpx import Response

from app.graph.pipeline import run_pipeline
from app.horizon_client import HORIZON_TESTNET_URL


@pytest.mark.asyncio
@respx.mock
async def test_pipeline_flags_high_risk_address():
    address = "GABCDEXAMPLE"
    respx.get(f"{HORIZON_TESTNET_URL}/accounts/{address}/operations").mock(
        return_value=Response(
            200,
            json={
                "_embedded": {
                    "records": [
                        {"created_at": "2026-01-01T00:00:00Z", "to": "GX", "amount": "10"},
                        {"created_at": "2026-01-01T00:00:05Z", "to": "GX", "amount": "10"},
                        {"created_at": "2026-01-01T00:00:10Z", "to": "GX", "amount": "9999"},
                    ]
                }
            },
        )
    )

    result = await run_pipeline(address, threshold=10)
    assert len(result["operations"]) == 3
    assert result["score"] > 0
    assert result["flagged"] is True


@pytest.mark.asyncio
@respx.mock
async def test_pipeline_does_not_flag_address_with_no_history():
    address = "GNEWACCOUNT"
    respx.get(f"{HORIZON_TESTNET_URL}/accounts/{address}/operations").mock(
        return_value=Response(404)
    )

    result = await run_pipeline(address, threshold=50)
    assert result["score"] == 0
    assert result["flagged"] is False


@pytest.mark.asyncio
@respx.mock
async def test_pipeline_respects_custom_threshold():
    address = "GMODERATE"
    respx.get(f"{HORIZON_TESTNET_URL}/accounts/{address}/operations").mock(
        return_value=Response(
            200,
            json={
                "_embedded": {
                    "records": [
                        {"created_at": "2026-01-01T00:00:00Z", "to": "GX", "amount": "10"},
                        {"created_at": "2026-01-01T00:05:00Z", "to": "GY", "amount": "12"},
                    ]
                }
            },
        )
    )

    low_threshold_result = await run_pipeline(address, threshold=1)
    high_threshold_result = await run_pipeline(address, threshold=99)
    assert low_threshold_result["flagged"] is True
    assert high_threshold_result["flagged"] is False
