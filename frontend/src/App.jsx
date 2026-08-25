import { useEffect, useState } from "react";
import {
  BarChart3,
  CheckCircle2,
  Clock3,
  CreditCard,
  IndianRupee,
  Search,
  XCircle,
  Gift,
  Coins,
} from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import axios from "axios";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

function formatCurrency(value) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 2,
  }).format(Number(value || 0));
}

function App() {
  const [summary, setSummary] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [loadingSummary, setLoadingSummary] = useState(true);
  const [loadingTransactions, setLoadingTransactions] = useState(true);
  const [error, setError] = useState("");

  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);

  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [status, setStatus] = useState("");
  const [paymentMethod, setPaymentMethod] = useState("");

  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");

  const [sortBy, setSortBy] = useState("id");
  const [sortOrder, setSortOrder] = useState("asc");

  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(0);

  // Rewards
  const [rewards, setRewards] = useState([]);
  const [rewardBalance, setRewardBalance] = useState(null);
  const [loadingRewards, setLoadingRewards] = useState(true);
  const [redeemingReward, setRedeemingReward] = useState(null);
  const [rewardMessage, setRewardMessage] = useState("");
  const [rewardError, setRewardError] = useState("");
  const [selectedReward, setSelectedReward] = useState(null);

  useEffect(() => {
    loadSummary();
    loadRewards();
    loadRewardBalance();
  }, []);

  useEffect(() => {
    loadTransactions();
  }, [
    page,
    search,
    category,
    status,
    paymentMethod,
    dateFrom,
    dateTo,
    sortBy,
    sortOrder,
  ]);

  async function loadSummary() {
    try {
      setLoadingSummary(true);
      setError("");

      const response = await axios.get(
        `${API_BASE_URL}/api/transactions/summary`
      );

      setSummary(response.data);
    } catch (err) {
      console.error(err);
      setError("Unable to load transaction summary.");
    } finally {
      setLoadingSummary(false);
    }
  }

  async function loadTransactions() {
    try {
      setLoadingTransactions(true);
      setError("");

      const params = {
        page,
        page_size: pageSize,
        sort_by: sortBy,
        sort_order: sortOrder,
      };

      if (search.trim()) {
        params.search = search.trim();
      }

      if (category) {
        params.category = category;
      }

      if (status) {
        params.status = status;
      }

      if (paymentMethod) {
        params.payment_method = paymentMethod;
      }

      if (dateFrom) {
        params.date_from = `${dateFrom}T00:00:00`;
      }

      if (dateTo) {
        params.date_to = `${dateTo}T23:59:59`;
      }

      const response = await axios.get(
        `${API_BASE_URL}/api/transactions`,
        {
          params,
        }
      );

      setTransactions(response.data.items);
      setTotal(response.data.total);
      setTotalPages(response.data.total_pages);
    } catch (err) {
      console.error(err);
      setError("Unable to load transactions.");
    } finally {
      setLoadingTransactions(false);
    }
  }

  async function loadRewards() {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/api/rewards`
      );

      setRewards(response.data.items || []);
    } catch (err) {
      console.error(err);
      setRewardError("Unable to load rewards.");
    }
  }

  async function loadRewardBalance() {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/api/rewards/balance`
      );

      setRewardBalance(response.data);
    } catch (err) {
      console.error(err);
      setRewardError("Unable to load reward balance.");
    } finally {
      setLoadingRewards(false);
    }
  }

  async function redeemReward(rewardId) {
    try {
      setRedeemingReward(rewardId);
      setRewardMessage("");
      setRewardError("");

      const response = await axios.post(
        `${API_BASE_URL}/api/rewards/redeem`,
        {
          reward_id: rewardId,
        }
      );

      setRewardMessage(response.data.message);
      setSelectedReward(null);

      await loadRewardBalance();
    } catch (err) {
      console.error(err);

      const message =
        err.response?.data?.detail ||
        "Unable to redeem this reward.";

      setRewardError(message);
    } finally {
      setRedeemingReward(null);
    }
  }

  function handleSearchChange(event) {
    setSearch(event.target.value);
    setPage(1);
  }

  function handleFilterChange(setter) {
    return (event) => {
      setter(event.target.value);
      setPage(1);
    };
  }

  function handleDateFromChange(event) {
    setDateFrom(event.target.value);
    setPage(1);
  }

  function handleDateToChange(event) {
    setDateTo(event.target.value);
    setPage(1);
  }

  function handleSortChange(event) {
    setSortBy(event.target.value);
    setPage(1);
  }

  function handleSortOrderChange(event) {
    setSortOrder(event.target.value);
    setPage(1);
  }

  function clearFilters() {
    setSearch("");
    setCategory("");
    setStatus("");
    setPaymentMethod("");
    setDateFrom("");
    setDateTo("");
    setSortBy("id");
    setSortOrder("asc");
    setPage(1);
  }

  const categories = [
    "Education",
    "Entertainment",
    "Food & Dining",
    "Fuel",
    "Groceries",
    "Health",
    "Insurance",
    "Shopping",
    "Travel",
    "Utilities",
  ];

  const paymentMethods = [
    "Credit Card",
    "Debit Card",
    "Netbanking",
    "UPI",
  ];

  return (
    <div className="app">
      <header className="topbar">
        <div>
          <p className="eyebrow">DIGITAL ALPHA</p>

          <h1>Transactions Dashboard</h1>

          <p className="subtitle">
            Monitor transactions, spending patterns and payment activity.
          </p>
        </div>

        <div className="header-status">
          <span className="status-dot" />
          API Connected
        </div>
      </header>

      <main className="container">
        {error && <div className="error-banner">{error}</div>}

        {/* Summary Cards */}
        <section className="stats-grid">
          <StatCard
            title="Total Transactions"
            value={
              loadingSummary
                ? "..."
                : summary?.total_transactions?.toLocaleString("en-IN")
            }
            icon={<BarChart3 size={21} />}
          />

          <StatCard
            title="Total Amount"
            value={
              loadingSummary
                ? "..."
                : formatCurrency(summary?.total_amount)
            }
            icon={<IndianRupee size={21} />}
          />

          <StatCard
            title="Successful"
            value={
              loadingSummary
                ? "..."
                : summary?.successful_transactions?.toLocaleString("en-IN")
            }
            icon={<CheckCircle2 size={21} />}
            variant="success"
          />

          <StatCard
            title="Failed"
            value={
              loadingSummary
                ? "..."
                : summary?.failed_transactions?.toLocaleString("en-IN")
            }
            icon={<XCircle size={21} />}
            variant="danger"
          />

          <StatCard
            title="Pending"
            value={
              loadingSummary
                ? "..."
                : summary?.pending_transactions?.toLocaleString("en-IN")
            }
            icon={<Clock3 size={21} />}
            variant="warning"
          />
        </section>

        {/* Rewards */}
        <section className="card rewards-card">
          <div className="card-heading rewards-heading">
            <div>
              <h2>
                <Gift size={20} />
                Rewards
              </h2>
              <p>
                Redeem your earned coins for rewards.
              </p>
            </div>

            <div className="coin-balance">
              <Coins size={19} />

              <div>
                <span>Available Coins</span>

                <strong>
                  {loadingRewards
                    ? "..."
                    : (
                        rewardBalance?.balance || 0
                      ).toLocaleString("en-IN")}
                </strong>
              </div>
            </div>
          </div>

          {rewardMessage && (
            <div className="reward-success">
              {rewardMessage}
            </div>
          )}

          {rewardError && (
            <div className="reward-error">
              {rewardError}
            </div>
          )}

          <div className="rewards-grid">
            {loadingRewards ? (
              <div className="loading">
                Loading rewards...
              </div>
            ) : rewards.length === 0 ? (
              <div className="empty-state">
                No rewards available.
              </div>
            ) : (
              rewards.map((reward) => {
                const canRedeem =
                  (rewardBalance?.balance || 0) >=
                  reward.coin_cost;

                const isRedeeming =
                  redeemingReward === reward.id;

                return (
                  <div
                    className="reward-item"
                    key={reward.id}
                  >
                    <div className="reward-icon">
                      <Gift size={22} />
                    </div>

                    <div className="reward-info">
                      <strong>{reward.name}</strong>

                      <span>
                        {reward.description}
                      </span>

                      <div className="reward-cost">
                        <Coins size={15} />
                        {reward.coin_cost.toLocaleString(
                          "en-IN"
                        )}{" "}
                        coins
                      </div>
                    </div>

                    <button
                      type="button"
                      className="redeem-button"
                      disabled={
                        !canRedeem || isRedeeming
                      }
                      onClick={() =>
                        setSelectedReward(reward)
                      }
                    >
                      {isRedeeming
                        ? "Redeeming..."
                        : canRedeem
                          ? "Redeem"
                          : "Not enough coins"}
                    </button>
                  </div>
                );
              })
            )}
          </div>
        </section>

        {/* Charts */}
        <section className="charts-grid">
          <div className="card chart-card">
            <div className="card-heading">
              <div>
                <h2>Spending by Category</h2>
                <p>Transaction amount by category</p>
              </div>
            </div>

            <div className="chart-container">
              {loadingSummary ? (
                <div className="loading">
                  Loading chart...
                </div>
              ) : (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={
                      summary?.category_breakdown || []
                    }
                  >
                    <CartesianGrid strokeDasharray="3 3" />

                    <XAxis
                      dataKey="category"
                      angle={-30}
                      textAnchor="end"
                      height={80}
                      tick={{ fontSize: 11 }}
                    />

                    <YAxis
                      tickFormatter={(value) =>
                        `₹${(value / 100000).toFixed(0)}L`
                      }
                    />

                    <Tooltip
                      formatter={(value) =>
                        formatCurrency(value)
                      }
                    />

                    <Bar
                      dataKey="amount"
                      name="Amount"
                      fill="#2563eb"
                      radius={[5, 5, 0, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              )}
            </div>
          </div>

          <div className="card chart-card">
            <div className="card-heading">
              <div>
                <h2>Payment Methods</h2>
                <p>
                  Transaction activity by payment method
                </p>
              </div>
            </div>

            <div className="chart-container">
              {loadingSummary ? (
                <div className="loading">
                  Loading chart...
                </div>
              ) : (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={
                      summary?.payment_method_breakdown ||
                      []
                    }
                  >
                    <CartesianGrid strokeDasharray="3 3" />

                    <XAxis dataKey="payment_method" />

                    <YAxis />

                    <Tooltip
                      formatter={(value, name) => [
                        name === "amount"
                          ? formatCurrency(value)
                          : value,
                        name === "amount"
                          ? "Amount"
                          : "Transactions",
                      ]}
                    />

                    <Legend />

                    <Bar
                      dataKey="count"
                      name="Transactions"
                      fill="#0f766e"
                      radius={[5, 5, 0, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              )}
            </div>
          </div>
        </section>

        {/* Top Merchants */}
        <section className="card merchants-card">
          <div className="card-heading">
            <div>
              <h2>Top Merchants</h2>
              <p>
                Merchants ranked by transaction activity
              </p>
            </div>
          </div>

          <div className="merchant-grid">
            {loadingSummary ? (
              <div className="loading">
                Loading merchants...
              </div>
            ) : (
              summary?.top_merchants?.map(
                (merchant, index) => (
                  <div
                    className="merchant-item"
                    key={merchant.merchant}
                  >
                    <div className="merchant-rank">
                      {index + 1}
                    </div>

                    <div className="merchant-info">
                      <strong>
                        {merchant.merchant}
                      </strong>

                      <span>
                        {merchant.count.toLocaleString(
                          "en-IN"
                        )}{" "}
                        transactions
                      </span>
                    </div>

                    <strong>
                      {formatCurrency(
                        merchant.amount
                      )}
                    </strong>
                  </div>
                )
              )
            )}
          </div>
        </section>

        {/* Transactions */}
        <section className="card transactions-card">
          <div className="transactions-header">
            <div>
              <h2>Transactions</h2>

              <p>
                {total.toLocaleString("en-IN")} matching
                transactions
              </p>
            </div>

            <button
              className="clear-button"
              onClick={clearFilters}
              type="button"
            >
              Clear filters
            </button>
          </div>

          {/* Filters */}
          <div className="filters">
            <div className="search-box">
              <Search size={18} />

              <input
                type="text"
                placeholder="Search merchant..."
                value={search}
                onChange={handleSearchChange}
              />
            </div>

            <select
              value={category}
              onChange={handleFilterChange(
                setCategory
              )}
            >
              <option value="">
                All categories
              </option>

              {categories.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>

            <select
              value={status}
              onChange={handleFilterChange(setStatus)}
            >
              <option value="">
                All statuses
              </option>

              <option value="SUCCESS">
                Success
              </option>

              <option value="FAILED">
                Failed
              </option>

              <option value="PENDING">
                Pending
              </option>
            </select>

            <select
              value={paymentMethod}
              onChange={handleFilterChange(
                setPaymentMethod
              )}
            >
              <option value="">
                All payment methods
              </option>

              {paymentMethods.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>

            <input
              type="date"
              value={dateFrom}
              onChange={handleDateFromChange}
              aria-label="Start date"
              title="Start date"
            />

            <input
              type="date"
              value={dateTo}
              onChange={handleDateToChange}
              aria-label="End date"
              title="End date"
            />

            <select
              value={sortBy}
              onChange={handleSortChange}
            >
              <option value="id">
                Sort by ID
              </option>

              <option value="timestamp">
                Sort by Date
              </option>

              <option value="amount">
                Sort by Amount
              </option>

              <option value="merchant">
                Sort by Merchant
              </option>
            </select>

            <select
              value={sortOrder}
              onChange={handleSortOrderChange}
            >
              <option value="asc">
                Ascending
              </option>

              <option value="desc">
                Descending
              </option>
            </select>
          </div>

          {/* Transaction Table */}
          <div className="table-wrapper">
            {loadingTransactions ? (
              <div className="loading table-loading">
                Loading transactions...
              </div>
            ) : transactions.length === 0 ? (
              <div className="empty-state">
                No transactions found.
              </div>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Transaction ID</th>
                    <th>Date</th>
                    <th>Merchant</th>
                    <th>Category</th>
                    <th>Amount</th>
                    <th>Status</th>
                    <th>Payment Method</th>
                  </tr>
                </thead>

                <tbody>
                  {transactions.map(
                    (transaction) => (
                      <tr key={transaction.id}>
                        <td>
                          #{transaction.id}
                        </td>

                        <td className="transaction-id">
                          {transaction.transaction_id}
                        </td>

                        <td>
                          {new Date(
                            transaction.timestamp
                          ).toLocaleString(
                            "en-IN",
                            {
                              dateStyle: "medium",
                              timeStyle: "short",
                            }
                          )}
                        </td>

                        <td className="merchant-name">
                          {transaction.merchant}
                        </td>

                        <td>
                          {transaction.category || (
                            <span className="muted">
                              Uncategorized
                            </span>
                          )}
                        </td>

                        <td className="amount">
                          {formatCurrency(
                            transaction.amount
                          )}
                        </td>

                        <td>
                          <StatusBadge
                            status={
                              transaction.status
                            }
                          />
                        </td>

                        <td>
                          <span className="payment-method">
                            <CreditCard size={15} />
                            {
                              transaction.payment_method
                            }
                          </span>
                        </td>
                      </tr>
                    )
                  )}
                </tbody>
              </table>
            )}
          </div>

          {/* Pagination */}
          <div className="pagination">
            <span>
              Page {page} of {totalPages || 1}
            </span>

            <div className="pagination-buttons">
              <button
                type="button"
                disabled={page <= 1}
                onClick={() =>
                  setPage(
                    (current) => current - 1
                  )
                }
              >
                Previous
              </button>

              <button
                type="button"
                disabled={
                  totalPages === 0 ||
                  page >= totalPages
                }
                onClick={() =>
                  setPage(
                    (current) => current + 1
                  )
                }
              >
                Next
              </button>
            </div>
          </div>
        </section>
      </main>

      {/* Redemption Confirmation Modal */}
      {selectedReward && (
        <div
          className="modal-backdrop"
          onClick={() =>
            setSelectedReward(null)
          }
        >
          <div
            className="redeem-modal"
            onClick={(event) =>
              event.stopPropagation()
            }
          >
            <div className="modal-icon">
              <Gift size={25} />
            </div>

            <h3>
              Redeem {selectedReward.name}?
            </h3>

            <p>
              You are about to spend{" "}
              <strong>
                {selectedReward.coin_cost.toLocaleString(
                  "en-IN"
                )}{" "}
                coins
              </strong>
              .
            </p>

            <div className="modal-balance">
              <span>Current balance</span>
              <strong>
                {(
                  rewardBalance?.balance || 0
                ).toLocaleString("en-IN")}{" "}
                coins
              </strong>
            </div>

            <div className="modal-actions">
              <button
                type="button"
                className="modal-cancel"
                onClick={() =>
                  setSelectedReward(null)
                }
                disabled={redeemingReward !== null}
              >
                Cancel
              </button>

              <button
                type="button"
                className="modal-confirm"
                onClick={() =>
                  redeemReward(
                    selectedReward.id
                  )
                }
                disabled={
                  redeemingReward !== null ||
                  (rewardBalance?.balance || 0) <
                    selectedReward.coin_cost
                }
              >
                {redeemingReward ===
                selectedReward.id
                  ? "Redeeming..."
                  : "Confirm Redemption"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function StatCard({
  title,
  value,
  icon,
  variant = "",
}) {
  return (
    <div className={`stat-card ${variant}`}>
      <div className="stat-icon">{icon}</div>

      <div>
        <p>{title}</p>
        <h3>{value}</h3>
      </div>
    </div>
  );
}

function StatusBadge({ status }) {
  const normalizedStatus =
    status?.toUpperCase();

  return (
    <span
      className={`status-badge ${normalizedStatus?.toLowerCase()}`}
    >
      {normalizedStatus}
    </span>
  );
}

export default App;
