import { render, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom/extend-expect";
import TransactionTable from "./TransactionTable";
import "@testing-library/jest-dom";

test("renders transaction table with pagination and additional attributes", () => {
  const transactions = [
    {
      txId: "0x1",
      timeStamp: "1633024800",
      eth_usdt_price: 3000,
      fee_in_usdt: 10,
      fee_in_eth: 0.0033,
    }, // Added missing attributes
    {
      txId: "0x2",
      timeStamp: "1633025800",
      eth_usdt_price: 3100,
      fee_in_usdt: 12,
      fee_in_eth: 0.0039,
    }, // Added missing attributes
  ];

  const onTransactionClick = jest.fn();
  const setPage = jest.fn();
  const setPageSize = jest.fn();

  const { getByText, getAllByRole } = render(
    <TransactionTable
      transactions={transactions}
      page={1}
      setPage={setPage}
      pageSize={50}
      setPageSize={setPageSize}
      total={100}
      onTransactionClick={onTransactionClick}
    />
  );

  expect(getByText(/Tx ID/i)).toBeInTheDocument();
  expect(getByText("0x1")).toBeInTheDocument();
  expect(getByText("0x2")).toBeInTheDocument();
  expect(getByText("3000")).toBeInTheDocument(); // Verify eth_usdt_price is rendered
  expect(getByText("10")).toBeInTheDocument(); // Verify fee_in_usdt is rendered
  expect(getByText("0.0033")).toBeInTheDocument(); // Verify fee_in_eth is rendered

  const rows = getAllByRole("row");
  fireEvent.click(rows[1]);
  expect(onTransactionClick).toHaveBeenCalledWith("0x1");
});

test("handles page change with additional attributes", () => {
  const transactions = [
    {
      txId: "0x1",
      timeStamp: "1633024800",
      eth_usdt_price: 3000,
      fee_in_usdt: 10,
      fee_in_eth: 0.0033,
    }, // Added missing attributes
    {
      txId: "0x2",
      timeStamp: "1633025800",
      eth_usdt_price: 3100,
      fee_in_usdt: 12,
      fee_in_eth: 0.0039,
    }, // Added missing attributes
  ];

  const onTransactionClick = jest.fn();
  const setPage = jest.fn();
  const setPageSize = jest.fn();

  const { getByLabelText } = render(
    <TransactionTable
      transactions={transactions}
      page={1}
      setPage={setPage}
      pageSize={50}
      setPageSize={setPageSize}
      total={100}
      onTransactionClick={onTransactionClick}
    />
  );

  const input = getByLabelText("Page Size:");
  fireEvent.change(input, { target: { value: "25" } });
  expect(setPageSize).toHaveBeenCalledWith(25);
});
