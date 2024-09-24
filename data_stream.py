import time
from AccessToken import token

from tinkoff.invest import (
    CandleInstrument,
    Client,
    MarketDataRequest,
    SubscribeCandlesRequest,
    SubscriptionAction,
    SubscriptionInterval,
)

TOKEN = token

def checkTradingStatus(figi_lists, client):
    newFigiLists = []
    for figis in figi_lists:
        if (client.market_data.get_trading_status(figi = figis, instrument_id = figis).trading_status == 5):
            # 5 - нормальная торговля
            newFigiLists.append(figis)
            print("Торговля доступна", f"Figi: {figis}")
        else:
            print("Торговля НЕДОСТУПНА", f"Figi: {figis}")
    return newFigiLists
      

def data():
    def request_iterator():
        yield MarketDataRequest(
            subscribe_candles_request=SubscribeCandlesRequest(
                waiting_close=True,
                subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                instruments=[
                    CandleInstrument(figi=figi, interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,) for figi in checkTradingStatus(figi_lists, client)],
        )
    )
        while True:
            time.sleep(1)

    with Client(TOKEN) as client:

        figi_lists = ["BBG004730ZJ9", "BBG000000001", "BBG006L8G4H1", "TCS00A105EX7", "BBG0100R9963", "BBG004731032", "TCS00A106YF0", "BBG000QJW156"]

        for marketdata in client.market_data_stream.market_data_stream(
            request_iterator()
        ):
            candle = marketdata.candle
            if candle:
                close_price = candle.close.units + candle.close.nano * 10**(-9)
                timeOpenCandle = candle.time
                
                response = [candle.figi, round(close_price, 2), timeOpenCandle]
                yield response #отправка данных
    

    
       
if __name__ == "__main__":
    data()
    
    
