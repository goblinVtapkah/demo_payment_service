from broker.broker import broker


async def first_try(message):
	await broker.publish(message, queue="payments.retry.1")


async def second_try(message):
	await broker.publish(message, queue="payments.retry.2")


async def third_try(message):
	await broker.publish(message, queue="payments.retry.3")