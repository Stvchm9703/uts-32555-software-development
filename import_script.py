# import http.client
from httpx import AsyncClient
import asyncio
baseUrl = "127.0.0.1:8000"
# conn = http.client.HTTPSConnection("{{baseUrl}}")

json_list = [
    {

        "name": "Supreme Pizza",
        "description": "Delicious pizza with a variety of toppings.",
        "item_type": "single",
        "category": "pizza,chicken,meat",
        "kal": 1000.2,
        "price_value": 1.23,
        "rate": 0.015,
        "options": [
            {

                "name": "Pizza sauce",
                "description": "Choose your favorite pizza sauce.",
                "extra_charge": 1.2,
                "option_kind": "favour",
                "max_count": None,
                "min_count": None,
                "kal": 120.0,
                "option_sets": [
                    "Tomato sauce",
                    "BBQ sauce"
                ]
            },
            {

                "name": "Pizza size",
                "description": "Select the size of your pizza.",
                "extra_charge": 1.2,
                "option_kind": "size",
                "max_count": 2,
                "min_count": -1,
                "kal": 120.0,
                "option_sets": [
                    "small (8 Inch)",
                    "Large (11 Inch)",
                    "Extra Large (12 Inch)"
                ]
            },
            {

                "name": "Meat amount",
                "description": "Meat on top of pizza, it can be extra with numbers of 500 grams.",
                "extra_charge": 1.25,
                "option_kind": "number_count",
                "max_count": 5,
                "min_count": 0,
                "kal": 130.0,
                "option_sets": None
            }
        ]
    },
    {

        "name": "Sausage sizzle Pizza",
        "description": "Delicious pizza topped with sausage.",
        "item_type": "single",
        "category": "pizza,sausage",
        "kal": 1000.2,
        "price_value": 1.23,
        "rate": 0.015,
        "options": [
            {

                "name": "Pizza sauce",
                "description": "Choose your favorite pizza sauce.",
                "extra_charge": 1.2,
                "option_kind": "favour",
                "max_count": None,
                "min_count": None,
                "kal": 120.0,
                "option_sets": [
                    "Tomato sauce",
                    "BBQ sauce"
                ]
            },
            {

                "name": "Pizza size",
                "description": "Select the size of your pizza.",
                "extra_charge": 1.2,
                "option_kind": "size",
                "max_count": 2,
                "min_count": -1,
                "kal": 120.0,
                "option_sets": [
                    "small (8 Inch)",
                    "Large (11 Inch)",
                    "Extra Large (12 Inch)"
                ]
            },
            {

                "name": "Sausage amount",
                "description": "Sausage on top of pizza, it can be extra with numbers of 500 grams.",
                "extra_charge": 1.25,
                "option_kind": "number_count",
                "max_count": 5,
                "min_count": 0,
                "kal": 130.0,
                "option_sets": None
            }
        ]
    },
    {

        "name": "Hawaiian sizzle Pizza",
        "description": "A delicious pizza with a perfect blend of savory ham and sweet pineapple. The Hawaiian sizzle pizza is a tropical delight that will transport your taste buds to paradise. The crispy crust, tangy tomato sauce, and melted cheese perfectly complement the juicy ham and juicy pineapple toppings. Customize your Hawaiian sizzle pizza by adding extra ham or pineapple for an even more indulgent experience.",
        "item_type": "single",
        "category": "pizza,ham",
        "kal": 1000.2,
        "price_value": 1.23,
        "rate": 0.015,
        "options": [
            {

                "name": "pizza saurce",
                "description": "Choose your preferred sauce to enhance the flavors of your Hawaiian sizzle pizza.",
                "extra_charge": 1.2,
                "option_kind": "favour",
                "max_count": None,
                "min_count": None,
                "kal": 120.0,
                "option_sets": [
                    "Tomato sauce",
                    "BBQ sauce"
                ]
            },
            {

                "name": "Pizza size",
                "description": "Select the size of your Hawaiian sizzle pizza to satisfy your appetite.",
                "extra_charge": 1.2,
                "option_kind": "size",
                "max_count": 2,
                "min_count": -1,
                "kal": 120.0,
                "option_sets": [
                    "small (8 Inch)",
                    "Large (11 Inch)",
                    "Extra Large (12 Inch)"
                ]
            },
            {

                "name": "Ham amount",
                "description": "Add extra slices of ham to your Hawaiian sizzle pizza for a meatier experience.",
                "extra_charge": 1.25,
                "option_kind": "number_count",
                "max_count": 5,
                "min_count": 0,
                "kal": 130.0,
            },
            {

                "name": "Pineapple amount",
                "description": "Boost the tropical flavor by adding more juicy pineapple to your Hawaiian sizzle pizza.",
                "extra_charge": 1.25,
                "option_kind": "number_count",
                "max_count": 5,
                "min_count": 0,
                "kal": 130.0,
            }
        ]
    },
    {

        "name": "Chicken Pizza",
        "description": "Indulge in the flavors of a mouthwatering chicken pizza. This pizza features tender and succulent chicken pieces as the star ingredient. The combination of savory chicken, melted cheese, and tangy tomato sauce creates a delightful harmony of flavors. The crust is baked to perfection, offering a crispy bite with each slice. Customize your chicken pizza by adding your favorite toppings such as onions, bell peppers, mushrooms, or olives.",
        "item_type": "single",
        "category": "pizza,chicken",
        "kal": 1000.2,
        "price_value": 1.23,
        "rate": 0.015,
        "options": [
            {

                "name": "Pizza saurce",
                "description": "Choose your preferred sauce to complement the flavors of your chicken pizza.",
                "extra_charge": 1.2,
                "option_kind": "favour",
                "kal": 120.0,
                "option_sets": [
                    "Tomato sauce",
                    "BBQ sauce"
                ]
            },
            {

                "name": "Pizza size",
                "description": "Select the size of your chicken pizza to satisfy your appetite.",
                "extra_charge": 1.2,
                "option_kind": "size",
                "max_count": 2,
                "min_count": -1,
                "kal": 120.0,
                "option_sets": [
                    "small (8 Inch)",
                    "Large (11 Inch)",
                    "Extra Large (12 Inch)"
                ]
            },
            {

                "name": "Chicken amount",
                "description": "Chicken on top of pizza, it can be extra with numbers of 500 grams.",
                "extra_charge": 1.25,
                "option_kind": "number_count",
                "max_count": 5,
                "min_count": 0,
                "kal": 130.0,
            },
            {

                "name": "Chicken favor",
                "description": "Chicken on top of pizza, it can be extra with numbers of 500 grams.",
                "extra_charge": 1.25,
                "option_kind": "favour",
                "max_count": 5,
                "min_count": 0,
                "kal": 130.0,
                "option_sets": [
                    "Sweet chilli chicken",
                    "Peri-peri chicken"
                ]
            },
            {
                "name": "Toppings",
                "description": "Enhance the flavors of your chicken pizza with your choice of additional toppings.",
                "extra_charge": 0.75,
                "option_kind": "favour",
                "max_count": 5,
                "min_count": 0,
                "kal": 80,
                "option_sets": [
                    "Onions",
                    "Bell Peppers",
                    "Mushrooms",
                    "Olives",
                    "Tomatoes"
                ]
            }
        ]
    },
    {

        "name": "Veggie lovers' Pizza",
        "description": "Experience a burst of fresh and vibrant flavors with our Veggie Lovers' Pizza. This delightful pizza is a vegetarian's dream, loaded with a colorful array of nutritious vegetables. Each bite offers a medley of flavors, from the earthiness of mushrooms to the sweetness of bell peppers and the tanginess of tomatoes. The crust is perfectly baked to a golden brown, providing a satisfying crunch.",
        "item_type": "single",
        "category": "pizza,veggie",
        "kal": 1000.2,
        "price_value": 1.23,
        "rate": 0.015,
        "options": [
            {

                "name": "Pizza saurce",
                "description": "Choose your preferred sauce to complement the flavors of your Veggie Lovers' Pizza.",
                "extra_charge": 1.2,
                "option_kind": "favour",
                "kal": 120.0,
                "option_sets": [
                    "Tomato sauce",
                    "BBQ sauce"
                ]
            },
            {

                "name": "Pizza size",
                "description": "Select the size of your Veggie Lovers' Pizza to suit your appetite.",
                "extra_charge": 1.2,
                "option_kind": "size",
                "max_count": 2,
                "min_count": -1,
                "kal": 120.0,
                "option_sets": [
                    "small (8 Inch)",
                    "Large (11 Inch)",
                    "Extra Large (12 Inch)"
                ]
            },
            {
                "name": "Toppings",
                "description": "Customize your Veggie Lovers' Pizza with a selection of delicious toppings.",
                "extra_charge": 0.75,
                "option_kind": "favour",
                "kal": 80,
                "option_sets": [
                    "Onions",
                    "Bell Peppers",
                    "Mushrooms",
                    "Olives",
                    "Extra Cheese"
                ]
            }
        ]
    },
    {

        "name": "Garlic bread",
        "description": "Indulge in our freshly baked garlic bread, infused with aromatic garlic butter and sprinkled with a blend of herbs and spices. Each bite delivers a perfect combination of softness and crispiness, leaving you craving for more. Whether you enjoy it as an appetizer or a side dish, our garlic bread is a delightful addition to any meal.",
        "item_type": "side",
        "category": "side,bread",
        "kal": 240.8,
        "price_value": 2.99,
        "rate": 0.014,
        
    },
    {

        "name": "Breadsticks",
        "description": "Savor the warm and comforting goodness of our freshly baked breadsticks. These golden sticks of dough are brushed with garlic butter and sprinkled with a blend of herbs, giving them a fragrant aroma and irresistible flavor. Dip them in marinara sauce or creamy garlic dip for an extra burst of deliciousness. Our breadsticks are perfect as an appetizer or a side to complement your main course.",
        "item_type": "side",
        "category": "side,bread,appetizer",
        "kal": 180.5,
        "price_value": 2.49,
        "rate": 0.012,
        
    },
    {

        "name": "Salad",
        "description": "Experience a refreshing burst of flavors with our crisp and vibrant salad. Made with a variety of fresh vegetables, such as lettuce, tomatoes, cucumbers, and carrots, our salad is a healthy and delicious choice. It is accompanied by your choice of dressing, ranging from tangy vinaigrette to creamy ranch. Whether as a starter or a light meal, our salad is a perfect way to incorporate a dose of greens into your dining experience.",
        "item_type": "side",
        "category": "side,appetizer",
        "kal": 120.3,
        "price_value": 4.99,
        "rate": 0.015,
        
    },
    {

        "name": "French fries",
        "description": "Indulge in the crispy and golden perfection of our French fries. Made from fresh potatoes, cut into thin strips and cooked to a delightful crispiness, these fries are a classic favorite. Seasoned with just the right amount of salt, they are perfect on their own or as a side dish. Whether you're enjoying them with a burger or as a snack, our French fries are guaranteed to satisfy your cravings.",
        "item_type": "side",
        "category": "side, fries,appetizer",
        "kal": 350.2,
        "price_value": 3.49,
        "rate": 0.011,
        
    },
    {

        "name": "Onion rings",
        "description": "Delight in the crispy and flavorful experience of our onion rings. Sliced onions are coated in a light and crispy batter, then fried to a golden brown perfection. Each bite offers a delightful combination of sweet onion and a satisfying crunch. Served with a tangy dipping sauce, our onion rings make for a fantastic appetizer or side dish that will leave you wanting more.",
        "item_type": "side",
        "category": "side, fries,appetizer",
        "kal": 280.9,
        "price_value": 3.99,
        "rate": 0.013,
        
    },
    {

        "name": "Mozzarella sticks",
        "description": "Indulge in the gooey and cheesy goodness of our mozzarella sticks. Made with premium mozzarella cheese coated in a crispy breading, these sticks are deep-fried to a golden brown perfection. Each bite reveals a stretchy and melty cheese center that is simply irresistible. Served with a zesty marinara sauce for dipping, our mozzarella sticks are a crowd-pleasing appetizer that will satisfy your cheese cravings.",
        "item_type": "side",
        "category": "side,fries",
        "kal": 320.6,
        "price_value": 5.99,
        "rate": 0.016,
        
    },
    {

        "name": "Chicken wings",
        "description": "Sink your teeth into our mouthwatering chicken wings. Whether you like them spicy, tangy, or savory, we have a variety of flavors to suit your taste. Our chicken wings are seasoned and cooked to perfection, with tender and juicy meat on the inside and crispy skin on the outside. Served with your choice of dipping sauces, our chicken wings are an absolute favorite for game nights, parties, or simply as a delicious appetizer or snack.",
        "item_type": "side",
        "category": "side,chicken,appetizer",
        "kal": 410.2,
        "price_value": 7.99,
        "rate": 0.02,
        
    },
    {

        "name": "Grilled vegetables",
        "description": "Experience the natural flavors of our grilled vegetables. We carefully select a medley of fresh vegetables, such as bell peppers, zucchini, eggplant, and mushrooms, and grill them to perfection. The grilling process enhances their natural sweetness and adds a smoky charred flavor. Served as a side dish or as part of a hearty platter, our grilled vegetables are a healthy and delicious way to enjoy the goodness of nature's bounty.",
        "item_type": "side",
        "category": "side,fries",
        "kal": 150.9,
        "price_value": 4.99,
        "rate": 0.015,
        
    },
    {

        "name": "Potato wedges",
        "description": "Indulge in the satisfying crispiness of our potato wedges. Made from thick-cut potatoes, seasoned with a blend of spices, and baked to a golden brown, these wedges are a delicious alternative to traditional fries. Their soft and fluffy interior paired with their crispy exterior makes them a delightful side dish or a snack option. Whether you dip them in ketchup or your favorite sauce, our potato wedges are a tasty treat for any occasion.",
        "item_type": "side",
        "category": "side,fries",
        "kal": 280.1,
        "price_value": 3.99,
        "rate": 0.013,
        
    },
    {

        "name": "Creamy mushroom pasta",
        "description": "Indulge in a creamy and flavorful pasta dish with our creamy mushroom pasta. Tender pasta is tossed in a rich and velvety sauce, infused with the earthy and savory flavors of mushrooms. Each bite is a delightful combination of silky pasta, tender mushrooms, and a luscious cream sauce that coats every strand. Served with a sprinkle of grated Parmesan cheese, our creamy mushroom pasta is a comforting and satisfying choice for pasta lovers.",
        "item_type": "side",
        "category": "side,pasta",
        "kal": 540.7,
        "price_value": 11.99,
        "rate": 0.018,
        
    },
    {

        "name": "Classic Bolognese pasta",
        "description": "Delight in the timeless classic of our Bolognese pasta. Our pasta is cooked to al dente perfection and tossed in a rich and hearty Bolognese sauce. Made with a flavorful combination of ground beef, tomatoes, onions, garlic, and herbs, our Bolognese sauce delivers a comforting and robust taste. Finished with a sprinkle of grated Parmesan cheese, our classic Bolognese pasta is a satisfying choice for pasta enthusiasts.",
        "item_type": "side",
        "category": "side,pasta",
        "kal": 620.4,
        "price_value": 12.99,
        "rate": 0.02,
        
    },
    {
        "name": "Coke",
        "description": "Classic and refreshing soda with a hint of caramel flavor.",
        "item_type": "side",
        "category": "drink",
        "kal": 220.5,
        "price_value": 4.23,
        "rate": 0.015
    },
    {
        "name": "Sprite",
        "description": "Refreshing lemon-lime soda with a crisp and bubbly taste.",
        "item_type": "side",
        "category": "drink",
        "kal": 180.2,
        "price_value": 3.99,
        "rate": 0.01
    },
    {
        "name": "Root Beer",
        "description": "Traditional and creamy soda with a distinct root beer flavor.",
        "item_type": "side",
        "category": "drink",
        "kal": 210.5,
        "price_value": 4.49,
        "rate": 0.01
    },
    {
        "name": "Iced Tea",
        "description": "Refreshing cold tea with a choice of flavors like lemon, peach, or raspberry.",
        "item_type": "side",
        "category": "drink",
        "kal": 120.8,
        "price_value": 3.29,
        "rate": 0.01
    },
    {
        "name": "Sparkling Water",
        "description": "Effervescent and pure mineral water with a sparkling touch.",
        "item_type": "side",
        "category": "drink",
        "kal": 0,
        "price_value": 2.99,
        "rate": 0.01
    }
]


async def main():
    for sett in json_list:
        print(sett['name'])
        async with AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/api/product/create/",
                json=sett
            )
            print(response.text)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
