from unittest import TestCase
from app import app

from models import db, User, Post


app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserTestCase(TestCase):
    def setUp(self):
        """Clean up any exisiting Users"""

        User.query.delete()
        Post.query.delete()

        user = User(first_name="First", last_name="Last")

        db.session.add(user)
        db.session.commit()

        post = Post(title="mine", content="iiiihayyeeeee", user_table=f"{user.id}")

        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id
    def tearDown(self):
        """Clean up any fouled transactions"""

        db.session.rollback()


    def test_redirect_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Users', html)

    def test_add_users(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>First Last</h1>", html)
    
    def test_edit_users(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Edit First</h1>", html)

    def test_new_user_page(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Create a user</h1>", html)

    def test_post(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/posts/new", data={'title': 'hey', 
            'content': 'here i am!', 'user_table': {self.user_id}})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f'http://localhost/users/{self.user_id}')

    def test_post_follows(self):
        with app.test_client() as client:
            resp = client.get(f'http://localhost/users/{self.user_id}', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>First Last</h1>', html)
    
    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>First Post!</h1>', html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f'/posts/{self.post_id}/delete')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f'http://localhost/users/{self.user_id}')

    def test_delete_post_follows(self):
        with app.test_client() as client:
            resp = client.get(f"http://localhost/users/{self.user_id}", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>First Last</h1>', html)