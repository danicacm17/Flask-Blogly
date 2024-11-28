from app import app
from models import db, User, Post, Tag, PostTag

# Ensure we are in the application context
with app.app_context():
    # Drop all tables and recreate them
    db.drop_all()
    db.create_all()

    # Add users with image URLs
    user1 = User(first_name="Luke", last_name="Skywalker")
    user2 = User(first_name="Leia", last_name="Organa")
    user3 = User(first_name="Han", last_name="Solo")
    user4 = User(first_name="Darth", last_name="Vader")

    db.session.add_all([user1, user2, user3, user4])
    db.session.commit()

    # Add posts for each user with 75+ characters
    post1 = Post(title="A New Hope", content="The rebellion fights against the Empire. In this battle for freedom, hope rises as the heroes begin to stand up against the oppression of the Sith.", user_id=user1.id)
    post2 = Post(title="Empire Strikes Back", content="A battle on Hoth changes everything. In the wake of their loss, the rebels must regroup while the Empire's dark hand closes in on the galaxy.", user_id=user1.id)
    post3 = Post(title="Return of the Jedi", content="Victory for the rebellion. After facing the greatest trials, the forces of light ultimately overcome the Empire, securing the future of the galaxy.", user_id=user1.id)

    post4 = Post(title="Rebellion's Leader", content="A princess fights for freedom and justice. Leia stands at the forefront of the Rebellion, pushing for victory in a war that could change the galaxy forever.", user_id=user2.id)
    post5 = Post(title="A Family Secret", content="Discovering the truth about my lineage. Leia learns the shocking revelation of her true family and the terrible connection to the Empire's dark legacy.", user_id=user2.id)
    post6 = Post(title="A Diplomat's Mission", content="Balancing politics and war is not easy. Leia faces the delicate task of negotiating with allies while navigating a war that puts everything she holds dear at risk.", user_id=user2.id)

    post7 = Post(title="Smuggler's Life", content="Flying the Millennium Falcon across the galaxy. Han Solo's wild adventures take him across the stars, always a step ahead of danger and enemies.", user_id=user3.id)
    post8 = Post(title="Rescue Mission", content="Saving a princess from the Death Star. Han and his allies face impossible odds to rescue Leia from the clutches of the Empire, risking it all for a cause they believe in.", user_id=user3.id)
    post9 = Post(title="A Friend in Need", content="Helping Luke destroy the Empire. Han Solo may be a smuggler, but when it comes to fighting the Empire, he's ready to stand by his friends and lead the charge.", user_id=user3.id)

    post10 = Post(title="The Dark Side", content="The power of the Sith cannot be underestimated. Darth Vader reflects on the dangerous allure of the dark side, while battling his own inner turmoil.", user_id=user4.id)
    post11 = Post(title="A Father's Struggle", content="Facing the conflict within myself. Darth Vader struggles with his past as Anakin Skywalker and the powerful temptations of the dark side.", user_id=user4.id)
    post12 = Post(title="Redemption", content="Even in darkness, there is light. Anakin's eventual redemption shows that even the most twisted soul can find the path back to light.", user_id=user4.id)

    db.session.add_all([post1, post2, post3, post4, post5, post6, post7, post8, post9, post10, post11, post12])
    db.session.commit()

    # Add tags
    tag1 = Tag(name="Rebellion")
    tag2 = Tag(name="Empire")
    tag3 = Tag(name="Jedi")
    tag4 = Tag(name="Smuggler")
    tag5 = Tag(name="Sith")

    db.session.add_all([tag1, tag2, tag3, tag4, tag5])
    db.session.commit()

    # Assign tags to posts
    post_tags = [
        PostTag(post_id=post1.id, tag_id=tag1.id),
        PostTag(post_id=post2.id, tag_id=tag2.id),
        PostTag(post_id=post3.id, tag_id=tag3.id),
        PostTag(post_id=post4.id, tag_id=tag1.id),
        PostTag(post_id=post5.id, tag_id=tag3.id),
        PostTag(post_id=post6.id, tag_id=tag1.id),
        PostTag(post_id=post7.id, tag_id=tag4.id),
        PostTag(post_id=post8.id, tag_id=tag1.id),
        PostTag(post_id=post9.id, tag_id=tag3.id),
        PostTag(post_id=post10.id, tag_id=tag2.id),
        PostTag(post_id=post11.id, tag_id=tag5.id),
        PostTag(post_id=post12.id, tag_id=tag3.id)
    ]

    db.session.add_all(post_tags)
    db.session.commit()

    print("Database seeded successfully!")
