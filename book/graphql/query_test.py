# import pytest
# from unibuddy_api.blog.factory import create_blog, create_blog_topic
# from unibuddy_api.blog.models import BlogPost
# from unibuddy_api.blog.query import get_included_blog_post_ids
# from unibuddy_api.user.university_user.factory import UniversityUserFactory
#
# from unibuddy_api.degree.models import Degree
# from unibuddy_api.geography.factory import CountryFactory
# from unibuddy_api.university.factory import UniversityFactory
# from unibuddy_api.user.mentor.factory import MentorFactory
#
#
# class TestPost:
#     def test_includes_non_archived_posts(self, start_pikachu):
#         client, _, _ = start_pikachu
#
#         country = CountryFactory.create('UK')
#         university = UniversityFactory.create('Edinburgh', country)
#         university_user = UniversityUserFactory.create('Sam', university)
#         mentor = MentorFactory.create('Malcolm', university, country_code=country.code)
#         topic = create_blog_topic(university_user.id, university, 'Testing')
#         blog_post = create_blog(mentor, topic, 'A', '...', image='image.jpeg')
#         query = """
#             {{
#                 post(id: "{id}") {{
#                     id
#                 }}
#             }}
#         """.format(id=blog_post.id)
#         response = client.graphql(query)
#
#         assert response['data']['post']['id'] == str(blog_post.id)
#
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_excludes_archived_posts(self, start_pikachu):
#         client, _, _ = start_pikachu
#
#         country = CountryFactory.create('GB')
#         university = UniversityFactory.create('Edinburgh', country)
#         university_user = UniversityUserFactory.create('Sam', university)
#         mentor = MentorFactory.create('Malcolm', university, country_code=country.code)
#         topic = create_blog_topic(university_user.id, university, 'Testing')
#         blog_post = create_blog(mentor, topic, 'A', '...', image='image.jpeg')
#         blog_post.modify(set__archived=True)
#
#         query = """
#             {{
#                 post(id: "{id}") {{
#                     id
#                 }}
#             }}
#         """.format(id=blog_post.id)
#         response = client.graphql(query)
#
#         assert response['data']['post'] is None
#
#
# class TestAllPosts:
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_excludes_archived_posts(self, start_pikachu):
#         client, _, _ = start_pikachu
#
#         country = CountryFactory.create('GB')
#         university = UniversityFactory.create('Edinburgh', country)
#         university_user = UniversityUserFactory.create('Sam', university)
#         mentor = MentorFactory.create('Malcolm', university, country_code=country.code)
#         topic = create_blog_topic(university_user.id, university, 'Testing')
#         blog_post_unarchived = create_blog(mentor, topic, 'A', '...', image='image.jpeg')
#         blog_post_archived = create_blog(mentor, topic, 'B', '...', image='image.jpeg')
#         blog_post_archived.modify(set__archived=True)
#
#         query = """
#             {{
#                 allPosts(universitySlug: "{university_slug}") {{
#                     id
#                 }}
#             }}
#         """.format(university_slug=university.slug)
#         response = client.graphql(query)
#
#         posts = response['data']['allPosts']
#         assert len(posts) == 1
#         assert posts[0]['id'] == str(blog_post_unarchived.id)
#
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_get_posts_by_author_degree(self, start_pikachu):
#         client, _, _ = start_pikachu
#
#         country = CountryFactory.create('GB')
#         university = UniversityFactory.create('UCL', country)
#         university_user = UniversityUserFactory.create('Sam', university)
#         mentor_one = MentorFactory.create('Kimeshan', university, country_code=country.code, degree_name="Degree 1")
#         mentor_two = MentorFactory.create('Diego', university, country_code=country.code, degree_name="Degree 2")
#         topic = create_blog_topic(university_user.id, university, 'Testing')
#         blog_post_one = create_blog(mentor_one, topic, 'Title 1', 'Blog text 1', image='image.jpeg', approved=True)
#         create_blog(mentor_two, topic, 'Title 2', 'Blog text 2', image='image.jpeg')
#         degree = Degree.objects.get(name="Degree 1", university=university)
#         query = """
#             {{
#                 allPosts(universitySlug: "{university_slug}", degreeId: "{degree_id}") {{
#                     id
#                 }}
#             }}
#         """.format(university_slug=university.slug, degree_id=degree.id)
#         response = client.graphql(query)
#         posts = response['data']['allPosts']
#         assert len(posts) == 1
#         assert posts[0]['id'] == str(blog_post_one.id)
#
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_get_posts_by_university_slug(self, start_pikachu):
#         client, _, _ = start_pikachu
#
#         country = CountryFactory.create('GB')
#         university_one = UniversityFactory.create('UCL', country)
#         university_two = UniversityFactory.create('Imperial', country)
#         university_one_user = UniversityUserFactory.create('Amy', university_one)
#         university_two_user = UniversityUserFactory.create('Niall', university_two)
#         mentor_one = MentorFactory.create('Kimeshan', university_one, country_code=country.code, degree_name="Degree 1")
#         mentor_two = MentorFactory.create('Diego', university_two, country_code=country.code, degree_name="Degree 2")
#         topic_one = create_blog_topic(university_one_user.id, university_one, 'Topic 1')
#         topic_two = create_blog_topic(university_two_user.id, university_two, 'Topic 2')
#         blog_post_one_uni_one = create_blog(mentor_one, topic_one, 'Title 1 at Uni 1', 'Blog text',
#                                             image='image.jpeg', approved=True)
#         blog_post_two_uni_one = create_blog(mentor_one, topic_one, 'Title 2 at Uni 1', 'Blog text',
#                                             image='image.jpeg', approved=True)
#         create_blog(mentor_two, topic_two, 'Title 1 at Uni 2', 'Blog text',
#                     image='image.jpeg', approved=True)
#         query = """
#             {{
#                 allPosts(universitySlug: "{university_slug}") {{
#                     id
#                 }}
#             }}
#         """.format(university_slug=university_one.slug)
#         response = client.graphql(query)
#         posts = response['data']['allPosts']
#         assert len(posts) == 2
#         assert {'id': str(blog_post_one_uni_one.id)} in posts
#         assert {'id': str(blog_post_two_uni_one.id)} in posts
#
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_get_posts_by_university_id(self, start_pikachu):
#         client, _, _ = start_pikachu
#
#         country = CountryFactory.create('GB')
#         university_one = UniversityFactory.create('UCL', country)
#         university_two = UniversityFactory.create('Imperial', country)
#         university_one_user = UniversityUserFactory.create('Amy', university_one)
#         university_two_user = UniversityUserFactory.create('Niall', university_two)
#         mentor_one = MentorFactory.create('Kimeshan', university_one, country_code=country.code, degree_name="Degree 1")
#         mentor_two = MentorFactory.create('Diego', university_two, country_code=country.code, degree_name="Degree 2")
#         topic_one = create_blog_topic(university_one_user.id, university_one, 'Topic 1')
#         topic_two = create_blog_topic(university_two_user.id, university_two, 'Topic 2')
#         blog_post_one_uni_one = create_blog(mentor_one, topic_one, 'Title 1 at Uni 1',
#                                             'Blog text', image='image.jpeg', approved=True)
#         blog_post_two_uni_one = create_blog(mentor_one, topic_one, 'Title 2 at Uni 1',
#                                             'Blog text', image='image.jpeg', approved=True)
#         create_blog(mentor_two, topic_two, 'Title 1 at Uni 2', 'Blog text', image='image.jpeg', approved=True)
#         query = """
#             {{
#                 allPosts(universityId: "{university_id}") {{
#                     id
#                 }}
#             }}
#         """.format(university_id=university_one.id)
#         response = client.graphql(query)
#         posts = response['data']['allPosts']
#         assert len(posts) == 2
#         assert {'id': str(blog_post_one_uni_one.id)} in posts
#         assert {'id': str(blog_post_two_uni_one.id)} in posts
#
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_filter_by_author_id(self, start_pikachu):
#         client, _, _ = start_pikachu
#         country = CountryFactory.create('GB')
#         university = UniversityFactory.create('Edinburgh', country)
#         university_user = UniversityUserFactory.create('Ed', university)
#         mentor1 = MentorFactory.create('Sam', university, country_code=country.code)
#         mentor2 = MentorFactory.create('Joe', university, country_code=country.code)
#         topic = create_blog_topic(university_user.id, university, 'Sport')
#         blog1 = create_blog(mentor1, topic, 'Gym', 'hello', image='image.jpeg', approved=True)
#         create_blog(mentor2, topic, 'Pole', 'yo', image='image.jpeg', approved=True)
#
#         query = """
#             {{
#                 allPosts(universitySlug: "{university_slug}", authorId: "{mentor.id}") {{
#                     id
#                 }}
#             }}
#         """.format(university_slug=university.slug, mentor=mentor1)
#         response = client.graphql(query)
#
#         posts = response['data']['allPosts']
#         assert len(posts) == 1
#         assert posts[0]['id'] == str(blog1.id)
#
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_limit_less_than_max(self, start_pikachu):
#         client, _, _ = start_pikachu
#         country = CountryFactory.create('GB')
#         university = UniversityFactory.create('Edinburgh', country)
#         university_user = UniversityUserFactory.create('Ed', university)
#         mentor = MentorFactory.create('Sam', university, country_code=country.code)
#         topic = create_blog_topic(university_user.id, university, 'Sport')
#         create_blog(mentor, topic, 'Gym', 'hello', image='image.jpeg', approved=True)
#         create_blog(mentor, topic, 'Pole', 'yo', image='image.jpeg', approved=True)
#
#         query = """
#             {{
#                 allPosts(universitySlug: "{university_slug}", limit: 1) {{
#                     id
#                 }}
#             }}
#         """.format(university_slug=university.slug, mentor=mentor)
#         response = client.graphql(query)
#
#         posts = response['data']['allPosts']
#         assert len(posts) == 1
#
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_limit_more_than_max(self, start_pikachu):
#         client, _, _ = start_pikachu
#         country = CountryFactory.create('GB')
#         university = UniversityFactory.create('Edinburgh', country)
#         university_user = UniversityUserFactory.create('Ed', university)
#         mentor = MentorFactory.create('Sam', university, country_code=country.code)
#         topic = create_blog_topic(university_user.id, university, 'Sport')
#         create_blog(mentor, topic, 'Gym', 'hello', image='image.jpeg', approved=True)
#         create_blog(mentor, topic, 'Pole', 'yo', image='image.jpeg', approved=True)
#
#         query = """
#                 {{
#                     allPosts(universitySlug: "{university_slug}", limit: 3) {{
#                         id
#                     }}
#                 }}
#             """.format(university_slug=university.slug, mentor=mentor)
#         response = client.graphql(query)
#
#         posts = response['data']['allPosts']
#         assert len(posts) == 2
#
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_limit_and_page_num(self, start_pikachu):
#         client, _, _ = start_pikachu
#         country = CountryFactory.create('GB')
#         university = UniversityFactory.create('Edinburgh', country)
#         university_user = UniversityUserFactory.create('Ed', university)
#         mentor = MentorFactory.create('Sam', university, country_code=country.code)
#         topic = create_blog_topic(university_user.id, university, 'Sport')
#         create_blog(mentor, topic, 'Gym', 'hello', image='image.jpeg', approved=True)
#         post = create_blog(mentor, topic, 'Pole', 'yo', image='image.jpeg', approved=True)
#         create_blog(mentor, topic, 'Boxing', 'yo', image='image.jpeg', approved=True)
#
#         query = """
#             {{
#                 allPosts(universitySlug: "{university_slug}", limit: 1, offset: 1) {{
#                     id
#                 }}
#             }}
#         """.format(university_slug=university.slug, mentor=mentor)
#         response = client.graphql(query)
#
#         posts = response['data']['allPosts']
#         assert len(posts) == 1
#         assert posts[0]["id"] == str(post.id)
#
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_excludes_archived_posts(self, start_pikachu):
#         client, _, _ = start_pikachu
#
#         country = CountryFactory.create('GB')
#         university = UniversityFactory.create('Edinburgh', country)
#         university_user = UniversityUserFactory.create('Sam', university)
#         mentor = MentorFactory.create('Malcolm', university, country_code=country.code)
#         topic = create_blog_topic(university_user.id, university, 'Testing')
#         blog_post_unarchived = create_blog(mentor, topic, 'A', '...', image='image.jpeg', approved=True)
#         blog_post_archived = create_blog(mentor, topic, 'B', '...', image='image.jpeg', approved=True)
#         blog_post_archived.modify(set__archived=True)
#
#         query = """
#             {{
#                 allPosts(universitySlug: "{university_slug}") {{
#                     id
#                 }}
#             }}
#         """.format(university_slug=university.slug)
#         response = client.graphql(query)
#
#         posts = response['data']['allPosts']
#         assert len(posts) == 1
#         assert posts[0]['id'] == str(blog_post_unarchived.id)
#
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_excludes_disapproved_posts(self, start_pikachu):
#         client, _, _ = start_pikachu
#
#         country = CountryFactory.create('GB')
#         university = UniversityFactory.create('Edinburgh', country)
#         university_user = UniversityUserFactory.create('Sam', university)
#         mentor = MentorFactory.create('Malcolm', university, country_code=country.code)
#         topic = create_blog_topic(university_user.id, university, 'Testing')
#         blog_post1 = create_blog(mentor, topic, 'A', '...', image='image.jpeg', approved=True)
#         create_blog(mentor, topic, 'B', '...', image='image.jpeg', approved=False)
#
#         query = """
#                 {{
#                     allPosts(universitySlug: "{university_slug}") {{
#                         id
#                     }}
#                 }}
#             """.format(university_slug=university.slug)
#         response = client.graphql(query)
#
#         posts = response['data']['allPosts']
#         assert len(posts) == 1
#         assert posts[0]['id'] == str(blog_post1.id)
#
#
# class TestMentorPosts:
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_get_mentor_blog_posts(self, start_pikachu):
#         client, _, _ = start_pikachu
#         country = CountryFactory.create('GB')
#         university = UniversityFactory.create('Edinburgh', country)
#         university_user = UniversityUserFactory.create('Sam', university)
#         mentor_one = MentorFactory.create('Malcolm', university, country_code=country.code)
#         mentor_two = MentorFactory.create('Diego', university, country_code=country.code)
#         topic = create_blog_topic(university_user.id, university, 'Testing')
#         blog_post_one = create_blog(mentor_one, topic, 'My post 1', '...', image='image.jpeg', approved=True)
#         blog_post_two = create_blog(mentor_one, topic, 'My post 2', '...', image='image.jpeg', approved=True)
#         create_blog(mentor_two, topic, 'Other post', '...', image='image.jpeg')
#         query = """
#             {{
#                 mentorPosts(mentorId: "{mentorId}") {{
#                     id
#                 }}
#             }}
#         """.format(mentorId=mentor_one.id)
#         response = client.graphql(query)
#
#         posts = response['data']['mentorPosts']
#         assert len(posts) == 2
#         assert {'id': str(blog_post_one.id)} in posts
#         assert {'id': str(blog_post_two.id)} in posts
#
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_excludes_archived_posts(self, start_pikachu):
#         client, _, _ = start_pikachu
#
#         country = CountryFactory.create('GB')
#         university = UniversityFactory.create('Edinburgh', country)
#         university_user = UniversityUserFactory.create('Sam', university)
#         mentor = MentorFactory.create('Malcolm', university, country_code=country.code)
#         topic = create_blog_topic(university_user.id, university, 'Testing')
#         blog_post_unarchived = create_blog(mentor, topic, 'A', '...', image='image.jpeg', approved=True)
#         blog_post_archived = create_blog(mentor, topic, 'B', '...', image='image.jpeg', approved=True)
#         blog_post_archived.modify(set__archived=True)
#
#         query = """
#             {{
#                 mentorPosts(mentorId: "{mentorId}") {{
#                     id
#                 }}
#             }}
#         """.format(mentorId=mentor.id)
#         response = client.graphql(query)
#
#         posts = response['data']['mentorPosts']
#         assert len(posts) == 1
#         assert posts[0]['id'] == str(blog_post_unarchived.id)
#
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_excludes_non_approved_posts(self, start_pikachu):
#         client, _, _ = start_pikachu
#
#         country = CountryFactory.create('GB')
#         university = UniversityFactory.create('Edinburgh', country)
#         university_user = UniversityUserFactory.create('Sam', university)
#         mentor = MentorFactory.create('Malcolm', university, country_code=country.code)
#         topic = create_blog_topic(university_user.id, university, 'Testing')
#         blog_post1 = create_blog(mentor, topic, 'A', '...', image='image.jpeg', approved=True)
#         create_blog(mentor, topic, 'B', '...', image='image.jpeg', approved=False)
#
#         query = """
#             {{
#                 mentorPosts(mentorId: "{mentorId}") {{
#                     id
#                 }}
#             }}
#         """.format(mentorId=mentor.id)
#         response = client.graphql(query)
#
#         posts = response['data']['mentorPosts']
#         assert len(posts) == 1
#         assert posts[0]['id'] == str(blog_post1.id)
#
#
# class TestGetIncludedBlogPostIds:
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_includes_only_approved_posts(self, start_pikachu):
#         client, _, _ = start_pikachu
#
#         country = CountryFactory.create('GB')
#         university = UniversityFactory.create('Edinburgh', country)
#         university_user = UniversityUserFactory.create('Sam', university)
#         mentor = MentorFactory.create('Malcolm', university, country_code=country.code)
#         topic = create_blog_topic(university_user.id, university, 'Testing')
#         create_blog(mentor, topic, 'A', '...', image='image.jpeg', approved=False)
#         post = create_blog(mentor, topic, 'B', '...', image='image.jpeg', approved=True)
#
#         posts = get_included_blog_post_ids(university.id, university_user.id)
#
#         assert posts == [post.id]
#
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_includes_my_unapproved_posts(self, start_pikachu):
#         client, _, _ = start_pikachu
#
#         country = CountryFactory.create('GB')
#         university = UniversityFactory.create('Edinburgh', country)
#         university_user = UniversityUserFactory.create('Sam', university)
#         mentor1 = MentorFactory.create('Malcolm', university, country_code=country.code)
#         mentor2 = MentorFactory.create('Zarko', university, country_code=country.code)
#         topic = create_blog_topic(university_user.id, university, 'Testing')
#         post1 = create_blog(mentor1, topic, 'A', '...', image='image.jpeg', approved=True)
#         post2 = create_blog(mentor2, topic, 'B', '...', image='image.jpeg', approved=False)
#
#         posts = get_included_blog_post_ids(university.id, mentor2.id)
#
#         assert posts == [post1.id, post2.id]
#
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_includes_old_posts_without_approval(self, start_pikachu):
#         client, _, _ = start_pikachu
#
#         country = CountryFactory.create('GB')
#         university = UniversityFactory.create('Edinburgh', country)
#         university_user = UniversityUserFactory.create('Sam', university)
#         mentor1 = MentorFactory.create('Malcolm', university, country_code=country.code)
#         mentor2 = MentorFactory.create('Zarko', university, country_code=country.code)
#         topic = create_blog_topic(university_user.id, university, 'Testing')
#         post1 = create_blog(mentor1, topic, 'A', '...', image='image.jpeg', approved=True)
#         post2 = create_blog(mentor2, topic, 'B', '...', image='image.jpeg', approved=False)
#         post_without_approval = BlogPost.objects.create(
#             topic=topic,
#             university=mentor1.university,
#             author=mentor1,
#             title="Old",
#             text="text",
#             image="image.jpeg",
#         )
#
#         posts = get_included_blog_post_ids(university.id, mentor2.id)
#
#         assert posts == [post1.id, post2.id, post_without_approval.id]
#
#
# class TestUniversityBlogPosts:
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_pagination(self, start_pikachu):
#         _, auth, _ = start_pikachu
#
#         country = CountryFactory.create('GB')
#         university = UniversityFactory.create('Edinburgh', country)
#         university_user = UniversityUserFactory.create('Sam', university)
#         mentor = MentorFactory.create('Malcolm', university, country_code=country.code)
#         topic = create_blog_topic(university_user.id, university, 'Testing')
#         blog1 = create_blog(mentor, topic, 'A', '...', image='image.jpeg')
#         create_blog(mentor, topic, 'B', '...', image='image.jpeg')
#
#         query = """
#             {{
#                 universityBlogPosts(pageNum: 1, itemsPerPage: 1) {{
#                     blogPosts {{
#                         id
#                     }}
#                 }}
#             }}
#         """.format(university_slug=university.slug)
#         response = auth.jwt.graphql(email=university_user.email, query=query)
#
#         posts = response['data']['universityBlogPosts']["blogPosts"]
#         assert len(posts) == 1
#         assert posts[0]['id'] == str(blog1.id)
#
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_ordering(self, start_pikachu):
#         _, auth, _ = start_pikachu
#
#         country = CountryFactory.create('GB')
#         university = UniversityFactory.create('Edinburgh', country)
#         university_user = UniversityUserFactory.create('Sam', university)
#         mentor = MentorFactory.create('Malcolm', university, country_code=country.code)
#         topic = create_blog_topic(university_user.id, university, 'Testing')
#         blog1 = create_blog(mentor, topic, 'A', '...', image='image.jpeg')
#         create_blog(mentor, topic, 'B', '...', image='image.jpeg')
#
#         query = """
#             {{
#                 universityBlogPosts(order: "title") {{
#                     blogPosts {{
#                         id
#                     }}
#                 }}
#             }}
#         """.format(university_slug=university.slug)
#         response = auth.jwt.graphql(email=university_user.email, query=query)
#
#         posts = response['data']['universityBlogPosts']["blogPosts"]
#         assert len(posts) == 2
#         assert posts[0]['id'] == str(blog1.id)
#
# class TestMyTopics:
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_my_university_topics(self, start_pikachu):
#         _, auth, _ = start_pikachu
#
#         country = CountryFactory.create('GB')
#         university1 = UniversityFactory.create('Edinburgh', country)
#         university2 = UniversityFactory.create('UCL', country)
#         university_user1 = UniversityUserFactory.create('Sam', university1)
#         university_user2 = UniversityUserFactory.create('Tom', university2)
#         mentor = MentorFactory.create('Malcolm', university1, country_code=country.code)
#         topic1 = create_blog_topic(university_user1.id, university1, 'Testing1')
#         topic2 = create_blog_topic(university_user2.id, university2, 'Testing2')
#
#         query = """
#             {
#                 myBlogTopics {
#                     id
#                 }
#             }
#         """
#         response = auth.jwt.graphql(email=mentor.email, query=query)
#
#         topics = response['data']['myBlogTopics']
#         assert len(topics) == 1
#         assert topics[0]['id'] == str(topic1.id)
#
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_my_inactive_topics(self, start_pikachu):
#         _, auth, _ = start_pikachu
#
#         country = CountryFactory.create('GB')
#         university = UniversityFactory.create('Edinburgh', country)
#         university_user = UniversityUserFactory.create('Sam', university)
#         mentor = MentorFactory.create('Malcolm', university, country_code=country.code)
#         topic1 = create_blog_topic(university_user.id, university, 'Testing1')
#         topic2 = create_blog_topic(university_user.id, university, 'Testing2')
#         topic2.modify(active=False)
#
#         query = """
#             {
#                 myBlogTopics {
#                     id
#                 }
#             }
#         """
#         response = auth.jwt.graphql(email=mentor.email, query=query)
#
#         topics = response['data']['myBlogTopics']
#         assert len(topics) == 1
#         assert topics[0]['id'] == str(topic1.id)
#
#
# class TestUniversityTopics:
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_shows_inactive_topics(self, start_pikachu):
#         _, auth, _ = start_pikachu
#
#         country = CountryFactory.create('GB')
#         university = UniversityFactory.create('Edinburgh', country)
#         university_user = UniversityUserFactory.create('Sam', university)
#         topic1 = create_blog_topic(university_user.id, university, 'Testing1')
#         topic2 = create_blog_topic(university_user.id, university, 'Testing2')
#         topic2.modify(active=False)
#
#         query = """
#             {
#                 universityBlogTopics {
#                     id
#                 }
#             }
#         """
#         response = auth.jwt.graphql(email=university_user.email, query=query)
#
#         topics = response['data']['universityBlogTopics']
#         assert len(topics) == 2
#         assert topics[0]['id'] == str(topic1.id)
#         assert topics[1]['id'] == str(topic2.id)
#
#     @pytest.mark.usefixtures('start_pikachu')
#     def test_shows_only_uni_topics(self, start_pikachu):
#         _, auth, _ = start_pikachu
#
#         country = CountryFactory.create('GB')
#         university1 = UniversityFactory.create('Edinburgh', country)
#         university2 = UniversityFactory.create('UCL', country)
#         university_user1 = UniversityUserFactory.create('Sam', university1)
#         university_user2 = UniversityUserFactory.create('Tom', university2)
#         topic1 = create_blog_topic(university_user1.id, university1, 'Testing1')
#         topic2 = create_blog_topic(university_user2.id, university2, 'Testing2')
#
#         query = """
#             {
#                 universityBlogTopics {
#                     id
#                 }
#             }
#         """
#         response = auth.jwt.graphql(email=university_user1.email, query=query)
#
#         topics = response['data']['universityBlogTopics']
#         assert len(topics) == 1
#         assert topics[0]['id'] == str(topic1.id)
