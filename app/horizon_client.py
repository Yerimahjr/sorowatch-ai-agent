"""
Thin client for Stellar Horizon (used to gather account activity for
scoring). Uses the public Horizon API rather than Soroban RPC directly,
since Horizon exposes payment/operation history in a form that's easy to
score, whereas Soroban RPC is oriented around contract events.
"""
import httpx

HORIZON_TESTNET_URL = "https://horizon-testnet.stellar.org"


class HorizonClient:
    def __init__(self, base_url: str = HORIZON_TESTNET_URL, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def get_recent_operations(self, address: str, limit: int = 50) -> list[dict]:
        """
        Fetch the most recent operations for an address. Returns an empty
        list if the account doesn't exist yet (common for freshly-created
        testnet addresses) rather than raising, since "no history" is a
        valid input to the risk scorer.
        """
        url = f"{self.base_url}/accounts/{address}/operations"
        params = {"order": "desc", "limit": limit}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, params=params)
            if response.status_code == 404:
                return []
            response.raise_for_status()
            data = response.json()
            return data.get("_embedded", {}).get("records", [])
