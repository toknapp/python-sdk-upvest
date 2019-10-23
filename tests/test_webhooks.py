from .partials.client_instance import create_tenancy_client

tenancy = create_tenancy_client()


dummy_webhook = {
    "url": "https://upvest-raphael-flexapp.appspot.com/webhook/platitude--raphael-local-generic--tenant-1",
    "headers": {"X-Test": "Hello world!"},
    "version": "1.2",
    "status": "ACTIVE",
    "event_filters": ["wallet.created", "*", "wallet.*"],
    "hmac_secret_key": "abcdef",
}


def test_create_webhook():
    """Tests an API call to create a webhook"""
    is_created = tenancy.webhooks.create(**dummy_webhook)
    assert is_created


def test_list_webhooks():
    """Tests an API call to get a list of webhooks"""
    webhooks = tenancy.webhooks.all()
    assert isinstance(webhooks, list)
    webhook_id = webhooks[0].id
    webhook = tenancy.webhooks.get(webhook_id)
    assert webhook.url == dummy_webhook["url"]


def test_update_webhook():
    """Tests an API call to update a webhook"""
    webhooks = tenancy.webhooks.all()
    webhook_id = webhooks[0].id
    webhook = tenancy.webhooks.get(webhook_id)
    # update and save the webhook
    webhook2 = dict(webhook, hmac_secret_key="123456")
    is_updated = tenancy.webhooks.update(webhook_id, **webhook2)
    assert is_updated


def test_delete_webhook():
    webhooks = tenancy.webhooks.all()
    webhook_id = webhooks[0].id
    is_deleted = tenancy.webhooks.delete(webhook_id)
    assert is_deleted


def test_retrieve_webhook():
    webhooks = tenancy.webhooks.all()
    webhook_id = webhooks[0].id
    webhook = tenancy.webhooks.get(webhook_id)
    assert webhook.url == dummy_webhook["url"]
