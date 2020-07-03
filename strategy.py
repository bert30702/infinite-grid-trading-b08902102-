# Class name must be Strategy
class Strategy():
    def __setitem__(self, key, value):
        self.options[key] = value

    def __getitem__(self, key):
        return self.options.get(key, '')

    def __init__(self):
        self.subscribedBooks = {
            'Bitfinex': {
                'pairs': ['ETH-USDT'],
            },
        }
        self.period = 2
        self.options = {}

        self.last_price = 0.0
        self.BTC_balance = 0.0
        self.USDT_balance = 0.0
    
    def on_order_state_change(state, a) :
        Log('WTF')
    # called every self.period
    def trade(self, information):
        # for single pair strategy, user can choose which exchange/pair to use when launch, get current exchange/pair from information
        exchange = list(information['candles'])[0]
        pair = list(information['candles'][exchange])[0]
        close_price = float(information['candles'][exchange][pair][0]['close'] or 0)

        Log(' : ' + str(self.BTC_balance) + ' ' + str(self.USDT_balance) + ' ' + str(close_price))

        if(close_price <= 1000 or close_price > 20000) :
            Log('WTF close price == ' + str(close_price))
            return []
        
        if(self.last_price == 0) :
            self.last_price = close_price
            self.BTC_balance = 65000 / close_price
            self.USDT_balance = 35000
            return [
                {
                    'exchange': exchange,
                    'amount': 65000 / close_price,
                    'price': -1,
                    'type': 'MARKET',
                    'pair': pair,
                }
            ]
        
        if(close_price / self.last_price - 1 >= 0.01 or close_price / self.last_price - 1 <= -0.01) :
            sell_amount = self.BTC_balance * (close_price / self.last_price - 1)
            if(self.USDT_balance + sell_amount * close_price < 1000) : return []
            if(self.BTC_balance - sell_amount < 0.1)                 : return []

            
            self.BTC_balance -= sell_amount
            self.USDT_balance += sell_amount * close_price
            self.last_price = close_price
            return [
                {
                    'exchange': exchange,
                    'amount': -sell_amount,
                    'price': -1,
                    'type': 'MARKET',
                    'pair': pair,
                }
            ]
        
        return []
