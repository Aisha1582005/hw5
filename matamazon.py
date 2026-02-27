# TODO add all imports needed here
import json


class InvalidIdException(Exception):
    pass


class InvalidPriceException(Exception):
    pass


class Customer:
    class Customer:
        def __init__(self, id, name, city, address):
            if id < 0 or not isinstance(id, int):
                raise InvalidIdException("Id is not legal")
            self.id = id
            self.name = name
            self.city = city
            self.address = address

        def __str__(self):
            return f"Product(id={self.id}, name='{self.name}', city='{self.city}', address='{self.address}')"

    # TODO implement this class as instructed
    pass


class Supplier:
    def __init__(self, id, name, city, address):
        if id < 0 or not isinstance(id, int):
            raise InvalidIdException("Id is illegal")
        self.id = id
        self.name = name
        self.city = city
        self.address = address

    def __str__(self):
        return f"Supplier(id={self.id}, name='{self.name}', city='{self.city}', address='{self.address}')"

    # TODO implement this class as instructed
    pass


class Product:
    def __init__(self, id, name, price, supplier_id, quantity):
        if id < 0 or not isinstance(id, int) or not isinstance(supplier_id, int) or supplier_id < 0:
            raise InvalidIdException("Id is not legal")
        if (price < 0):
            raise InvalidPriceException("price is negative")
        self.id = id
        self.name = name
        self.price = price
        self.supplier_id = supplier_id
        self.quantity = quantity

    def __str__(self):
        return "Product(id={self.id}, name='{self.name}', price='{self.price}', supplier_id='{self.supplier_id}', quantity='{self.quantity}')"

    # TODO implement this class as instructed
    pass


class Order:
    def __init__(self, id, customer_id, product_id, quantity, total_price):
        if (id < 0 or not isinstance(id, int) or not isinstance(customer_id, int) or
                not isinstance(product_id, int) or customer_id < 0 or product_id < 0):
            raise InvalidIdException("Id is not legal")
        if total_price < 0 or not isinstance(total_price, float):
            raise InvalidPriceException("price is negative")
        self.id = id
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity
        self.total_price = total_price

    def __str__(self):
        return "Order({self.id}, {self.customer_id}, {self.product_id}, {self.quantity}, {self.total_price})"

    # TODO implement this class as instructed
    pass


class MatamazonSystem:
    """
    Main system class that stores and manages customers, suppliers, products and orders.

    The system must support:
        - Registering customers/suppliers (with unique IDs across both types).
        - Adding/updating products (must validate supplier existence).
        - Placing orders (validate product existence and stock).
        - Removing objects by ID and type (with dependency constraints).
        - Searching products by name/query and optional max price.
        - Exporting system state to a text file (customers/suppliers/products only).
        - Exporting orders to JSON grouped by supplier origin city.

    Notes:
        - The specification does not require specific internal fields. Any data structures are allowed,
          as long as the behaviors match the spec.
        - A parameterless constructor is required.
    """

    def __init__(self):
        self.customers = {}
        self.suppliers = {}
        self.products = {}
        self.orders = {}
        self.order_id = 1

        # TODO implement this method if needed

    pass

    def register_entity(self, entity, is_customer):
        if is_customer:
            if entity.id in self.customers:
                raise InvalidIdException("Customer already exists")

            self.customers[entity.id] = entity
        else:
            if entity.id in self.suppliers:
                raise InvalidIdException("Customer already exists")

            self.suppliers[entity.id] = entity
        # TODO implement this method as instructed
        pass

    def add_or_update_entity(self, entity):
        if entity.id in self.products:
            if self.products[entity.id].supplier_id != entity.supplier_id:
                raise InvalidIdException("Suppliers does not match")
            else:
                self.products[entity.id].name = entity.name
                self.products[entity.id].price = entity.price
                self.products[entity.id].quantity = entity.quantity
        else:
            self.products[entity.id] = entity

        # TODO implement this method as instructed

    pass

    def place_order(self, customer_id, product_id, quantity=1):
        if customer_id not in self.customers:
            raise InvalidIdException("Customer does not exist")
        if product_id in self.products:
            if self.products[product_id].quantity >= quantity:
                self.products[product_id].quantity -= quantity
                total_price = self.products[product_id].price * quantity
                self.orders[self.order_id] = Order(self.order_id, customer_id, product_id, quantity, total_price)
                self.order_id += 1
                return "The order has been accepted in the system"
            else:
                return "The quantity requested for this product is greater than the quantity in stock"
        else:
            return "The product does not exist in the system"

    """
    Place an order for a product by a customer.

    Args:
        customer_id (int): Customer ID.
        product_id (int): Product ID.
        quantity (int, optional): Quantity to order. Defaults to 1.

    Returns:
        str: Status message according to specification:
            - "The order has been accepted in the system"
            - "The product does not exist in the system"
            - "The quantity requested for this product is greater than the quantity in stock"

    Behavior:
        - If product does not exist: return the relevant message.
        - If quantity requested > stock: return the relevant message.
        - Otherwise:
            - Decrease product stock by quantity.
            - Create a new Order with an auto-incremented system ID (starting at 1).
            - Store the order in the system.
            - Return success message.

    Notes:
        - The specification assumes quantity is an integer.
    """
    # TODO implement this method as instructed
    pass


def remove_object(self, _id, class_type):
    if not isinstance(_id, int) or _id < 0:
        raise InvalidIdException("Invalid id")
    class_type = class_type.strip()
    if class_type == "Order":
        if _id not in self.orders:
            raise InvalidIdException("Order does not exist")
        order = self.orders[_id]
        product = self.products[order.product_id]
        product.quantity += order.quantity
        del self.orders[_id]
        return order.quantity
    elif class_type == "Product":
        if _id not in self.products:
            raise InvalidIdException("Product does not exist")
        for order in self.orders.values():
            if order.product_id == _id:
                raise InvalidIdException("Product has dependent orders")
        del self.products[_id]
    elif class_type == "Customer":
        if _id not in self.customers:
            raise InvalidIdException("Customer does not exist")
        for order in self.orders.values():
            if order.customer_id == _id:
                raise InvalidIdException("Customer has dependent orders")
        del self.customers[_id]
    elif class_type == "Supplier":
        if _id not in self.suppliers:
            raise InvalidIdException("Supplier does not exist")
        for product in self.products.values():
            if product.supplier_id == _id:
                raise InvalidIdException("Supplier has dependent products")
        del self.suppliers[_id]
    else:
        raise InvalidIdException("Invalid class type")
        """
        Remove an object from the system by ID and type.

        Args:
            _id (int): Object ID to remove.
            class_type (str): One of: "Customer", "Supplier", "Product", "Order"
                              (exact casing/spelling per assignment).

        Returns:
            int | None:
                - If removing an Order: return the ordered quantity of that order (to restore stock).
                - Otherwise: no return value required.

        Raises:
            InvalidIdException:
                - If _id is not a valid non-negative integer.
                - If attempting to remove a Customer/Supplier/Product that still has dependent orders
                  in the system (i.e., orders that were not removed).
                - Additional InvalidIdException conditions as required by specification.
        """
        # TODO implement this method as instructed
        pass


def search_products(self, query, max_price=None):
    result = []
    for product in self.products.values():
        if product.quantity != 0 and query.lower() in product.name.lower():
            if max_price is None or product.price <= max_price:
                result.append(product)
    return sorted(result, key=lambda p: p.price)
    """
    Search products by query in the product name, and optionally filter by max_price.

    Args:
        query (str): Product name or part of product name.
        max_price (float, optional): If provided, only return products with price <= max_price.

    Returns:
        list[Product]:
            - Products that match the query and have quantity != 0,
            - Sorted by ascending price.
            - If no matching products exist, return an empty list.
    """
    # TODO implement this method as instructed
    pass


def export_system_to_file(self, path):
    with open(path, "w") as f:
        for customer in self.customers.values():
            print(customer, file=f)
        for supplier in self.suppliers.values():
            print(supplier, file=f)
        for product in self.products.values():
            print(product, file=f)
        """
        Export system state (customers, suppliers, products) to a text file.

        Args:
            path (str): Output file path.

        Behavior:
            - Write each object on its own line, using the object's print/str representation.
            - Orders must NOT be included.
            - No constraint on the ordering of objects in the output.

        Raises:
            OSError (or any file-open exception): Must be propagated to the caller.
        """
        # TODO implement this method as instructed
        pass


def export_orders(self, out_file):
    data = {}
    for order in self.orders.values():
        product = self.products[order.product_id]
        supplier = self.suppliers[product.supplier_id]
        city = supplier.city
        if city not in data:
            data[city] = []
        data[city].append(str(order))
    json.dump(data, out_file)
    """
    Export orders in JSON format grouped by origin city.

    Args:
        out_file (file-like)

    Behavior (per specification):
        - Produce a JSON object where:
            - Keys: origin city (supplier city) for each order.
            - Values: list of strings representing orders (format as specified in section 4.1.4).
        - Order lists can be in any order.
        - No requirement on key ordering.

    Raises:
        Any exception during writing: Must be propagated to the caller.

    Notes:
        - The order origin city is the supplier city of the ordered product.
    """
    # TODO implement this method as instructed
    pass


def load_system_from_file(path):
    system = MatamazonSystem()
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = eval(line)
                if isinstance(obj, Customer):
                    system.customers[obj.id] = obj
                elif isinstance(obj, Supplier):
                    system.suppliers[obj.id] = obj
                elif isinstance(obj, Product):
                    system.products[obj.id] = obj
            except SyntaxError:
                continue
    return system
    """
    Load a MatamazonSystem from an input file.

    Args:
        path (str): Path to a text file containing customers, suppliers and products.

    Returns:
        MatamazonSystem: Initialized system with the data found in the file.

    Behavior:
        - The file lines contain objects in the format produced by export_system_to_file (section 4.2).
        - Lines may appear in any order (e.g., product lines can appear before supplier lines).
        - Illegal lines may be ignored.
        - If an exception occurs during the creation of any required object due to invalid data,
          the function should stop and propagate the exception (as specified).

    Notes:
        - The assignment hints that eval() may be used.
    """
    # TODO implement this function as instructed
    pass

# TODO all the main part here
