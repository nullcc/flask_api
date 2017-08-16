# -*- coding: utf-8 -*-

from flask_api.config import config
from .user import UserService
from .message import MessageService

user_service = UserService(config.CORE_SERVICE_URL, "user")
message_service = MessageService(config.CORE_SERVICE_URL, "message")
