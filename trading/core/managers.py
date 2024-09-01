import requests

from config import BACKEND_URL, api_requests_mapping


class BaseManager:
    @staticmethod
    def get_objects(path: str):
        return requests.get(
            url=f"{BACKEND_URL}{path}"
        ).json()

    @staticmethod
    def get_object(path: str, object_id: str):
        return requests.get(
            url=f"{BACKEND_URL}{path}/{object_id}"
        ).json()

    @staticmethod
    def create_object(path: str, object_data: dict):
        return requests.post(
            url=f"{BACKEND_URL}{path}",
            data=object_data
        ).json()

    @staticmethod
    def update_object(path: str, object_id: str, object_data: dict):
        return requests.patch(
            url=f"{BACKEND_URL}{path}/{object_id}",
            data=object_data
        ).json()

    @staticmethod
    def delete_object(path: str, object_id: str):
        return requests.delete(
            url=f"{BACKEND_URL}{path}/{object_id}"
        ).json()


class DealManager(BaseManager):
    @staticmethod
    def get_deals():
        return super().get_objects(
            path=api_requests_mapping["deals"]
        )

    @staticmethod
    def get_deal(deal_id: str):
        return super().get_object(
            path=api_requests_mapping["deals"],
            object_id=deal_id
        )

    @staticmethod
    def create_deal(deal_data: dict):
        return super().create_object(
            path=api_requests_mapping["deals"],
            object_data=deal_data
        )

    @staticmethod
    def update_deal(deal_id: str, deal_data: dict):
        return super().update_object(
            path=api_requests_mapping["deals"],
            object_id=deal_id,
            object_data=deal_data
        )

    @staticmethod
    def delete_deal(deal_id: str):
        return super().delete_object(
            path=api_requests_mapping["deals"],
            object_id=deal_id
        )


class GridManager(BaseManager):
    @staticmethod
    def get_grids():
        return super().get_objects(
            path=api_requests_mapping["grids"]
        )

    @staticmethod
    def get_grid(grid_id: str):
        return super().get_object(
            path=api_requests_mapping["grids"],
            object_id=grid_id
        )

    @staticmethod
    def create_grid(grid_data: dict):
        return super().create_object(
            path=api_requests_mapping["grids"],
            object_data=grid_data
        )

    @staticmethod
    def update_grid(grid_id: str, grid_data: dict):
        return super().update_object(
            path=api_requests_mapping["grids"],
            object_id=grid_id,
            object_data=grid_data
        )

    @staticmethod
    def delete_grid(grid_id: str):
        return super().delete_object(
            path=api_requests_mapping["grids"],
            object_id=grid_id
        )


class LevelManager(BaseManager):
    @staticmethod
    def get_levels():
        return super().get_objects(
            path=api_requests_mapping["levels"]
        )

    @staticmethod
    def get_level(level_id: str):
        return super().get_object(
            path=api_requests_mapping["levels"],
            object_id=level_id
        )

    @staticmethod
    def create_level(level_data: dict):
        return super().create_object(
            path=api_requests_mapping["levels"],
            object_data=level_data
        )

    @staticmethod
    def update_level(level_id: str, level_data: dict):
        return super().update_object(
            path=api_requests_mapping["levels"],
            object_id=level_id,
            object_data=level_data
        )

    @staticmethod
    def delete_level(level_id: str):
        return super().delete_object(
            path=api_requests_mapping["levels"],
            object_id=level_id
        )


class TickerManager(BaseManager):
    @staticmethod
    def get_tickers():
        return super().get_objects(
            path=api_requests_mapping["tickers"]
        )

    @staticmethod
    def get_ticker(ticker_id: str):
        return super().get_object(
            path=api_requests_mapping["tickers"],
            object_id=ticker_id
        )

    @staticmethod
    def create_ticker(ticker_data: dict):
        return super().create_object(
            path=api_requests_mapping["tickers"],
            object_data=ticker_data
        )

    @staticmethod
    def update_ticker(ticker_id: str, ticker_data: dict):
        return super().update_object(
            path=api_requests_mapping["tickers"],
            object_id=ticker_id,
            object_data=ticker_data
        )

    @staticmethod
    def delete_ticker(ticker_id: str):
        return super().delete_object(
            path=api_requests_mapping["tickers"],
            object_id=ticker_id
        )


class TraderManager(BaseManager):
    @staticmethod
    def get_traders():
        return super().get_objects(
            path=api_requests_mapping["traders"]
        )

    @staticmethod
    def get_trader(trader_id: str):
        return super().get_object(
            path=api_requests_mapping["traders"],
            object_id=trader_id
        )

    @staticmethod
    def create_trader(trader_data: dict):
        return super().create_object(
            path=api_requests_mapping["traders"],
            object_data=trader_data
        )

    @staticmethod
    def update_trader(trader_id: str, trader_data: dict):
        return super().update_object(
            path=api_requests_mapping["traders"],
            object_id=trader_id,
            object_data=trader_data
        )

    @staticmethod
    def delete_trader(trader_id: str):
        return super().delete_object(
            path=api_requests_mapping["traders"],
            object_id=trader_id
        )
