from faststream.rabbit import RabbitQueue, RabbitExchange, ExchangeType

payments_new = RabbitQueue(
	"payments.new",
	routing_key="create",
    durable=True,
    arguments={
        "x-dead-letter-exchange": "payments.dlx",
        "x-dead-letter-routing-key": "dlq",
    },
)

payments_dlx = RabbitExchange(
	"payments.dlx",
	type=ExchangeType.DIRECT,
    durable=True,
)

payments_retry_1 = RabbitQueue(
    "payments.retry.1",
    durable=True,
    arguments={
        "x-message-ttl": 5000,
        "x-dead-letter-exchange": "payments.dlx",
        "x-dead-letter-routing-key": "create",
    },
)

payments_retry_2 = RabbitQueue(
    "payments.retry.2",
    durable=True,
    arguments={
        "x-message-ttl": 10000,
        "x-dead-letter-exchange": "payments.dlx",
        "x-dead-letter-routing-key": "create",
    },
)

payments_retry_3 = RabbitQueue(
    "payments.retry.3",
    durable=True,
    arguments={
        "x-message-ttl": 20000,
        "x-dead-letter-exchange": "payments.dlx",
        "x-dead-letter-routing-key": "create",
    },
)

payments_dlq = RabbitQueue(
    "payments.dlq",
    durable=True,
	routing_key="dlq",
)