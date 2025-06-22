import os
import ssl
import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()

# --- The rest of your code follows ---
import streamlit as st

# Symbolic types
class Symbol: pass
# ... and so on
import streamlit as st

# --- Symbolic Type Definitions ---
# These classes represent the distinct elements of the set S.

class Symbol:
    """Base class for all elements in the system."""
    pass

class Real(Symbol):
    """Represents a real number from the set R."""
    def __init__(self, value):
        self.value = float(value)
    def __repr__(self):
        # Show integers without the .0
        if self.value.is_integer():
            return f"Real({int(self.value)})"
        return f"Real({self.value})"

class MeasuredZero(Symbol):
    """Represents the element 0m."""
    def __repr__(self):
        return "0m"

class AbsoluteZero(Symbol):
    """Represents the element 0bm, the additive identity."""
    def __repr__(self):
        return "0bm"

class TransientOne(Symbol):
    """Represents the element 1t, which emerges from 0m/0m."""
    def __repr__(self):
        return "1t"

# --- Axiomatic Operations ---
# These functions implement the axioms defined in the paper.

def add(a, b):
    """Implements the addition axioms A1, A2, A3, and A4."""
    # Axiom A1: x + 0bm = x
    if isinstance(a, AbsoluteZero): return b
    if isinstance(b, AbsoluteZero): return a

    # Axiom A4: a + 1t = a + 1 and 1t + 1t = 2
    if isinstance(a, TransientOne) and isinstance(b, TransientOne): return Real(2)
    if isinstance(a, TransientOne) and isinstance(b, Real): return Real(b.value + 1)
    if isinstance(b, TransientOne) and isinstance(a, Real): return Real(a.value + 1)

    # Axiom A3: a + 0m = a and 0m + 0m = 0m
    if isinstance(a, MeasuredZero) and isinstance(b, MeasuredZero): return MeasuredZero()
    if isinstance(a, Real) and isinstance(b, MeasuredZero): return a
    if isinstance(b, Real) and isinstance(a, MeasuredZero): return b

    # Axiom A2: Standard real addition
    if isinstance(a, Real) and isinstance(b, Real): return Real(a.value + b.value)
    
    # All other cases, like 1t + 0m, are undefined by the axioms.
    return "Undefined"

def mul(a, b):
    """Implements the multiplication axioms M1, M2, and M3."""
    # Axiom M1: x * 0bm = 0bm
    if isinstance(a, AbsoluteZero) or isinstance(b, AbsoluteZero): return AbsoluteZero()

    # Axiom M3 (Special Case): 1t * 0m = 0m. Handle this explicitly first.
    if (isinstance(a, TransientOne) and isinstance(b, MeasuredZero)) or \
       (isinstance(b, TransientOne) and isinstance(a, MeasuredZero)):
        return MeasuredZero()
    
    # Axiom M2: x * 0m = 0m (for x not being 1t, which is handled above)
    if isinstance(a, MeasuredZero) or isinstance(b, MeasuredZero): return MeasuredZero()
    
    # Axiom M3 (General Case): 1t * x = x for x != 0m
    if isinstance(a, TransientOne): return b
    if isinstance(b, TransientOne): return a
        
    # Standard real multiplication
    if isinstance(a, Real) and isinstance(b, Real): return Real(a.value * b.value)
    
    # All other cases are undefined.
    return "Undefined"

def div(a, b):
    """Implements the division axioms D1 and D2."""
    # Axiom D1: x / 0bm = 0bm
    if isinstance(b, AbsoluteZero): return AbsoluteZero()
    
    # Axiom D2: 0m / 0m = 1t
    if isinstance(a, MeasuredZero) and isinstance(b, MeasuredZero): return TransientOne()
    
    # Standard real division
    if isinstance(a, Real) and isinstance(b, Real):
        if b.value == 0:
            # The theory distinguishes 0 from 0bm and 0m. Division by real 0 is still classically undefined.
            return "Classically Undefined (division by real 0)"
        return Real(a.value / b.value)
        
    # All other cases, like 1/0m, are undefined by the axioms.
    return "Undefined"

# --- User Interface Setup (using Streamlit) ---

st.set_page_config(layout="wide")
st.title("🧮 Measurement-Based Mathematics Engine")
st.markdown("An interactive calculator to demonstrate the algebraic system from the paper 'A Formal Theory of Measurement-Based Mathematics'.")

# Define the set of selectable inputs
symbol_map = {
    "Real(5)": Real(5),
    "Real(7)": Real(7),
    "Real(2)": Real(2),
    "Real(-5)": Real(-5),
    "Real(0)": Real(0),
    "0m (Measured Zero)": MeasuredZero(),
    "0bm (Absolute Zero)": AbsoluteZero(),
    "1t (Transient One)": TransientOne()
}

# Create columns for layout
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Operand 1")
    input1_str = st.selectbox("Select the first value", options=symbol_map.keys(), key="op1")
    sym1 = symbol_map[input1_str]

with col2:
    st.subheader("Operation")
    operation_str = st.selectbox("Select the operation", options=["+", "×", "/"], key="op")

with col3:
    st.subheader("Operand 2")
    input2_str = st.selectbox("Select the second value", options=symbol_map.keys(), key="op2")
    sym2 = symbol_map[input2_str]

# Perform calculation when a button is pressed
if st.button("Calculate", use_container_width=True):
    if operation_str == "+":
        result = add(sym1, sym2)
    elif operation_str == "×":
        result = mul(sym1, sym2)
    elif operation_str == "/":
        result = div(sym1, sym2)
    else:
        result = "Unknown operation"

    # Display the result
    st.markdown("---")
    st.subheader("Result")
    st.markdown(f"#### `{sym1} {operation_str} {sym2} = {result}`")