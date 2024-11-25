import React, { useState } from "react";
import { Modal, Button, message } from "antd";
import {
  CardElement,
  useStripe,
  useElements,
} from "@stripe/react-stripe-js";

interface PaymentModalProps {
  isVisible: boolean;
  amount: number; 
  onCancel: () => void;
  onPaymentSuccess: () => void;
}

const PaymentModal: React.FC<PaymentModalProps> = ({
  isVisible,
  amount,
  onCancel,
  onPaymentSuccess,
}) => {
  const stripe = useStripe();
  const elements = useElements();
  const [loading, setLoading] = useState(false);

  const handlePayment = async () => {
    if (!stripe || !elements) {
      message.error("Stripe has not loaded yet. Please try again.");
      return;
    }

    setLoading(true);

    try {
        // 4242 4242 4242 4242 
        onPaymentSuccess();
    } catch (err) {
      console.error(err);
      message.error("An error occurred during payment.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      title="Complete Your Payment"
      visible={isVisible}
      onCancel={onCancel}
    >
      <div>
        <p>Total Amount: ${amount.toFixed(2)}</p>
        <CardElement />
        <Button
          type="primary"
          onClick={handlePayment}
          loading={loading}
          style={{ marginTop: "1rem" }}
        >
          Pay ${amount.toFixed(2)}
        </Button>
      </div>
    </Modal>
  );
};

export default PaymentModal;
