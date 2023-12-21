from abc import ABCMeta, abstractmethod


class IObserver(metaclass=ABCMeta):
    @abstractmethod
    def notify(self, rival, amount, product):
        pass


class IObservable(metaclass=ABCMeta):
    @abstractmethod
    def add_observer(self, observer: IObserver):
        pass

    @abstractmethod
    def remove_observer(self, observer: IObserver):
        pass

    @abstractmethod
    def notify_observers(self):
        pass


class DeliveryStrategy:
    # я решил сделать данный метод абстрактным, ведь оне все равно должен быть переписан во всех случаях
    # а так же статическим так как он все равно не будет использовать self
    @staticmethod
    @abstractmethod
    def notification_about_delivery(name):
        pass


# классы доставки
class CourierDeliveryStrategy(DeliveryStrategy):
    @staticmethod
    def notification_about_delivery(name):
        print(f"{name}'s delivery ll be performed by Drevnii Rus Courier Delivery")


class PostDeliveryStrategy(DeliveryStrategy):
    @staticmethod
    def notification_about_delivery(name):
        print(f"{name}'s delivery ll be performed by Drevnii Rus Post Delivery")


class PickupDeliveryStrategy(DeliveryStrategy):
    @staticmethod
    def notification_about_delivery(name):
        print(f"{name}'s delivery ll be performed by {name}")


class IProduct(IObservable):
    def __init__(self, name, price, discount, amount):
        self.name = name
        self.price = price
        self.discount = discount
        self.amount = amount
        self.observers = []

    def to_buy(self, amount):
        self.amount -= amount

    def get_name(self):
        return self.name

    def get_amount(self):
        return self.amount

    def add_observer(self, observer: IObserver):
        self.observers.append(observer)

    def remove_observer(self, observer: IObserver):
        self.observers.remove(observer)

    def get_observers(self) -> list:
        return self.observers

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.amount, self.name)


# классы продуктов
class Negr(IProduct):
    def __init__(self):
        super().__init__('Негр', 100, 50, 42020743)


class Rtx400080(IProduct):
    def __init__(self):
        super().__init__('Nvidia GeForce RTX400080', 400080**2, 0, 2)


class JoJo(IProduct):
    def __init__(self):
        super().__init__('ジョジョの奇妙な冒険 Part9:The JoJoLands', 1000, 0, 100)


class PutinsPortrait(IProduct):
    def __init__(self):
        super().__init__('Портрет президента Российской Федерации Владимира Владимировича Путина', 28070988, 0, 1952)


class ProductFactory:
    @staticmethod
    def get_in_stock(product_type: str):
        if product_type.lower() == 'negr':
            return Negr()
        if product_type.lower() == 'rtx400080':
            return Rtx400080()
        if product_type.lower() == 'jojo':
            return JoJo()
        if product_type.lower() == 'putins portrait':
            return PutinsPortrait()
        ValueError("There is no such type of product")


class Customer(IObserver):
    def __init__(self, name, nationality):
        self.name = name
        self.nationality = nationality
        self.observable_products = []
        self.ordered = []
        self.delivery = []

    def get_name(self):
        return self.name

    def get_nationality(self):
        return self.nationality

    def add_product(self, product):
        self.observable_products.append(product)

    def add_to_ordered(self, product: IProduct, delivery: DeliveryStrategy, amount):
        print(f'{self.name} successfully ordered {product.get_name()}x{amount}')
        self.delivery.append(delivery)
        self.remove_product(product)
        self.ordered.append(product)

    def remove_product(self, product):
        self.observable_products.remove(product)

    def get_products(self):
        return self.observable_products

    def notify(self, rival, amount, product):
        print(f"there is only {amount} of {product} to buy now,",
              f"{self.name} shall hust to get some of {product},",
              f"while its still in stock and {rival} not bought some more",
              f"or {self.name} will lose chance to get so precious and",
              f"adorable {product} in own posession, our dear and gracious",
              f"dedicated {self.name} thou ll regret of {self.name}'s fate without our {product}",
              sep='\n')


class Shop:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        else:
            print('our shop is only one in that program, others shall perish before being born')
        return cls.__instance

    def __init__(self):
        self.customers = []
        self.products = []
        self.orderers = []

    def add_product(self, product: IProduct):
        self.products.append(product)

    def add_customer(self, customer: Customer):
        self.customers.append(customer)

    def remove_customer(self, customer: Customer):
        self.customers.remove(customer)

    def add_orderer(self, orderer: Customer):
        self.orderers.append(orderer)

    def set_customer_to_product_as_observer(self, customer: Customer, product: IProduct):
        self.customers.append(customer)
        self.products.append(product)
        customer.add_product(product)
        product.add_observer(customer)

    def get_customers(self):
        return self.customers

    def get_products(self):
        return self.products

    def to_order(self, customer: Customer, amount: int, product: IProduct, delivery: DeliveryStrategy):
        if customer in product.get_observers():
            if product.get_amount() >= amount:
                customer.add_to_ordered(product, delivery, amount)
                delivery.notification_about_delivery(customer.get_name())
                self.orderers.append(customer)
                self.remove_customer(customer)
                product.remove_observer(customer)
                product.to_buy(amount)
                for customers in product.get_observers():
                    customers.notify(customer.get_name(), product.get_amount(), product.get_name())
            else:
                print(f'the whole shop shall regret that {product.get_name()}',
                      f'll not be sold to {customer.get_name()}',
                      f'since our shop dont have enough quantity of {product.get_name()} in stock',
                      sep='\n')
        else:
            if customer.get_nationality() != 'yastcher':
                print(f'{customer.get_name()} shall not have the {product.get_name()} because he is not interested '
                      f'in {product.get_name()}')
            else:
                print(f'{customer.get_name()} shall not have the {product.get_name()} cuz he is not interested '
                      f'in {product.get_name()} and he is ever yastcher, tho ll be defeated by '
                      f'slavyanskii zathzim yaicami')


if __name__ == '__main__':
    # магазин и фабрика
    factory = ProductFactory()
    shop = Shop()
    shop2 = Shop()
    # продукты
    negr = factory.get_in_stock('negr')
    videockard = factory.get_in_stock('RTX400080')
    jojo = factory.get_in_stock('jojo')
    portrait = factory.get_in_stock('Putins portrait')
    # покупатель
    rus0 = Customer('Сварогов Дубомир Славянович', 'slavic')
    yastcher = Customer('Зверобогов Ящур Питонович', 'yastcher')
    rus1 = Customer('Ярилов Богдан Перунович', 'slavic')
    # процесс
    shop.set_customer_to_product_as_observer(rus0, portrait)
    shop.set_customer_to_product_as_observer(rus1, portrait)
    shop.to_order(yastcher, 1952, portrait, PostDeliveryStrategy)
    shop.to_order(rus0, 1951, portrait, PickupDeliveryStrategy)
    shop.to_order(rus1, 2, portrait, CourierDeliveryStrategy)
