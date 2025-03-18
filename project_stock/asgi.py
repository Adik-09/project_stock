import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import stock_app.routing  # Import your WebSocket routes

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_stock.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP requests
    "websocket": AuthMiddlewareStack(  # WebSockets
        URLRouter(
            stock_app.routing.websocket_urlpatterns
        )
    ),
})
