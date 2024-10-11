import React from "react";
import TransactionsPage from "./pages/TransactionsPage"; // Import the TransactionsPage

const App: React.FC = () => {
  return (
    <div className="App">
      <TransactionsPage /> {/* Render the TransactionsPage */}
    </div>
  );
};

export default App;