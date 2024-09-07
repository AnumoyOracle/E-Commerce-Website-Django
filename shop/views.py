from django.shortcuts import render, HttpResponse
import razorpay.client
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json
import razorpay

# Create your views here.


def index(request):
    allProducts = list(
        Product.objects.all().values("product_id", "product_name", "price")
    )
    allProds = []
    catProds = Product.objects.values("category", "product_id")
    category = {item["category"] for item in catProds}
    for cat in category:
        products = Product.objects.filter(category=cat)
        for product in products:
            truncated_desc = (
                "\n".join(product.product_desc.splitlines()[:1]) + "..."
                if len(product.product_desc.splitlines()) > 1
                else product.product_desc
            )
            product.product_desc = truncated_desc
        n = len(products)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([products, range(1, nSlides), nSlides])
    params = {"allProds": allProds, "products": allProducts}
    return render(request, "shop/index.html", params)


def about(request):
    allProducts = list(
        Product.objects.all().values("product_id", "product_name", "price")
    )
    params = {"products": allProducts}
    return render(request, "shop/about.html", params)


def contact(request):
    allProducts = list(
        Product.objects.all().values("product_id", "product_name", "price")
    )
    params = {"products": allProducts}
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        desc = request.POST.get("desc", "")
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        return render(request, "shop/contact.html", params)
    return render(request, "shop/contact.html", params)


def tracker(request):
    allProducts = list(
        Product.objects.all().values("product_id", "product_name", "price")
    )
    params = {"products": allProducts}
    if request.method == "POST":
        orderId = request.POST.get("orderId", "")
        email = request.POST.get("email", "")
        try:
            order = Order.objects.filter(order_id=orderId, email=email).first()
            if order is not None:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({"text": item.update_desc, "time": item.timestamp})
                response = json.dumps([updates, order.items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse("{}")
        except Exception as e:
            return HttpResponse("{}")
    return render(request, "shop/tracker.html", params)


def searchMatch(query, item):
    if (
        query in item.product_name.lower()
        or query in item.category.lower()
        or query in item.product_desc.lower()
    ):
        return True
    else:
        return False


def search(request):
    query = request.GET.get("search")
    allProducts = list(
        Product.objects.all().values("product_id", "product_name", "price")
    )
    allProds = []
    catprods = Product.objects.values("category", "product_id")
    cats = {item["category"] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {"allProds": allProds, "products": allProducts}
    return render(request, "shop/search.html", params)


def productView(request, id):
    allProducts = list(
        Product.objects.all().values("product_id", "product_name", "price")
    )
    product = Product.objects.filter(product_id=id).first()
    return render(
        request, "shop/productView.html", {"product": product, "products": allProducts}
    )


def checkout(request):
    allProducts = list(
        Product.objects.all().values("product_id", "product_name", "price")
    )
    params = {"products": allProducts}

    if request.method == "POST":
        items_json = request.POST.get("itemsJson", "")
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        zip_code = request.POST.get("zip_code", "")
        address = request.POST.get("address", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        amount = int(request.POST.get("amount", ""))

        client = razorpay.Client(
            auth=("rzp_test_U9h78QlmdsdsasasJGYju2", "PAO5KY2kPYeasgsaSADARZsIeolqw1evU")
        )
        payment = client.order.create(
            {"amount": amount, "currency": "INR", "payment_capture": "1"}
        )

        new_order = Order(
            items_json=items_json,
            name=name,
            email=email,
            phone=phone,
            zip_code=zip_code,
            state=state,
            city=city,
            address=address,
            amount=amount,
            rzp_order_id=payment["id"],
            payment_status=False,
        )
        new_order.save()

        update_order = OrderUpdate(
            order_id=new_order.order_id, update_desc="The order has been placed"
        )
        update_order.save()

        thank = "true"
        order_id = new_order.order_id
        params["order_id"] = order_id
        params["thank"] = thank

        response_data = {
            "order_id": new_order.order_id,
            "checkout_done": True,
            "payment": payment,
        }

        response = json.dumps(response_data, default=str)
        return HttpResponse(response)
    return render(request, "shop/checkout.html", params)


def updatePaymentStatus(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        payment_id = request.POST.get("payment_id")

        try:
            order = Order.objects.filter(order_id=order_id).first()
            order.rzp_payment_id = payment_id
            order.payment_status = True
            order.save()

            return HttpResponse(json.dumps({"status": "success"}, default=str))
        except Exception as e:
            return HttpResponse(
                json.dumps(
                    {"status": "error", "message": "Order not found"}, default=str
                )
            )

    return HttpResponse(
        json.dumps({"status": "error", "message": "Invalid request"}, default=str)
    )
