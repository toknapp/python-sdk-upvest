import os

from .partials.client_instance import create_tenancy_client

tenancy = create_tenancy_client()

webhook_url = os.getenv("WEBHOOK_URL", "")
webhook_verification_url = os.getenv("WEBHOOK_VERIFICATION_URL", "")

dummy_webhook = {
    "url": webhook_url,
    "name": "test-webhook",
    "headers": {"X-Test": "Hello world!"},
    "version": "1.2",
    "status": "ACTIVE",
    "event_filters": ["upvest.wallet.created", "ropsten.block.*", "upvest.echo.post"],
    "hmac_secret_key": "abcdef",
}

def test_webhook_verify():
    is_verified = tenancy.webhooks.verify(webhook_url)
    assert is_verified

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


def test_retrieve_webhook():
    webhooks = tenancy.webhooks.all()
    webhook_id = webhooks[0].id
    webhook = tenancy.webhooks.get(webhook_id)
    assert webhook.url == dummy_webhook["url"]


def test_delete_webhook():
    webhooks = tenancy.webhooks.all()
    webhook_id = webhooks[0].id
    is_deleted = tenancy.webhooks.delete(webhook_id)
    assert is_deleted
