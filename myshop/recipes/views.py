from django.shortcuts import render, redirect
import random
from django.http import HttpResponse, Http404, JsonResponse
# Create your views here.

RECIPES = [
    {
        "id": 1,
        "slug": "khinkali",
        "name": "ხინკალი",
        "category": "main",
        "minutes": 90,
        "vegetarian": False,
        "ingredients": ["ფქვილი", "საქონლის ხორცი", "ღორის ხორცი", "ხახვი", "კვლიავი"]
    },
    {
        "id": 2,
        "slug": "khachapuri",
        "name": "ხაჭაპური",
        "category": "bakery",
        "minutes": 60,
        "vegetarian": True,
        "ingredients": ["ფქვილი", "იმერული ყველი", "კვერცხი", "კარაქი"]
    },
    {
        "id": 3,
        "slug": "lobiani",
        "name": "ლობიანი",
        "category": "bakery",
        "minutes": 75,
        "vegetarian": True,
        "ingredients": ["ფქვილი", "ლობიო", "ხახვი", "კარაქი"]
    },
    {
        "id": 4,
        "slug": "pkhali",
        "name": "ფხალი",
        "category": "snack",
        "minutes": 30,
        "vegetarian": True,
        "ingredients": ["ისპანახი", "ნიგოზი", "ნიორი", "ქინძი"]
    },
    {
        "id": 5,
        "slug": "churchkhela",
        "name": "ჩურჩხელა",
        "category": "dessert",
        "minutes": 240,
        "vegetarian": True,
        "ingredients": ["ნიგოზი", "ყურძნის წვენი", "ფქვილი"]
    },
    {
        "id": 6,
        "slug": "chakapuli",
        "name": "ჩაქაფული",
        "category": "main",
        "minutes": 120,
        "vegetarian": False,
        "ingredients": ["ცხვრის ხორცი", "ტყემალი", "ტარხუნა", "თეთრი ღვინო"]
    },
]


def page(title, body):
    return HttpResponse(
        f"<h1>{title}</h1>{body}<hr>"
        "<a href='/recipes/'>← ყველა რეცეპტი</a>"
    )

def recipe_list(request):
    recipes = RECIPES.copy()

    category = request.GET.get("category")
    max_time = request.GET.get("max_minutes")
    vegetarian = request.GET.get("vegetarian")

    if category:
        recipes = [
            i for i in recipes
            if i["category"] == category
        ]

    if max_time:
        recipes = [
            i for i in recipes
            if i["minutes"] <= int(max_time)
        ]

    if vegetarian == "yes":
        recipes = [
            i for i in recipes
            if i["vegetarian"] is True
        ]

    items = "".join(
        f"<li><a href='/recipes/{i['id']}/'>"
        f"{i['name']}</a> -- {i['minutes']} წუთი</li>"
        for i in recipes
        
    )
    if not items:
        items = "<li>რეცეპტი ვერ მოიძებნა</li>"
    return page("რეცეპტები", f"<ul>{items}</ul>")

def recipe_detail(request, recipe_id):
    recipe = next((i for i in RECIPES if i["id"] == recipe_id), None)
    if not recipe:
        raise Http404("რეცეპტი ვერ მოიძებნა")

    ingredients = "".join(f"<li>{i}</li>" for i in recipe["ingredients"])
    return page(
        recipe["name"],
        f"<p>მზადების დრო: {recipe['minutes']} წუთი</p>"
        f"<ul>{ingredients}</ul>"
    )

def search(request):
    q = request.GET.get("q", "").strip()

    if not q:
        return page("ძებნა", "<p>ჩაწერე საძიებო სიტყვა</p>")

    filtered = [
        r for r in RECIPES
        if any(q.lower() in ingredient.lower()
               for ingredient in r["ingredients"])
    ]

    items = "".join(
        f"<li><a href='/recipes/{r['id']}/'>"
        f"{r['name']}</a></li>"
        for r in filtered
    )

    if not filtered:
        items = "<p>ვერაფერი მოიძებნა</p>"

    return page("ძებნის შედეგები", f"<ul>{items}</ul>")

def recipe_by_slug(request, slug):
    for recipe in RECIPES:
        if recipe["slug"] == slug:
            ingredients = ", ".join(recipe["ingredients"])

            body = f"""
                <p>კატეგორია: {recipe['category']}</p>
                <p>მომზადების დრო: {recipe['minutes']} წუთი</p>
                <p>ინგრედიენტები: {ingredients}</p>
            """

            return page(recipe["name"], body)

    raise Http404("რეცეპტი ვერ მოიძებნა")

def random_recipe(request):
    recipe = random.choice(RECIPES)

    return redirect(
        "recipes:detail",
        recipe_id=recipe["id"]
    )

def category_detail(request, name):
    categories = [r["category"] for r in RECIPES]

    if name not in categories:
        raise Http404("კატეგორია ვერ მოიძებნა")

    filtered = [
        r for r in RECIPES
        if r["category"] == name
    ]

    items = "".join(
        f"<li><a href='/recipes/{r['id']}/'>"
        f"{r['name']}</a> — {r['minutes']} წუთი</li>"
        for r in filtered
    )

    return page(f"კატეგორია: {name}", f"<ul>{items}</ul>")

def stats(request):
    return JsonResponse({
        "total_recipes": len(RECIPES),
        "vegetarian": sum(
            1 for r in RECIPES if r["vegetarian"]
        ),
        "categories": list(set(
            r["category"] for r in RECIPES
        )),
    })