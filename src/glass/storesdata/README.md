# Stores Data

This directory contains stores data files. 

The data are encoded as JSON with whole line // comments. Trailing // comments
and /* */ comments are not allowed.

Each file contains a JSON object. The member names are the store names. The member values are arrays with three or four values. The first three values for each store are:

- Type
- Weight
- Load

After that, there may be an object containing additional data, depending on the type of store.
