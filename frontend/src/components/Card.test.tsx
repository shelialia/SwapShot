// Card.test.tsx
import { render } from "@testing-library/react";
import "@testing-library/jest-dom/extend-expect";
import TransactionCard from "./Card";
import "@testing-library/jest-dom";


test("renders transaction details", () => {
  const transaction = {
    txId: "0x1234",
    eth_usdt_price: 2400,
    fee_in_usdt: 10,
    fee_in_eth: 0.005,
    gasPrice: 20000000000,
    gasUsed: 21000,
    timeStamp: "1633024800",
  };

  const { getByText } = render(<TransactionCard transaction={transaction} />);

  expect(getByText(/Transaction ID/i)).toBeInTheDocument();
  expect(getByText("0x1234")).toBeInTheDocument();
  expect(getByText("2400")).toBeInTheDocument();
  expect(getByText("10 USDT")).toBeInTheDocument();
  expect(getByText("0.005 ETH")).toBeInTheDocument();
});
