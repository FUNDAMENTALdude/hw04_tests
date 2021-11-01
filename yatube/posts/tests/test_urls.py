from django.test import TestCase, Client
from ..models import Post, User, Group


class PostURLResponseTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(title='test title',
                                         description='test desctiption',
                                         slug='test-slug')
        cls.post = Post.objects.create(author=cls.user,
                                       text='text',)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(PostURLResponseTests.user)

    def test_homepage_url_exists_at_desired_location(self):
        response = self.guest_client.get('/')
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, 200)

    def test_about_tech_url_exists_at_desired_location(self):
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, 200)

    def test_about_author_url_exists_at_desired_location(self):
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, 200)

    def test_group_posts_url_exists_at_desired_location(self):
        slug = PostURLResponseTests.group.slug
        response = self.guest_client.get(f'/group/{slug}/')
        self.assertEqual(response.status_code, 200)

    def test_profile_url_exists_at_desired_location(self):
        username = PostURLResponseTests.user.username
        response = self.guest_client.get(f'/profile/{username}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_url_exists_at_desired_location(self):
        pk = PostURLResponseTests.post.pk
        response = self.guest_client.get(f'/posts/{pk}/')
        self.assertEqual(response.status_code, 200)

    def test_post_create_url_exists_at_desired_location_authorized(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_post_edit_url_exists_desired_location_author(self):
        pk = PostURLResponseTests.post.pk
        response = self.authorized_client.get(f'/posts/{pk}/edit/')
        self.assertEqual(response.status_code, 200)

    def test_post_create_url_exists_at_desired_location_anonymous(self):
        response = self.guest_client.get('/create/')
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_post_edit_url_exists_at_desired_location_anonymous(self):
        pk = PostURLResponseTests.post.pk
        response = self.guest_client.get(f'/posts/{pk}/edit/')
        self.assertRedirects(response, f'/posts/{pk}/')


class PostURLTemplateTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(title='test title2',
                                         description='test desctiption2',
                                         slug='test-slug2')
        cls.user = User.objects.create_user(username='auth2')
        cls.post = Post.objects.create(text='text2',
                                       author=cls.user, group=cls.group)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTemplateTests.user)

    def test_post_urls_uses_correct_template(self):
        slug = PostURLTemplateTests.group.slug
        username = PostURLTemplateTests.user.username
        pk = PostURLTemplateTests.post.pk
        templates_urls_names = {
            '/': 'posts/index.html',
            f'/group/{slug}/': 'posts/group_list.html',
            f'/profile/{username}/': 'posts/profile.html',
            f'/posts/{pk}/': 'posts/post_detail.html',
            f'/posts/{pk}/edit/': 'posts/post_create.html',
            '/create/': 'posts/post_create.html',
        }

        for adress, template in templates_urls_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)
