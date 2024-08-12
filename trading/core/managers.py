import requests

from config import BACKEND_URL, api_requests_mapping


class BaseManager:
    def get_objects(self, path: str):
        return requests.get(
            url=f"{BACKEND_URL}{path}"
        ).json()

    def get_object(self, path: str, object_id: str):
        return requests.get(
            url=f"{BACKEND_URL}{path}/{object_id}"
        ).json()

    def create_object(self, path: str, object_data: dict):
        return requests.post(
            url=f"{BACKEND_URL}{path}",
            data=object_data
        ).json()

    def update_object(self, path: str, object_id: str, object_data: dict):
        return requests.patch(
            url=f"{BACKEND_URL}{path}/{object_id}",
            data=object_data
        ).json()

    def delete_object(self, path: str, object_id: str):
        return requests.delete(
            url=f"{BACKEND_URL}{path}/{object_id}"
        ).json()


class DealManager(BaseManager):
    def __init__(self):
        self.path = api_requests_mapping["deals"]

    def get_deals(self):
        return super().get_objects(
            path=self.path
        )

    def get_deal(self, deal_id: str):
        return super().get_object(
            path=self.path,
            object_id=deal_id
        )

    def create_deal(self, deal_data: dict):
        return super().create_object(
            path=self.path,
            object_data=deal_data
        )

    def update_deal(self, deal_id: str, deal_data: dict):
        return super().update_object(
            path=self.path,
            object_id=deal_id,
            object_data=deal_data
        )

    def delete_deal(self, deal_id: str):
        return super().delete_object(
            path=self.path,
            object_id=deal_id
        )


class GridManager(BaseManager):
    def __init__(self):
        self.path = api_requests_mapping["grids"]

    def get_grids(self):
        return super().get_objects(
            path=self.path
        )

    def get_grid(self, grid_id: str):
        return super().get_object(
            path=self.path,
            object_id=grid_id
        )

    def create_grid(self, grid_data: dict):
        return super().create_object(
            path=self.path,
            object_data=grid_data
        )

    def update_grid(self, grid_id: str, grid_data: dict):
        return super().update_object(
            path=self.path,
            object_id=grid_id,
            object_data=grid_data
        )

    def delete_grid(self, grid_id: str):
        return super().delete_object(
            path=self.path,
            object_id=grid_id
        )


class LevelManager(BaseManager):
    def __init__(self):
        self.path = api_requests_mapping["levels"]

    def get_levels(self):
        return super().get_objects(
            path=self.path
        )

    def get_level(self, level_id: str):
        return super().get_object(
            path=self.path,
            object_id=level_id
        )

    def create_level(self, level_data: dict):
        return super().create_object(
            path=self.path,
            object_data=level_data
        )

    def update_level(self, level_id: str, level_data: dict):
        return super().update_object(
            path=self.path,
            object_id=level_id,
            object_data=level_data
        )

    def delete_level(self, level_id: str):
        return super().delete_object(
            path=self.path,
            object_id=level_id
        )


class TickerManager(BaseManager):
    def __init__(self):
        self.path = api_requests_mapping["tickers"]

    def get_tickers(self):
        return super().get_objects(
            path=self.path
        )

    def get_ticker(self, ticker_id: str):
        return super().get_object(
            path=self.path,
            object_id=ticker_id
        )

    def create_ticker(self, ticker_data: dict):
        return super().create_object(
            path=self.path,
            object_data=ticker_data
        )

    def update_ticker(self, ticker_id: str, ticker_data: dict):
        return super().update_object(
            path=self.path,
            object_id=ticker_id,
            object_data=ticker_data
        )

    def delete_ticker(self, ticker_id: str):
        return super().delete_object(
            path=self.path,
            object_id=ticker_id
        )


class TraderManager(BaseManager):
    def __init__(self):
        self.path = api_requests_mapping["traders"]

    def get_traders(self):
        return super().get_objects(
            path=self.path
        )

    def get_trader(self, trader_id: str):
        return super().get_object(
            path=self.path,
            object_id=trader_id
        )

    def create_trader(self, trader_data: dict):
        return super().create_object(
            path=self.path,
            object_data=trader_data
        )

    def update_trader(self, trader_id: str, trader_data: dict):
        return super().update_object(
            path=self.path,
            object_id=trader_id,
            object_data=trader_data
        )

    def delete_trader(self, trader_id: str):
        return super().delete_object(
            path=self.path,
            object_id=trader_id
        )
