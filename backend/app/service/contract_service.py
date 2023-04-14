from datetime import date
from app.model import Orders, Client, HardwareOrder, Hardware
from jinja2 import Environment, FileSystemLoader
from app.repository.orders import OrdersRepository
from app.repository.client import ClientRepository
from sqlalchemy.sql import select
from app.config import db


class ContractService:

    @staticmethod
    async def get_blank(items: int):
        enviroment = Environment(loader=FileSystemLoader(
            "./templates/"), enable_async=True)

        template = enviroment.get_template("contract.html")

        city = ""

        class Date:
            pass
        order_date = Date()
        order_date.year = ""
        order_date.month = ""
        order_date.day = ""
        months = ["" * 12]
        warehouse = ""
        total = ""
        order_items = [{'Наименование': "", 'Количество': "",
                        'Стоимость': ""} for _ in range(items)]
        taxes = {"total": "", "first_payment": "",
                 "second_payment": ""}
        first_payment = {"percents": "", "amount": ""}
        second_payment = {"percents": "", "amount": ""}
        penalty = {"self": {"day": "", "max": ""},
                   "client": {"day": "", "max": ""}}
        company = {"name": "",
                   "address": "",
                   "postal_address": "",
                   "tin": "",
                   "bank": "",
                   "bik": "",
                   "ks": "",
                   "corr_account": "",
                   "bank_account": ""
                   }
        client = {"name": "",
                  "address": "",
                  "postal_address": "",
                  "tin": ""
                  }

        return await template.render_async(
            city=city,
            order_date=order_date,
            months=months,
            warehouse=warehouse,
            taxes=taxes,
            first_payment=first_payment,
            second_payment=second_payment,
            penalty=penalty,
            company=company,
            client=client,
            order_items=order_items,
            total=total
        )

    @staticmethod
    async def create_contract(order_id: str):

        months = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня',
                  'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']
        order: Orders = await OrdersRepository.get_by_id(order_id)
        client_profile: Client = await ClientRepository.get_by_id(order.user_id)
        query = select(Hardware.name, HardwareOrder.volume, HardwareOrder.value).join_from(
            Hardware, HardwareOrder).where(HardwareOrder.order_id == order_id)
        hardware_orders = (await db.execute(query)).mappings().all()
        order_items = [{'Наименование': item.name, 'Количество': item.volume,
                        'Стоимость': item.value} for item in hardware_orders]

        city: str = "Москва"
        order_date: date = order.created_at
        warehouse = "Москва"
        total = order.total
        taxes = {"total": total * 0.1, "first_payment": total * 0.05,
                 "second_payment": total * 0.05}
        first_payment = {"percents": "50", "amount": total * 0.5}
        second_payment = {"percents": "50", "amount": total * 0.5}
        penalty = {"self": {"day": "2", "max": "50"},
                   "client": {"day": "2", "max": "50"}}
        company = {"name": "ООО Купи Железо",
                   "address": "Москва, Проспект Мира, д.1, корп.1",
                   "postal_address": "Москва, Проспект Мира, д.1, корп.1",
                   "tin": "123456789",
                   "bank": "Банк России",
                   "bik": "123456789",
                   "ks": "123456789",
                   "corr_account": "123456789",
                   "bank_account": "123456789"
                   }
        client = {"name": client_profile.name,
                  "address": client_profile.address,
                  "postal_address": client_profile.postal_address,
                  "tin": client_profile.tin
                  }

        # Создаем HTML-шаблон для PDF-файла

        enviroment = Environment(loader=FileSystemLoader(
            "./templates/"), enable_async=True)

        template = enviroment.get_template("contract.html")

        return await template.render_async(city=city,
                                           order_date=order_date,
                                           months=months,
                                           warehouse=warehouse,
                                           taxes=taxes,
                                           first_payment=first_payment,
                                           second_payment=second_payment,
                                           penalty=penalty,
                                           company=company,
                                           client=client,
                                           order_items=order_items,
                                           total=total)
