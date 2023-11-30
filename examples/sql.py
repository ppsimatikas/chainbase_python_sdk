from chainbase_sdk import Chainbase

client = Chainbase()
df = client.sql.query_pandas("select * from ethereum.blocks limit 10")
print(df)