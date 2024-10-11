import React from "react";
import { Transaction } from "../services/api";
import { Pagination } from "@mui/material";

interface Props {
  transactions: Transaction[];
  page: number;
  setPage: React.Dispatch<React.SetStateAction<number>>;
  pageSize: number;
  setPageSize: React.Dispatch<React.SetStateAction<number>>;
}

const TransactionTable: React.FC<Props> = ({
  transactions,
  page,
  setPage,
  pageSize,
  setPageSize,
}) => {
  const handlePageChange = (
    event: React.ChangeEvent<unknown>,
    value: number
  ) => {
    setPage(value);
  };

  const handlePageSizeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPageSize(parseInt(event.target.value, 10));
  };

  return (
    <div className="mt-6">
      <h2 className="text-xl font-semibold mb-4">Transactions</h2>
      <table className="table-auto w-full border border-gray-200">
        <thead>
          <tr className="bg-gray-100">
            <th className="px-4 py-2">Tx ID</th>
            <th className="px-4 py-2">Fee in ETH</th>
            <th className="px-4 py-2">Fee in USDT</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((txn) => (
            <tr key={txn.txId} className="border-t">
              <td className="px-4 py-2">{txn.txId}</td>
              <td className="px-4 py-2">{txn.fee_in_eth}</td>
              <td className="px-4 py-2">{txn.fee_in_usdt}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Pagination */}
      <div className="flex justify-between items-center mt-4">
        <Pagination
          count={Math.ceil(transactions.length / pageSize)}
          page={page}
          onChange={handlePageChange}
          color="primary"
        />

        {/* Page Size Control */}
        <div>
          <label className="mr-2">Page Size:</label>
          <input
            type="number"
            value={pageSize}
            onChange={handlePageSizeChange}
            className="border px-2 py-1"
            min="1"
            max="100"
          />
        </div>
      </div>
    </div>
  );
};

export default TransactionTable;