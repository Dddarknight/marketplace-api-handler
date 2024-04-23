import pandas as pd

from src.responses_schemas import OrderModel, SalesModel


class FileHandler:
    def __init__(self):
        ...

    async def save_to_excel(self, orders: list[OrderModel], sales: list[SalesModel], name: str):
        """Saves data to the Excel file."""
        orders_data = pd.DataFrame(
            [order.model_dump() for order in orders],
            columns=OrderModel.model_fields,
        )
        sales_data = pd.DataFrame(
            [sales_item.model_dump() for sales_item in sales],
            columns=SalesModel.model_fields,
        )
        with pd.ExcelWriter(name, engine='openpyxl') as writer:
            orders_data.to_excel(writer, sheet_name='Orders', index=False)
            sales_data.to_excel(writer, sheet_name='Sales', index=False)
