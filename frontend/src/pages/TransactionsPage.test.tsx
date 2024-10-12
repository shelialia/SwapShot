// TransactionsPage.test.tsx
import { render, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom/extend-expect";
import TransactionsPage from "./TransactionsPage";
import "@testing-library/jest-dom";

jest.mock("../services/api", () => ({
  fetchTransactionByTxId: jest.fn(),
  fetchTransactionsByTimeRange: jest.fn(),
  fetchAllTransactions: jest.fn(),
}));

test("renders search form and transaction table", async () => {
  const { getByPlaceholderText, getByText, findByText } = render(
    <TransactionsPage />
  );

  expect(getByPlaceholderText(/Search by Transaction ID/i)).toBeInTheDocument();
  expect(getByText(/Search by Time Range/i)).toBeInTheDocument();

  const startTimeInput = getByPlaceholderText(/Start Time/i);
  fireEvent.change(startTimeInput, { target: { value: "2021-09-30T00:00" } });

  const searchButton = getByText(/Search by Time Range/i);
  fireEvent.click(searchButton);

  await waitFor(() => findByText(/Transaction ID/i));
});
