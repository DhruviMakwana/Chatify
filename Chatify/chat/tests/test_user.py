from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

REGISTER = "api/register/"
USER_LIST_API = "chat/api/get_online_user/"
LOGIN_API = "api/login/"
SENDING_FILE_URL = "api/savefile/"
UNSENT_MESSAGE_API_URL = "api/unsend-message/"
ATTACHMENT_URL_API = "api/savefile/"


class UserTest(TestCase):
    def test_user_test(self):
        from chat.factory import UserFactory

        UserFactory()


class ChatGroupTest(TestCase):
    def test_chat_group(self):
        from chat.factory import GroupNameFactory

        GroupNameFactory()


class ChatFactoryTest(TestCase):
    def test_chat(self):
        from chat.factory import ChatFactory

        ChatFactory()


class RegistrationApiTest(APITestCase):
    def test_user_registration(self):
        from chat.factory import UserFactory

        user = UserFactory()
        data = {
            "mobile_number": "2345667888",
            "username": "nayan",
            "password": "1234",
            "profile_photo": "a1.jpg",
        }
        response = self.client.post(REGISTER, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetOnlineUserList(APITestCase):
    def test_online_user_list(self):
        self.client = APIClient()
        # surl = reverse("chat : get_online_user")
        response = self.client.get(USER_LIST_API)
        # url = "http://127.0.0.1:8000/chat/api/get_online_user/"
        # response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LoginTestCase(APITestCase):
    def test_login_api(self):
        data = {
            "username": "abc",
            "password": "1234",
        }
        response = self.client.post(LOGIN_API, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SendingFileAPI(APITestCase):
    def test_sending_file(self):
        data = {
            "mobile_number": "1234567888",
            "username": "abc123",
            "password": "1234",
            "profile_photo": "a1.jpg",
        }
        response = self.client.post(SENDING_FILE_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SaveUnsentMessageTest(APITestCase):
    def test_save_unsent_message(self):
        from chat.factory import UserFactory, GroupNameFactory, ChatFactory

        user = UserFactory()
        GroupNameFactory()
        chat = ChatFactory()

        # Make a POST request to the API endpoint
        data = {
            "requestUser": user.id,
            "currentUser": user.id,
            "message": chat.message,
        }
        response = self.client.post(UNSENT_MESSAGE_API_URL, data)
        self.assertEqual(response.status_code, 200)

        chat.refresh_from_db()
        self.assertTrue(chat.is_deleted)


class SaveAttachmentTest(APITestCase):
    def test_save_attachment(self):
        from chat.factory import UserFactory, ChatFactory, GroupNameFactory
        from chat.models import Chat, ChatGroup
        from datetime import datetime
        from chat.websocket_utils import get_group_name

        # Create test data using factories
        sender = UserFactory()
        receiver = UserFactory()
        date = "20/06/2023, 12:34:56 PM"
        file = "example.png"
        # Make a POST request to the API endpoint
        data = {
            "senderId": sender.id,
            "receiverId": receiver.id,
            "date": date,
            "file": file,
            "timezone": "UTC",  # Example timezone value
        }
        response = self.client.post(ATTACHMENT_URL_API, data)
        self.assertEqual(response.status_code, 200)
        chat = Chat.objects.last()
        self.assertEqual(chat.sent_at, datetime.strptime(date, "%d/%m/%Y, %I:%M:%S %p"))
        self.assertEqual(chat.sender, sender)
        self.assertEqual(chat.attachment, file)

        # Check if a ChatGroup object was created or retrieved correctly
        group_name = get_group_name(sender.id, receiver.id)
        chat_group = ChatGroup.objects.get(name=group_name)
        self.assertEqual(chat.group, chat_group)


class ChatMessagesTest(APITestCase):
    def test_chat_messages(self):
        from chat.factory import UserFactory, ChatFactory, GroupNameFactory
        from chat.serializers import ChatMessageSerializer

        user = UserFactory()
        group_member = UserFactory()
        chat_group = GroupNameFactory()
        chat1 = ChatFactory(group=chat_group)
        chat2 = ChatFactory(group=chat_group)
        # Make a GET request to the API endpoint
        url = f"/chat/api/messages/{chat_group.pk}/"
        self.client.force_authenticate(user=user)
        response = self.client.get(url)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Assert the response data
        expected_data = {
            "messageData": ChatMessageSerializer([chat1, chat2], many=True).data
        }
        self.assertEqual(response.json(), expected_data)


class VisibilityStatusTestCase(APITestCase):
    def setUp(self):
        from chat.models import User

        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_visibility_status_api(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        data = {"id": self.user.id, "status": "online"}

        response = self.client.post("/api/visibility-status/", data=data)

        self.assertEqual(response.status_code, 200)


class ChatViewTestCase(TestCase):
    def test_register_view(self):
        response = self.client.get("register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat/register.html")


class LoginUiTest(TestCase):
    def test_login_view(self):
        response = self.client.get("login_page/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat/login.html")


class ChatUITestCase(TestCase):
    def test_chat_view(self):
        response = self.client.get("chat/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat/chat.html")
