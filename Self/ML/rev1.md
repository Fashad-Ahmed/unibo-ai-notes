
# Data Science & Python Revision Notes 🐍

This document summarizes key Pandas, SciPy, and Scikit-learn commands and concepts for data manipulation and machine learning.

***

## 🐼 Pandas DataFrames

| Topic | Code Snippet | Explanation |
| :--- | :--- | :--- |
| **Wide to Long Format** (Melt/Unpivot) | `df = pd.melt(df, id_vars='id', value_vars=['math', 'chemistry'])` | Converts columns (`value_vars`) into row entries under a new `variable` and `value` column, using `id_vars` as identifiers. |
| **Remove Duplicates** | `df_cleaned = df.drop_duplicates()` | Removes identical rows, keeping the first occurrence. Useful for cleaning records like duplicate grades. |
| **Fill Missing Values (`NaN`)** | `df = df.fillna(80)` | Replaces **all** `NaN` values in the DataFrame with the value `80`. |
| **Fill Specific Column `NaN`** | `df['col'] = df['col'].fillna(df['col'].mean())` | Fills `NaN` values in a single column using a specific statistic (e.g., the mean) for imputation. |
| **Forward Fill Missing Values** | `times.fillna(method='ffill')` | Replaces `NaN` with the **last known valid observation** (propagates the value forward). Useful for time-series data. |
| **Convert to Lowercase** | `jobs['roles'].str.lower()` | Uses the `.str` accessor to apply the `.lower()` string method element-wise to a text column. |
| **Remove Leading Whitespace** | `df['col'].str.lstrip()` | Uses the `.str` accessor and the `.lstrip()` method to remove spaces/tabs only from the **left side** of strings. |
| **Remove ALL Spaces** | `df['col'].str.replace(' ', '')` | Replaces every occurrence of a space character with an empty string. |
| **Convert to Category Type** | `df['my_column'].astype('category')` | Converts a column's data type to `category`. Improves memory efficiency for columns with low cardinality (few unique values). |
| **Calculate D-Types** | `print(df.dtypes)` | Displays the data type (`int64`, `object`, `float64`, etc.) for every column in the DataFrame. |

***

## 📊 Data Import & Aggregation

| Task | Code Snippet | Key Parameter/Function |
| :--- | :--- | :--- |
| **Read only Specific Columns** | `pd.read_csv(file, usecols=['style', 'type', 'price'])` | `usecols`: A list of column names to import. |
| **Read only N Rows** | `pd.read_csv(file, nrows=4)` | `nrows`: Specifies the maximum number of data rows to read from the file (after the header). |
| **Load MATLAB (`.mat`) File** | `scipy.io.loadmat(file_name)` | Function from `scipy.io` that loads a MATLAB file as a **Python dictionary**. |
| **Load HDF5 File** | `hf = h5py.File('data.hdf5', 'r')` | Primary function in the `h5py` package to open and interact with HDF5 files. |
| **Compute Aggregates (Pivot Table)** | `pd.pivot_table(df, values=[...], index='cuisine', aggfunc=np.mean)` | `aggfunc`: Specifies the function (e.g., `np.mean`, `sum`, `count`) to use for aggregation. |

***

## 🤖 Scikit-learn (Cross-Validation)

| Concept | Code Snippet | Description |
| :--- | :--- | :--- |
| **Import Modules** | `from sklearn.model_selection import KFold, cross_val_score` | Imports the necessary tools for model evaluation. |
| **Setup KFold** | `kf = KFold(n_splits=6, shuffle=True, random_state=5)` | Defines the cross-validation strategy: 6 folds, shuffles data for randomness, and uses a fixed seed (`random_state`) for reproducibility. |
| **Compute Scores** | `cv_scores = cross_val_score(reg, X, y, cv=kf)` | Performs the cross-validation: fits the model (`reg`) on training folds and evaluates it on testing folds using the splitting strategy defined by `cv=kf`. |