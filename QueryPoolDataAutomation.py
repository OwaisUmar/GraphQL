from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import mysql.connector
import datetime

sample_transport = AIOHTTPTransport(
    url='https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'
)

client = Client(
    transport=sample_transport
)

query = gql('''
{
  poolDayDatas(first: 1000, orderBy: date, orderDirection: desc, where: {
    pool: "0x1d42064fc4beb5f8aaf85f4617ae8b3b5b8bd801", tick_not: null} ) {
    date
    pool{
      token0{
        symbol
        name
      }
      token1 {
        symbol
        name
      }
    }
    id
    liquidity
    sqrtPrice
    token0Price
    token1Price
    tick
    feeGrowthGlobal0X128
    feeGrowthGlobal1X128
    tvlUSD
    volumeToken0
    volumeToken1
    volumeUSD 
    feesUSD   
    txCount
    open
    high
    low
    close
  }
}
''')

response = client.execute(query)

pairs = []
for i in response['poolDayDatas']:
    pairs.append([
        i['id'],
        datetime.date.fromtimestamp(i['date']).isoformat(),
        i['pool']['token0']['name'],
        i['pool']['token1']['name'],
        i['pool']['token0']['symbol'] + '-' + i['pool']['token1']['symbol'],
        i['liquidity'],
        i['sqrtPrice'],
        i['token0Price'],
        i['token1Price'],
        i['tick'],
        i['feeGrowthGlobal0X128'],
        i['feeGrowthGlobal1X128'],
        i['tvlUSD'],
        i['volumeToken0'],
        i['volumeToken1'],
        i['volumeUSD'],
        i['feesUSD'],
        i['txCount'],
        i['open'],
        i['high'],
        i['low'],
        i['close']
    ])

columns = ['ID', 'Date', 'Token1', 'Token2', 'Pair', 'Liquidity', 'sqrtPrice',
           'token1Price', 'token2Price', 'tick', 'feeGrowthGlobal1X128',
           'feeGrowthGlobal2X128', 'tvlUSD', 'volumeToken1', 'volumeToken2',
           'volumeUSD', 'feesUSD', 'txCount', 'open', 'high', 'low', 'close', ]


# connecting to MySQL database:
mydb = mysql.connector.connect(
    # host='127.0.0.1',
    user='root',
    password='owais',
    # port='3306',
    database='trading_db'
)

create = 'create table pool_data (\n'  # Query string to create table
for col in columns:
    create += col + ' '
    if col == 'Date':
        create += 'date,\n'
    else:
        create += 'varchar(255),\n'
create = create + 'PRIMARY KEY (ID)\n)'

mycur = mydb.cursor()
mycur.execute(create)     # query to create table


insertDataQueries = ["insert into pool_data values('" + "', '".join(x) + "')" for x in pairs]
for insertQuery in insertDataQueries:
    mycur.execute(insertQuery)
    mydb.commit()

