import streamlit as st

# ---------------------------
# Account Class
# ---------------------------
class Account:
    def __init__(self, account_number, pin, balance=0):
        self.account_number = account_number
        self.pin = pin
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposited ₹{amount}")

    def withdraw(self, amount):
        if amount > self.balance:
            self.transactions.append(
                f"Failed Withdrawal ₹{amount} (Insufficient Balance)"
            )
            return False

        self.balance -= amount
        self.transactions.append(f"Withdrawn ₹{amount}")
        return True


# ---------------------------
# Initialize Session State
# ---------------------------
if "accounts" not in st.session_state:
    st.session_state.accounts = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None


# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="ATM Management System",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 ATM Management System")


# ---------------------------
# Logged In User Dashboard
# ---------------------------
if st.session_state.logged_in:

    account = st.session_state.accounts[
        st.session_state.current_user
    ]

    st.success(
        f"Logged in as {account.account_number}"
    )

    menu = st.sidebar.selectbox(
        "Select Option",
        [
            "Balance",
            "Deposit",
            "Withdraw",
            "Transaction History",
            "Logout"
        ]
    )

    if menu == "Balance":
        st.subheader("💰 Account Balance")

        st.metric(
            label="Current Balance",
            value=f"₹{account.balance:.2f}"
        )

    elif menu == "Deposit":
        st.subheader("➕ Deposit Money")

        amount = st.number_input(
            "Enter Amount",
            min_value=1.0,
            step=100.0
        )

        if st.button("Deposit"):
            account.deposit(amount)

            st.success(
                f"₹{amount:.2f} deposited successfully!"
            )

    elif menu == "Withdraw":
        st.subheader("➖ Withdraw Money")

        amount = st.number_input(
            "Enter Amount",
            min_value=1.0,
            step=100.0
        )

        if st.button("Withdraw"):
            success = account.withdraw(amount)

            if success:
                st.success(
                    f"₹{amount:.2f} withdrawn successfully!"
                )
            else:
                st.error(
                    "Insufficient Balance!"
                )

    elif menu == "Transaction History":
        st.subheader("📜 Transaction History")

        if account.transactions:
            for t in reversed(account.transactions):
                st.write("•", t)
        else:
            st.info("No transactions yet.")

    elif menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.current_user = None

        st.success("Logged Out Successfully")

        st.rerun()

# ---------------------------
# Login / Create Account
# ---------------------------
else:

    tab1, tab2 = st.tabs(
        ["🔐 Login", "📝 Create Account"]
    )

    # -----------------------
    # LOGIN
    # -----------------------
    with tab1:

        st.subheader("Login")

        login_acc = st.text_input(
            "Account Number"
        )

        login_pin = st.text_input(
            "PIN",
            type="password"
        )

        if st.button("Login"):

            if login_acc in st.session_state.accounts:

                acc = st.session_state.accounts[
                    login_acc
                ]

                if acc.pin == login_pin:

                    st.session_state.logged_in = True
                    st.session_state.current_user = login_acc

                    st.success(
                        "Login Successful!"
                    )

                    st.rerun()

                else:
                    st.error("Invalid PIN")

            else:
                st.error(
                    "Account Not Found"
                )

    # -----------------------
    # CREATE ACCOUNT
    # -----------------------
    with tab2:

        st.subheader("Create New Account")

        new_acc = st.text_input(
            "New Account Number"
        )

        new_pin = st.text_input(
            "Create PIN",
            type="password"
        )

        initial_balance = st.number_input(
            "Initial Deposit",
            min_value=0.0,
            step=100.0
        )

        if st.button("Create Account"):

            if not new_acc:
                st.error(
                    "Account Number Required"
                )

            elif new_acc in st.session_state.accounts:
                st.error(
                    "Account Already Exists"
                )

            else:

                st.session_state.accounts[
                    new_acc
                ] = Account(
                    new_acc,
                    new_pin,
                    initial_balance
                )

                st.success(
                    "Account Created Successfully!"
                )
