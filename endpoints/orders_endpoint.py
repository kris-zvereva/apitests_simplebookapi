import requests


class OrdersEndpoint:
    def __init__(self, base_url):
        self.base_url = base_url


    def create_order(self, book_id, customer_name, headers=None):
        """create a new order"""
        url = f"{self.base_url}/orders"
        payload = {
            'bookId': book_id,
            'customerName': customer_name,
        }
        return requests.post(url, headers=headers, json=payload)


    def get_list_of_orders(self,headers):
        url = f"{self.base_url}/orders"
        return requests.get(url, headers=headers)


    def get_order_by_id(self, order_id, headers):
        url = f"{self.base_url}/orders/{order_id}"
        return requests.get(url, headers=headers)


    def update_order(self, order_id, customer_name, headers):
        url = f"{self.base_url}/orders/{order_id}"
        payload = {
            'customerName': customer_name,
        }
        return requests.patch(url, headers=headers, json=payload)


    def delete_order(self, order_id, headers):
        url = f"{self.base_url}/orders/{order_id}"
        return requests.delete(url, headers=headers)
