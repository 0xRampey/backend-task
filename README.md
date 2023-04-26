# Sample requests
```
curl "http://localhost:8000/call_contract?contract_address=0xdac17f958d2ee523a2206206994597c13d831ec7&function_name=balanceOf&arguments=['0x742d35Cc6634C0532925a3b844Bc454e4438f44e']" -g

curl "http://localhost:5000/call_contract?contract_address=0xdac17f958d2ee523a2206206994597c13d831ec7&function_name=decimals&arguments=[]" -g

# Proxy contract
curl "http://localhost:8000/call_contract?contract_address=0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48&function_name=balanceOf&arguments=['0x742d35Cc6634C0532925a3b844Bc454e4438f44e']" -g
```
