from sqlmodel import Session, select, delete
from ..database import get_session_for_faker
from ..models.models import Category, Restaurant, Offer, Order, Follow, Favorite
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()


def clear_database(session: Session):
    # Delete in order from child to parent
    session.exec(delete(Follow))
    session.exec(delete(Favorite))
    session.exec(delete(Order))
    session.exec(delete(Offer))
    session.exec(delete(Restaurant))
    session.exec(delete(Category))
    session.commit()
    print("🧹 Database cleared.")


def generate_fake_categories(session: Session, n: int = 5):
    categories = []
    for _ in range(n):
        category = Category(name=fake.word().capitalize())
        session.add(category)
        categories.append(category)
    session.commit()
    print(f"✅ Created {n} categories.")
    return categories


def generate_fake_restaurants(session: Session, categories: list, n: int = 10):
    restaurants = []
    for _ in range(n):
        restaurant = Restaurant(
            name=fake.company(),
            description=fake.catch_phrase(),
            image=fake.image_url(),
            category_id=random.choice(categories).id
        )
        session.add(restaurant)
        restaurants.append(restaurant)
    session.commit()
    print(f"✅ Created {n} restaurants.")
    return restaurants


def generate_fake_offers(session: Session, restaurants: list, min_per_restaurant=1, max_per_restaurant=3):
    offers = []
    for r in restaurants:
        for _ in range(random.randint(min_per_restaurant, max_per_restaurant)):
            original_price = round(random.uniform(10, 50), 2)
            offer = Offer(
                title=fake.bs().capitalize(),
                description=fake.text(max_nb_chars=80),
                original_price=original_price,
                offer_price=round(
                    original_price * random.uniform(0.5, 0.9), 2),
                quantity=random.randint(5, 20),
                start_datetime=datetime.now(),
                end_datetime=datetime.now() + timedelta(days=random.randint(1, 10)),
                restaurant_id=r.id
            )
            session.add(offer)
            offers.append(offer)
    session.commit()
    print(f"✅ Created {len(offers)} offers.")
    return offers


def generate_fake_users():
    return [str(i) for i in range(1, 6)]  # Simulated user IDs as strings


def generate_fake_follows(session: Session, users: list, restaurants: list):
    for user in users:
        followed = random.sample(restaurants, random.randint(1, 3))
        for r in followed:
            session.add(Follow(user_id=user, restaurant_id=r.id))
    session.commit()
    print(f"✅ Created follows for users.")


def generate_fake_favorites(session: Session, users: list, restaurants: list):
    for user in users:
        favorited = random.sample(restaurants, random.randint(1, 3))
        for r in favorited:
            session.add(Favorite(user_id=user, restaurant_id=r.id))
    session.commit()
    print(f"✅ Created favorites for users.")


def generate_fake_orders(session: Session, offers: list, n: int = 20):
    for _ in range(n):
        offer = random.choice(offers)
        quantity = random.randint(1, min(3, offer.quantity))
        order = Order(
            buyer_id=fake.name(),
            phone=fake.phone_number(),
            address=fake.address(),
            quantity=quantity,
            offer_id=offer.id
        )
        offer.quantity -= quantity
        session.add(offer)
        session.add(order)
    session.commit()
    print(f"✅ Created {n} orders.")


def run_seed_script():
    with get_session_for_faker() as session:
        clear_database(session)
        categories = generate_fake_categories(session)
        restaurants = generate_fake_restaurants(session, categories)
        offers = generate_fake_offers(session, restaurants)
        users = generate_fake_users()
        generate_fake_follows(session, users, restaurants)
        generate_fake_favorites(session, users, restaurants)
        generate_fake_orders(session, offers)
        print("🌱 Fake data generation completed!")


run_seed_script()
