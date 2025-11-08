
"""
Unit tests for payment_service.py to raise overall coverage for Task 2.2.

"""

import time
import pytest
from services.payment_service import PaymentGateway


def test_process_payment_success(mocker):
    """
    Should return success tuple when amount > 0, <= 1000, and patron_id length == 6.
    """
    mocker.patch.object(time, "sleep", return_value=None)
    gateway = PaymentGateway()
    ok, txn, msg = gateway.process_payment("123456", 10.5, "Late fees")
    assert ok is True
    assert txn.startswith("txn_")
    assert "processed successfully" in msg


@pytest.mark.parametrize("amount", [0.0, -1.0])
def test_process_payment_invalid_amount_non_positive(mocker, amount):
    """
    Should reject non-positive amounts.
    """
    mocker.patch.object(time, "sleep", return_value=None)
    gateway = PaymentGateway()
    ok, txn, msg = gateway.process_payment("123456", amount, "x")
    assert ok is False
    assert txn == ""
    assert "Invalid amount" in msg


def test_process_payment_amount_exceeds_limit(mocker):
    """
    Should reject amounts greater than 1000.
    """
    mocker.patch.object(time, "sleep", return_value=None)
    gateway = PaymentGateway()
    ok, txn, msg = gateway.process_payment("123456", 1000.01, "x")
    assert ok is False
    assert txn == ""
    assert "exceeds limit" in msg


def test_process_payment_invalid_patron_id_length(mocker):
    """
    Should reject invalid patron_id length.
    """
    mocker.patch.object(time, "sleep", return_value=None)
    gateway = PaymentGateway()
    ok, txn, msg = gateway.process_payment("12345", 10.0, "x")
    assert ok is False
    assert txn == ""
    assert "Invalid patron ID format" in msg


def test_refund_payment_success(mocker):
    """
    Should return success tuple for a valid refund.
    """
    mocker.patch.object(time, "sleep", return_value=None)
    gateway = PaymentGateway()
    ok, msg = gateway.refund_payment("txn_123", 7.5)
    assert ok is True
    assert "processed successfully" in msg


@pytest.mark.parametrize("txn", ["", "abc", None])
def test_refund_payment_invalid_txn_id(mocker, txn):
    """
    Should reject invalid transaction_id.
    """
    mocker.patch.object(time, "sleep", return_value=None)
    gateway = PaymentGateway()
    ok, msg = gateway.refund_payment(txn, 5.0)
    assert ok is False
    assert "Invalid transaction ID" in msg


@pytest.mark.parametrize("amount", [0.0, -3.0])
def test_refund_payment_invalid_amount_non_positive(mocker, amount):
    """
    Should reject non-positive refund amount.
    """
    mocker.patch.object(time, "sleep", return_value=None)
    gateway = PaymentGateway()
    ok, msg = gateway.refund_payment("txn_123", amount)
    assert ok is False
    assert "Invalid refund amount" in msg


def test_verify_payment_status_completed(mocker):
    """
    Should return completed status for a valid transaction id.
    """
    mocker.patch.object(time, "sleep", return_value=None)
    gateway = PaymentGateway()
    result = gateway.verify_payment_status("txn_123")
    assert result["status"] == "completed"
    assert result["transaction_id"] == "txn_123"


@pytest.mark.parametrize("txn", ["", None, "bad"])
def test_verify_payment_status_not_found(mocker, txn):
    """
    Should return not_found for invalid transaction ids.
    """
    mocker.patch.object(time, "sleep", return_value=None)
    gateway = PaymentGateway()
    result = gateway.verify_payment_status(txn)
    assert result["status"] == "not_found"
