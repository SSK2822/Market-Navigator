import unittest
import pandas as pd
import numpy as np
import data_processing
from unittest.mock import patch
import data_fetching

class Tests(unittest.TestCase):
    # Testing functions from data_fetching.py
    def test_fetch_historical_data_format(self):
        with patch('data_fetching.requests.get') as mock_get, patch('data_fetching.cache_data') as mock_cache:
            mock_get.return_value.json.return_value = {
                "Time Series (Daily)": {
                    "2023-05-01": {"1. open": "135.0", "4. close": "140.0"}
                }
            }
            result = data_fetching.fetch_historical_data("AAPL")
            self.assertIsInstance(result, dict)
            self.assertIn("Time Series (Daily)", result)

    def test_fetch_historical_data_error(self):
        with self.assertRaises(ValueError):
            data_fetching.fetch_historical_data("XYZ")

    def test_get_data_frame(self):
        data = {
            "Time Series (Daily)": {
                "2023-05-01": {"open": 135.0, "close": 140.0}
            }
        }
        df = data_fetching.get_data_frame(data)
        self.assertIsInstance(df, pd.DataFrame)


    def test_fetch_fundamental_data_format(self):
        with patch('data_fetching.yf.Ticker') as mock_ticker:
            mock_ticker.return_value.info = {
                "trailingEps": 10.5, "debtToEquity": 50, "trailingPE": 30, "returnOnEquity": 15,
                "dividendYield": 0.005, "marketCap": 1000000000, "profitMargins": 0.1
            }
            result = data_fetching.fetch_fundamental_data("AAPL")
            self.assertIsInstance(result, dict)
            self.assertIn("EPS", result)
            self.assertEqual(result["EPS"], 6.43)  # value changes over time (check internet for the latest value)

    # Testing functions from data_processing.py
    def setUp(self):
        # Create a sample DataFrame for the tests
        self.df = pd.DataFrame({
            'high': np.random.random(100) + 100,
            'low': np.random.random(100) + 99,
            'close': np.random.random(100) + 99.5
        })

    def test_calculate_ath(self):
        self.assertEqual(data_processing.calculate_ath(self.df), self.df['high'].max())

    def test_calculate_atl(self):
        self.assertEqual(data_processing.calculate_atl(self.df), self.df['low'].min())

    def test_calculate_ema(self):
        ema = data_processing.calculate_ema(self.df)
        self.assertTrue(isinstance(ema, pd.Series))
        self.assertEqual(len(ema), len(self.df))

    def test_calculate_sma(self):
        sma = data_processing.calculate_sma(self.df)
        self.assertTrue(isinstance(sma, pd.Series))
        self.assertEqual(len(sma), len(self.df))

    def test_calculate_atr(self):
        atr = data_processing.calculate_atr(self.df)
        self.assertTrue(isinstance(atr, pd.Series))
        self.assertEqual(len(atr), len(self.df))

    def test_calculate_market_movement(self):
        movement = data_processing.calculate_market_movement(self.df)
        self.assertTrue(isinstance(movement, pd.Series))
        self.assertEqual(len(movement), len(self.df))

    def test_calculate_loss_percent(self):
        loss = data_processing.calculate_loss_percent(self.df)
        self.assertTrue(isinstance(loss, pd.Series))
        self.assertEqual(len(loss), len(self.df))

    def test_calculate_profit_percent(self):
        profit = data_processing.calculate_profit_percent(self.df)
        self.assertTrue(isinstance(profit, pd.Series))
        self.assertEqual(len(profit), len(self.df))

    def test_calculate_roc(self):
        roc = data_processing.calculate_roc(self.df)
        self.assertTrue(isinstance(roc, pd.Series))
        self.assertEqual(len(roc), len(self.df))

    def test_calculate_rsi(self):
        rsi = data_processing.calculate_rsi(self.df)
        self.assertTrue(isinstance(rsi, pd.Series))
        self.assertEqual(len(rsi), len(self.df))

    def test_calculate_swing_percent(self):
        swing = data_processing.calculate_swing_percent(self.df)
        self.assertTrue(isinstance(swing, pd.Series))
        self.assertEqual(len(swing), len(self.df))

    def test_extract_close_prices(self):
        close_prices = data_processing.extract_close_prices(self.df)
        self.assertTrue(isinstance(close_prices, pd.DataFrame))
        self.assertTrue('close' in close_prices.columns)
        self.assertTrue('date' in close_prices.columns)

if __name__ == "__main__":
    unittest.main()
