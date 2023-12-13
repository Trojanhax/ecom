import json
from .models import Product
from django.core.exceptions import ObjectDoesNotExist


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except json.JSONDecodeError:
        cart = {}

    items = []
    order = {"get_cart_total": 0, "get_cart_item": 0, 'shipping': False}
    cartItems = order['get_cart_item']

    for product_id, cart_item in cart.items():
        try:
            quantity = cart_item["quantity"]

            product = Product.objects.get(id=product_id)
            total = product.price * quantity

            order['get_cart_total'] += total
            order['get_cart_item'] += quantity

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': quantity,
                'get_total': total
            }
            items.append(item)

            if not product.digital:
                order['shipping'] = True

        except Product.DoesNotExist:
            # Handle the case where the product with the given ID is not found
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
    print("login now..")

    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookie_data = cookieCart(request)
    items = cookie_data['items']

    customer, created = Customer.objects.get_or_create(email=email)

    if created:
        customer.name = name
        customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    product_ids = [item['product']['id'] for item in items]

    try:
        products = Product.objects.filter(id__in=product_ids)

        for item, product in zip(items, products):
            order_item = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity']
            )

    except ObjectDoesNotExist as e:
        # Handle the case where a product is not found
        print(f"Error: {e}")

    return customer, order
