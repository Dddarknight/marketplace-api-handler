from datetime import datetime

from pydantic import BaseModel, Field, condecimal


class Common(BaseModel):
    date: datetime = Field()
    last_change_date: datetime = Field(validation_alias='lastChangeDate')
    warehouse_name: str = Field(validation_alias='warehouseName')
    country_name: str = Field(validation_alias='countryName')
    oblast_okrug_name: str = Field(validation_alias='oblastOkrugName')
    region_name: str = Field(validation_alias='regionName')
    supplier_article: int = Field(validation_alias='supplierArticle')
    nm_id: int = Field(validation_alias='nmId')
    barcode: str = Field()
    category: str = Field()
    subject: str = Field()
    brand: str = Field()
    tech_size: str = Field(validation_alias='techSize')
    income_id: int = Field(validation_alias='incomeID')
    is_supply: bool = Field(validation_alias='isSupply')
    is_realization: bool = Field(validation_alias='isRealization')
    total_price: condecimal(gt=0) = Field(validation_alias='totalPrice')
    discount_percent: int = Field(validation_alias='discountPercent')
    spp: int = Field()
    finished_price: condecimal(gt=0) = Field(validation_alias='finishedPrice')
    price_with_disc: condecimal(gt=0) = Field(validation_alias='priceWithDisc')
    order_type: str = Field(validation_alias='orderType')
    sticker: str = Field()
    g_number: str = Field(validation_alias='gNumber')
    srid: str = Field()


class OrderModel(Common):
    is_cancel: bool = Field(validation_alias='isCancel')
    cancel_date: datetime = Field(validation_alias='cancelDate')

    def to_orm_model(self):
        return {
            'srid': self.srid,
            'date': self.date,
            'last_change_date': self.last_change_date,
            'warehouse_name': self.warehouse_name,
            'country_name': self.country_name,
            'oblast_okrug_name': self.oblast_okrug_name,
            'region_name': self.region_name,
            'nm_id': self.nm_id,
            'income_id': self.income_id,
            'is_supply': self.is_supply,
            'is_realization': self.is_realization,
            'total_price': self.total_price,
            'discount_percent': self.discount_percent,
            'spp': self.spp,
            'finished_price': self.finished_price,
            'price_with_disc': self.price_with_disc,
            'order_type': self.order_type,
            'sticker': self.sticker,
            'g_number': self.g_number,
            'is_cancel': self.is_cancel,
            'cancel_date': self.cancel_date,
        }

    def extract_product_data(self):
        return {
            'supplier_article': self.supplier_article,
            'nm_id': self.nm_id,
            'barcode': self.barcode,
            'category': self.category,
            'subject': self.subject,
            'brand': self.brand,
            'tech_size': self.tech_size,
        }


class SalesModel(Common):
    payment_sale_amount: int = Field(validation_alias='paymentSaleAmount')
    for_pay: condecimal(gt=0) = Field(validation_alias='forPay')
    sale_id: str = Field(validation_alias='saleID')

    def to_orm_model(self):
        return {
            'sale_id': self.sale_id,
            'payment_sale_amount': self.payment_sale_amount,
            'for_pay': self.for_pay,
            'srid': self.srid,
        }
