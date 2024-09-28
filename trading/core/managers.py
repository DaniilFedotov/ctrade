import requests

from config import BACKEND_URL, api_requests_mapping


class BaseManager:
    @staticmethod
    def get_objects(path: str):
        return requests.get(
            url=f"{BACKEND_URL}{path}/"
        ).json()

    @staticmethod
    def get_object(path: str, object_id: str):
        return requests.get(
            url=f"{BACKEND_URL}{path}/{object_id}/"
        ).json()

    @staticmethod
    def create_object(path: str, object_data: dict):
        return requests.post(
            url=f"{BACKEND_URL}{path}/",
            data=object_data
        ).json()

    @staticmethod
    def update_object(path: str, object_id: str, object_data: dict):
        return requests.patch(
            url=f"{BACKEND_URL}{path}/{object_id}/",
            data=object_data
        )

    @staticmethod
    def delete_object(path: str, object_id: str):
        return requests.delete(
            url=f"{BACKEND_URL}{path}/{object_id}/"
        )


class DealManager(BaseManager):
    @classmethod
    def get_deals(cls):
        return super().get_objects(
            path=api_requests_mapping["deals"]
        )

    @classmethod
    def get_deal(cls, deal_id: str):
        return super().get_object(
            path=api_requests_mapping["deals"],
            object_id=deal_id
        )

    @classmethod
    def create_deal(cls, deal_data: dict):
        return super().create_object(
            path=api_requests_mapping["deals"],
            object_data=deal_data
        )

    @classmethod
    def update_deal(cls, deal_id: str, deal_data: dict):
        return super().update_object(
            path=api_requests_mapping["deals"],
            object_id=deal_id,
            object_data=deal_data
        )

    @classmethod
    def delete_deal(cls, deal_id: str):
        return super().delete_object(
            path=api_requests_mapping["deals"],
            object_id=deal_id
        )


class GridManager(BaseManager):
    @classmethod
    def get_grids(cls):
        return super().get_objects(
            path=api_requests_mapping["grids"]
        )

    @classmethod
    def get_grid(cls, grid_id: str):
        return super().get_object(
            path=api_requests_mapping["grids"],
            object_id=grid_id
        )

    @classmethod
    def create_grid(cls, grid_data: dict):
        return super().create_object(
            path=api_requests_mapping["grids"],
            object_data=grid_data
        )

    @classmethod
    def update_grid(cls, grid_id: str, grid_data: dict):
        return super().update_object(
            path=api_requests_mapping["grids"],
            object_id=grid_id,
            object_data=grid_data
        )

    @classmethod
    def delete_grid(cls, grid_id: str):
        return super().delete_object(
            path=api_requests_mapping["grids"],
            object_id=grid_id
        )


class LevelManager(BaseManager):
    @classmethod
    def get_levels(cls):
        return super().get_objects(
            path=api_requests_mapping["levels"]
        )

    @classmethod
    def get_level(cls, level_id: str):
        return super().get_object(
            path=api_requests_mapping["levels"],
            object_id=level_id
        )

    @classmethod
    def create_level(cls, level_data: dict):
        return super().create_object(
            path=api_requests_mapping["levels"],
            object_data=level_data
        )

    @classmethod
    def update_level(cls, level_id: str, level_data: dict):
        return super().update_object(
            path=api_requests_mapping["levels"],
            object_id=level_id,
            object_data=level_data
        )

    @classmethod
    def delete_level(cls, level_id: str):
        return super().delete_object(
            path=api_requests_mapping["levels"],
            object_id=level_id
        )


class TickerManager(BaseManager):
    @classmethod
    def get_tickers(cls):
        return super().get_objects(
            path=api_requests_mapping["tickers"]
        )

    @classmethod
    def get_ticker(cls, ticker_id: str):
        return super().get_object(
            path=api_requests_mapping["tickers"],
            object_id=ticker_id
        )

    @classmethod
    def create_ticker(cls, ticker_data: dict):
        return super().create_object(
            path=api_requests_mapping["tickers"],
            object_data=ticker_data
        )

    @classmethod
    def update_ticker(cls, ticker_id: str, ticker_data: dict):
        return super().update_object(
            path=api_requests_mapping["tickers"],
            object_id=ticker_id,
            object_data=ticker_data
        )

    @classmethod
    def delete_ticker(cls, ticker_id: str):
        return super().delete_object(
            path=api_requests_mapping["tickers"],
            object_id=ticker_id
        )


class TraderManager(BaseManager):
    @classmethod
    def get_traders(cls):
        return super().get_objects(
            path=api_requests_mapping["traders"]
        )

    @classmethod
    def get_trader(cls, trader_id: str):
        return super().get_object(
            path=api_requests_mapping["traders"],
            object_id=trader_id
        )

    @classmethod
    def create_trader(cls, trader_data: dict):
        return super().create_object(
            path=api_requests_mapping["traders"],
            object_data=trader_data
        )

    @classmethod
    def update_trader(cls, trader_id: str, trader_data: dict):
        return super().update_object(
            path=api_requests_mapping["traders"],
            object_id=trader_id,
            object_data=trader_data
        )

    @classmethod
    def delete_trader(cls, trader_id: str):
        return super().delete_object(
            path=api_requests_mapping["traders"],
            object_id=trader_id
        )
